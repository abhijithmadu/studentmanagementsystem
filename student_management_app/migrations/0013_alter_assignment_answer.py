# Generated by Django 3.2.5 on 2021-08-09 10:23

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0012_remove_assignment_student_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='answer',
            field=froala_editor.fields.FroalaField(blank=True, null=True),
        ),
    ]
