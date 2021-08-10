# Generated by Django 3.2.5 on 2021-08-09 12:53

from django.db import migrations, models
import django.db.models.deletion
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0013_alter_assignment_answer'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssignmentAnswer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('answer', froala_editor.fields.FroalaField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('course_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.courses')),
                ('student_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students')),
                ('subject_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student_management_app.subjects')),
            ],
        ),
    ]