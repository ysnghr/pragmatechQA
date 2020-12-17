from django.http import JsonResponse, QueryDict
from student.models import *
from student.forms import *
import requests, random, string
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime
from student.utils import FilterComments
from taggit.models import Tag
from itertools import chain
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from student.decorators import *
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib import messages
from django.db.models import Q
import datetime


password_characters = string.ascii_letters + string.digits + string.punctuation

auth = ('admin', 'admin123')

@login_required
@picture_required
def home(request, extra_context=None):
    template='main_page/home.html'
    page_template='main_page/question_list.html'
    context={
        'questions':Question.objects.all().order_by('-updated'),
        'page_template':page_template,
    }

    if request.is_ajax():
        template = page_template
    return render(request, template, context)

@login_required
@picture_required
def tags(request):
    template = 'categories/tags.html' 
    page_template = 'categories/tag-list.html'
    context={
        'tags' : Tag.objects.all().order_by('name') if Tag.objects.all() else -1,
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)

@login_required
@picture_required
def tag_info(request, slug):
    template = 'categories/single-tag.html' 
    page_template = 'categories/single-tag-questions.html'
    tag = Tag.objects.filter(slug = slug).first()
    questions = Question.objects.filter(tags__in = [tag])
    context={
        "tag" : tag,
        "questions" : questions,
        "page_template": page_template,
    }
    if request.is_ajax():
        template = page_template
    return render(request, 'categories/single-tag.html', context)

@login_required
@picture_required
def about(request):
    context={
        'roles': Role.objects.all(),
        'students': Student.objects.all().order_by('level')[0:10],
    }
    return render(request, 'main_page/about.html', context)

@login_required
@picture_required
def rules(request):
    return render(request, 'main_page/rules.html')

@login_required
@picture_required
def page_create_topic(request):
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST or None)
        if form.is_valid():
            new_question = form.save()  
            student = Student.objects.get(user = request.user)
            student.level +=3
            new_question.student = student
            new_question.save()
            student.save()
            if((len(request.FILES) == 1) and (request.FILES['file[0]'].name == 'blob')):
                pass
            else:
                MAX_FILES = 2 # The number of max files (Client-Side 2)
                if (len(request.FILES) <= MAX_FILES ): 
                    for imageKey, imageValue in request.FILES.items():
                        questionData = {'question' : new_question}
                        imageData = {'image' : imageValue}
                        formImage = QuestionImageForm(questionData, imageData)
                        if(formImage.is_valid()):
                            formImage.save()
                        else:
                            return JsonResponse(formImage.errors.as_json(), safe = False)  
                else:
                    return JsonResponse(JsonResponse({'max_files' : 2}, safe = False))
                    
            return JsonResponse({'data' : 'form_valid'})
        else:
            return JsonResponse(form.errors.as_json(), safe = False)

    context={
        'form':form,
    }
    return render(request, 'main_page/post_create.html', context)

