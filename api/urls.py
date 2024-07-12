from django.contrib import admin
from django.urls import re_path
from . import views

urlpatterns = [
    re_path("student-login/login/", views.student_login, name="student_login"),
    re_path("student-signup/signup/", views.student_signup, name="student_signup"),
    re_path("exercises/", views.exercise_list, name="exercise-list"),
]
