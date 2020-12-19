from django.urls import path
from student import views
from django.contrib.auth import views as auth_views
from student.forms import EmailValidationOnForgotPassword


urlpatterns = [
    path('', views.home, name='student-home'),
    path('about/', views.about, name='student-about'),
    path('rules/', views.rules, name='student-rules'),
    path('create-topic/', views.page_create_topic, name='student_page_create_topic'),
    path('question/<slug>', views.question_detail, name='single_topic'),
    path('question/edit/<slug>', views.question_edit, name='single_topic_edit'),
    path('question/delete/<slug>', views.question_delete, name='single_topic_delete'),
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
    path('search', views.search, name='search'),
    path('search/advanced', views.advanced_search, name='advanced_search'),
    path('password/reset', auth_views.PasswordResetView.as_view(template_name = "auth/reset_password.html", form_class=EmailValidationOnForgotPassword, html_email_template_name='registration/password_reset_html_email.html'), name ='reset_password'),
    path('password/reset/sent', auth_views.PasswordResetDoneView.as_view(template_name = "auth/password_reset_sent.html"), name ='password_reset_done'),
    path('password/reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name = "auth/password_reset_form.html"), name ='password_reset_confirm'),
    path('password/reset/complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "auth/password_reset_done.html"), name ='password_reset_complete'),
    path('password/change', views.change_password, name='change_password'),
]
