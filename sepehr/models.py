from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from compress_field import ZipFileField


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=128, blank=False, unique=True)
    password = models.CharField(max_length=128)
    firstName = models.CharField(max_length=128)
    lastName = models.CharField(max_length=128)
    email = models.EmailField(blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_assistant = models.BooleanField(default=False)
    phone = PhoneNumberField(null=False, blank=False, unique=True)

    def __str__(self):
        return self.username


class Exercise(models.Model):
    title = models.CharField(max_length=128, blank=False, unique=True)
    exercise_name = models.CharField(max_length=128, blank=False, unique=True)
    exercise_content = models.TextField(blank=True)
    is_visible = models.BooleanField(default=False)
    java_definition = ZipFileField(upload_to="mycontent/", blank=True)
    cpp_definition = ZipFileField(upload_to="mycontent/", blank=True)
    weight = models.IntegerField(default=1)


class Solution(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    exercise = models.OneToOneField(
        Exercise, on_delete=models.CASCADE, primary_key=True
    )
