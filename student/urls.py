from django.urls import path
from student import views

urlpatterns = [
    path('', views.home, name='student-home'),
    path('about/', views.about, name='student-about'),
    path('rules/', views.rules, name='student-rules'),
    path('create-topic/', views.page_create_topic, name='student_page_create_topic'),
    path('question/<slug>', views.question_detail, name='single_topic'),
    path('question/edit/<slug>', views.question_edit, name='single_topic_edit'),
    path('user/<int:id>', views.user_activity, name='user_activity'),
    path('user/<int:id>/questions', views.user_questions, name='user_questions'),
    path('user/<int:id>/comments', views.user_comments, name='user_comments'),
    path('user/<int:id>/tags', views.user_tags, name='user_tags'),
    path('tags/', views.tags, name='tags'),
    path('tag/<slug:slug>', views.tag_info, name='single_tag'),
    path('faq', views.faq, name='faq'),
    path('login/', views.login_view, name='login'),
    path('user/picture', views.picture_view, name='user_picture'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
]