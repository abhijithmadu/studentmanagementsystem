# Generated by Django 3.2.5 on 2021-08-09 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student_management_app', '0010_assignment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='assignment',
            name='student_id',
            field=models.ForeignKey(default=' ', on_delete=django.db.models.deletion.CASCADE, to='student_management_app.students'),
        ),
    ]