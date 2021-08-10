# Generated by Django 3.2.5 on 2021-08-09 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0015_assignmentanswer_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assignmentanswer',
            old_name='question',
            new_name='question_id',
        ),
        migrations.AlterField(
            model_name='assignmentanswer',
            name='course_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.courses'),
        ),
        migrations.AlterField(
            model_name='assignmentanswer',
            name='subject_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student_management_app.subjects'),
        ),
    ]