@login_required
@picture_required
def question_detail(request, slug):
    question = get_object_or_404(Question, slug=slug)
    comments = question.comment_set.all()
    # print('Comment: ')
    # print(FilterComments(question))
    # print(comments)
    if request.method=="POST":
        if request.is_ajax():
            if(request.POST['post_type'] == 'comment_create'):
                question = get_object_or_404(Question, id = int(request.POST['question_id']))
                student = Student.objects.get(user = request.user)
                comment_data = request.POST.copy()
                comment_data['question'] = question
                comment_data['student'] = student
                del comment_data['post_type']
                del comment_data['question_id']
                commentForm = CommentForm(comment_data)
                if(commentForm.is_valid()):
                    student.level +=1
                    student.save()
                    new_comment = commentForm.save()
                    if((len(request.FILES) == 1) and (request.FILES['file[0]'].name == 'blob')):
                        pass
                    else:
                        MAX_FILES = 2 # The number of max files (Client-Side 2)
                        if (len(request.FILES) <= MAX_FILES ): 
                            for imageKey, imageValue in request.FILES.items():
                                commentData = {'comment' : new_comment}
                                imageData = {'image' : imageValue}
                                commentImage = CommentImageForm(commentData, imageData)
                                if(commentImage.is_valid()):
                                    commentImage.save()
                                else:
                                    return JsonResponse(commentImage.errors.as_json(), safe = False)  
                        else:
                            return JsonResponse({'max_files' : 2})                            
                    comment_data = {}
                    comment_data['full_name'] = f'{new_comment.student.user.get_full_name()}'
                    comment_data['created_date'] = f'{(new_comment.created).strftime("%d %B, %Y")}'
                    comment_data['content'] = f'{new_comment.content}'
                    comment_data['question_id'] = int(f'{new_comment.question.id}')
                    comment_data['comment_id'] = int(f'{new_comment.id}')
                    comment_data['owner'] = True if question.student.user == request.user else False
                    comment_data['images'] = [comment_image.image.url for comment_image in new_comment.commentimage_set.all()]
                    return JsonResponse(comment_data)
            
            elif(request.POST['post_type'] == 'question_vote'):
                question = get_object_or_404(Question,id=request.POST.get("id"))
                stud = Student.objects.get(user=request.user)
                liked = question.action_set.filter(action_type=1).filter(student=stud).exists()
                disliked = question.action_set.filter(action_type=0).filter(student=stud).exists()
                if request.POST.get('type') == 'question':
                    if request.POST.get('action_type')=='dislike':
                        question.actions(0, stud, disliked, liked)
                    else:
                        question.actions(1, stud, liked, disliked)
                return JsonResponse({'liked': str(liked), 'disliked': str(disliked)})
            
            elif(request.POST['post_type'] == 'comment_vote'):
                question = get_object_or_404(Question,id =request.POST.get("id"))
                student = Student.objects.get(user = request.user)
                # Asagida hem comment_id, hem de question ile axtaririq cunki ola bilsin ki,
                # comment basqa suala aid olsun.
                comment = get_object_or_404(Comment, id = request.POST.get("comment_id"), question = question)
                liked = comment.action_set.filter(action_type = 1).filter(student = student).exists()
                disliked = comment.action_set.filter(action_type=0).filter(student = student).exists()
                if request.POST.get('type') == 'comment':
                    if request.POST.get('action_type')=='dislike':
                        # 0 - downvote dislike
                        comment.actions(0, student, disliked, liked)
                    else:
                        # 1 - upvote like
                        comment.actions(1, student, liked, disliked)
                return JsonResponse({'liked': str(liked), 'disliked': str(disliked)})
    
            elif(request.POST['post_type'] == 'select_answer'):
                student = get_object_or_404(Student, id = request.user.id)
                question = get_object_or_404(Question, id = request.POST.get("question_id"), student = student)
                comment = get_object_or_404(Comment, id = request.POST.get("comment_id"), question = question)
                if (question.answer == comment.id):
                    question.answer = None
                    question.save()
                    fill_green = False
                else:
                    question.answer = comment.id
                    question.save()
                    fill_green = True

                return JsonResponse({'fill_green': fill_green})
    else:
        question.view +=1
        question.save()
    context={
        'comments' : FilterComments(question),
        'question': question,
        'student': Student.objects.get(user = request.user),
    }
    return render(request, 'single-user/page-single-topic.html', context)

@login_required
@picture_required
def faq(request):
    context={
        "faq_list" : FAQ.objects.all().order_by('-updated'),
    }
    return render(request, 'main_page/faq.html', context)

@login_required
@picture_required
def user_activity(request, id):
    template='user-details/user-activity.html' 
    page_template='user-details/user-activity-list.html'
    temp_student = User.objects.get(id = id).student
    activity = sorted(chain(temp_student.question_set.all(), temp_student.comment_set.all()),key=lambda instance: instance.updated)
    context={
        'student' : temp_student,
        'activity' : activity if activity else -1,
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)

@login_required
@picture_required
def user_questions(request, id):
    template='user-details/user-questions.html'
    page_template='user-details/user-question-list.html'
    temp_student = User.objects.get(id = id).student
    context={
        'student' : temp_student,
        'questions' : temp_student.question_set.all().order_by('-updated') if temp_student.question_set.all() else -1,
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)

@login_required
@picture_required
def user_comments(request, id):
    template = 'user-details/user-comments.html'
    page_template = 'user-details/user-comment-list.html'
    temp_student = User.objects.get(id = id).student
    context={
        'student' : temp_student,
        'comments' : temp_student.comment_set.all().order_by('-updated') if temp_student.comment_set.all() else -1,
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)

@login_required
@picture_required
def user_tags(request, id):
    template = 'user-details/user-tags.html' 
    page_template = 'user-details/user-tag-list.html'
    temp_student = User.objects.get(id = id).student
    my_tags = set()
    for question in temp_student.question_set.all():
        for tag in question.tags.all():
            my_tags.add(tag)
    custom_list = [tag.id for tag in my_tags]
    context={
        'student' : temp_student,
        'tags' : Tag.objects.filter(id__in=custom_list).order_by('name') if Tag.objects.filter(id__in=custom_list) else -1,
        'page_template': page_template,
    }
    if request.is_ajax():
        template = page_template
    return render(request, template, context)

