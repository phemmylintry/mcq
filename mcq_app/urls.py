from django.contrib import admin
from django.urls import path, include, re_path
from . import views

app_name = 'mcq_app'

urlpatterns = [
    path('quiz/', views.quiz, name='quiz'),
    path('register/', views.register, name='register'),
    re_path('submission_result/(?P<attempted_question_pk>\d+)/', views.submission_result, name='submission_result'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]