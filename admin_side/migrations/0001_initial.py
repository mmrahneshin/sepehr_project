# Generated by Django 5.0.7 on 2024-07-11 17:23

import compress_field.models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, unique=True)),
                ('exercise_name', models.CharField(max_length=128, unique=True)),
                ('exercise_content', models.TextField(blank=True)),
                ('is_visible', models.BooleanField(default=False)),
                ('java_definition', compress_field.models.ZipFileField(blank=True, upload_to='mycontent/')),
                ('cpp_definition', compress_field.models.ZipFileField(blank=True, upload_to='mycontent/')),
                ('weight', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=128, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('firstName', models.CharField(max_length=128)),
                ('lastName', models.CharField(max_length=128)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_assistant', models.BooleanField(default=False)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('exercise', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='admin_side.exercise')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='admin_side.student')),
            ],
        ),
    ]