@logout_required
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = User.objects.filter(username = username).first()
            person = requests.post('http://157.230.220.111/api/person', data={"email": user.email}, auth=auth).json()
            if not person or dict(person).get('type')!=1:
                messages.error(request, "Sizin emailiniz Pragmatech sistemindən silinmişdir! \
                    Əgər emailinizi dəyişmisinizsə zəhmət olmasa yeni email ilə yenidən qeydiyyatdan keçin", extra_tags='danger')
                return redirect('login')
            user = authenticate(username=username, password=password)
            if user is None:
                messages.error(request, "İstifadəçi adı və ya şifrə düzgün deyil!", extra_tags='danger')
                return redirect('login')
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            login(request, user)
            if request.session.test_cookie_worked():
                    request.session.delete_test_cookie()
            return redirect('student-home')
    else:
        request.session.set_test_cookie()
    return render(request, "auth/login.html", {"form": form})

@logout_required
def register(request):
    form = EmailForm(request.POST or None)
    context = {'form':form}
    if request.method == "POST":
        if form.is_valid():
            # Getting persons data and creating username and random password
            person = dict(requests.post('http://157.230.220.111/api/person', data={"email":form.cleaned_data.get('email')}, auth=auth).json())
            username = person.get('name').lower()+'-'+person.get('surname')[0].lower()+person.get('father_name')[0].lower()
            password = ''.join([random.choice(password_characters) for i in range(12)])

            # Checking users with that username
            old_user = User.objects.filter(username__contains = username).last()
            check = 0
            if old_user:
                old_person = requests.post('http://157.230.220.111/api/person', data={"email":old_user.email}, auth=auth).json()
                # If Person changed email 
                if not old_person:
                    old_user.set_password(password)
                    old_user.email = person.get('email')
                    old_user.save()
                    username = old_user.username
                
                # If Person is new user
                else:
                    if old_user.username[-1].isdigit():
                        username = old_user.username[0:-1] + str(int(old_user.username[-1])+1)
                    else:
                        username+="2"
                    check = 1
            
            # Creating user if it's not already exist
            if not old_user or check == 1:
                user = User.objects.create_user(username, person.get('email'), password)
                user.first_name = person.get('name')
                user.last_name = person.get('surname')
                user.save()
                student = Student(user = user)
                student.save()
                student.add_roles(person.get('roles'))
                if 5 in person.get('roles'):
                    student.add_study_group(person)
                student.save()
            
            # Sending mail to user's email
            html_message = render_to_string('auth/verification.html', {'username': username, 'password': password})
            mail.send_mail(subject = 'PragmatechQA Hesab Təsdiqlənməsi', message = strip_tags(html_message), from_email = 'Pragmatech <soltanov.tarlan04@gmail.com>', recipient_list=[person.get('email')], html_message=html_message)
            messages.success(request, 'Profil yaradıldı və məlumatlar emailinizə göndərildi!')
            return redirect('login')
    return render(request, 'auth/register.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def picture_view(request):
    form =StudentPictureForm(request.POST or None,
                                request.FILES or None,
                                instance=request.user.student)
    if request.method =="POST":
        if form.is_valid():
            form.save()
            return redirect('student-home')
    return render(request, "auth/picture.html", {"form": form})

@login_required
def search(request):
    if request.is_ajax():
        q = request.GET.get('q')
        if q is not None:            
            results = Question.objects.filter(  
            	Q( title__contains = q ) |
                Q( content__contains = q ) ).all()[0:3]       
            return render(request, 'search/results.html', {'results': results})

@login_required
def advanced_search(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        username = request.POST.get('username')
        tags = [tag for tag in request.POST.get('tags').split(",")]
        results = Question.objects.filter(  
            	Q( title__contains = title ) |
                Q( content__contains = title ) )
        if request.POST.get('start'):
            start = datetime.date(*list(map(int, request.POST.get('start').split("-"))))
            if request.POST.get('end'):
                end = datetime.date(*list(map(int, request.POST.get('end').split("-"))))
                results = results.filter( created__range = (start, end) )
            else:
                results = results.filter( created__gte = start )
        if username:
            results = results.filter( student__user__username__contains = username )
        if tags != ['']:
            results = results.filter( tags__name__in = tags )
        context={
            'questions': results,
            'NotResult': "Nəticə tapılmadı",
        }

    template='main_page/home.html'
    page_template='main_page/question_list.html'
    context['page_template'] = page_template
    if request.is_ajax():
        template = page_template
    return render(request, template, context)

def error_404(request, exception):
    return render(request, 'error_pages/error404.html', context={})