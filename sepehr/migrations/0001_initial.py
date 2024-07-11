# Generated by Django 5.0.7 on 2024-07-10 23:24

import django.utils.timezone
import phonenumber_field.modelfields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
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
    ]
