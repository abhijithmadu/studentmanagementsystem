# Generated by Django 3.2.5 on 2021-07-24 05:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='session_start_end',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='students',
            name='session_start_year',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
