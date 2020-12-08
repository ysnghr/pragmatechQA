from django.http import JsonResponse, QueryDict
from student.models import *
from student.forms import QuestionForm, QuestionImageForm, CommentForm, CommentImageForm
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from datetime import datetime
from student.utils import FilterComments
from taggit.models import Tag
from itertools import chain


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

def about(request):
    return render(request, 'main_page/about.html')

def rules(request):
    return render(request, 'main_page/rules.html')

@login_required
def page_create_topic(request):
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST or None)
        if form.is_valid():
            new_question = form.save()  
            student = Student.objects.get(user = request.user)
            new_question.student = student
            new_question.save()
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
                print(question.answer )
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
    
def faq(request):
    context={
        "faq_list" : FAQ.objects.all().order_by('-updated'),
    }
    return render(request, 'main_page/faq.html', context)

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
    from itertools import chain