import os
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from compress_field import ZipFileField
from django.core.exceptions import ValidationError


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="student_profile"
    )
    is_assistant = models.BooleanField(default=False)
    phone_number = PhoneNumberField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Exercise(models.Model):
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard"),
    ]
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=128, blank=False)
    exercise_name = models.CharField(max_length=128, blank=False, unique=True)
    exercise_content = models.TextField(blank=True)
    is_visible = models.BooleanField(default=False)
    java_definition = ZipFileField(upload_to="mycontent/Exercises_CPP/", blank=True)
    cpp_definition = ZipFileField(upload_to="mycontent/Exercises_JAVA/", blank=True)
    weight = models.IntegerField(
        default=1, validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    difficulty_level = models.CharField(
        max_length=6, choices=DIFFICULTY_CHOICES, default="Easy"
    )

    def __str__(self):
        return self.title


def validate_file_size(max_size):
    """
    Returns a validator function that checks if a file's size is under the given max_size.

    :param max_size: Maximum file size in bytes.
    :return: Validator function.
    """

    def validator(value):
        if value.size > max_size:
            raise ValidationError(
                f"File size must be under {max_size / (1024 * 1024)}MB"
            )

    return validator


def solution_file_upload_to(instance, filename):
    return os.path.join(
        "solutionsFile",
        instance.student.user.username,
        instance.exercise.exercise_name,
        instance.language,
        filename,
    )


class Solution(models.Model):
    LANGUAGE = [
        ("cpp", "cpp"),
        ("java", "java"),
    ]
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    solution_file = ZipFileField(
        upload_to=solution_file_upload_to,
        validators=[validate_file_size(1 * 1024 * 1024)],  # 1MB limit
    )
    language = models.CharField(max_length=10, choices=LANGUAGE)

    def __str__(self):
        return f"{self.exercise}_{self.language} + {self.student} + {self.id}"


class Result(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.PROTECT)
    exercise = models.ForeignKey(Exercise, on_delete=models.PROTECT)
    solution = models.OneToOneField(Solution, on_delete=models.PROTECT)
    score = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(0)]
    )
    compile_time = models.DateTimeField()
    error_message = models.CharField(max_length=256)
    exercise_content = models.TextField(blank=True)
    output = models.JSONField()

    def __str__(self):
        return f"{self.exercise} + {self.solution} + {self.student} + {self.id}"
