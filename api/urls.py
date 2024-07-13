from django.contrib import admin
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^student-login/login/$", views.student_login, name="student_login"),
    re_path(r"^student-signup/signup/$", views.student_signup, name="student_signup"),
    re_path(r"^exercises/$", views.exercise_list, name="exercise-list"),
    re_path(r"^exercises/(?P<pk>\d+)/$", views.exercise_detail, name="exercise-detail"),
    re_path(r"^upload-solution/$", views.upload_solution, name="upload-solution"),
]
