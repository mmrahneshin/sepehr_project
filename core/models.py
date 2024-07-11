from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from compress_field import ZipFileField
import uuid


class Student(models.Model):
    username = models.CharField(
        primary_key=True, max_length=128, blank=False, unique=True
    )
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
    exercise_name = models.CharField(
        primary_key=True, max_length=128, blank=False, unique=True
    )
    exercise_content = models.TextField(blank=True)
    is_visible = models.BooleanField(default=False)
    java_definition = ZipFileField(upload_to="mycontent/", blank=True)
    cpp_definition = ZipFileField(upload_to="mycontent/", blank=True)
    weight = models.IntegerField(default=1)

    def __str__(self):
        return self.exercise_name


class Solution(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.OneToOneField(Student, on_delete=models.PROTECT)
    exercise = models.OneToOneField(Exercise, on_delete=models.PROTECT)
    solution_file = ZipFileField(upload_to="mycontent/")

    def __str__(self):
        return f"{self.exercise} + {self.student} + {self.id}"


class Result(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    student = models.OneToOneField(Student, on_delete=models.PROTECT)
    exercise = models.OneToOneField(Exercise, on_delete=models.PROTECT)
    solution = models.OneToOneField(
        Solution, primary_key=True, on_delete=models.PROTECT
    )
    score = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    compile_time = models.DateTimeField()
    error_message = models.CharField(max_length=256)
    exercise_content = models.TextField(blank=True)
    output = models.JSONField()

    def __str__(self):
        return f"{self.exercise} + {self.solution} + {self.student} + {self.id}"