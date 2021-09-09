from django.contrib.auth.models import AbstractUser
from os import name
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver
from froala_editor.fields import FroalaField
from django.db.models import Q

class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Semester(models.Model):
    id = models.AutoField(primary_key=True)
    semester_name = models.CharField(max_length=20)
    course = models.ForeignKey(Courses,on_delete=models.CASCADE)
    objects = models.Manager()

class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Stuednt"))
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10)


class AdminHOD(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=CASCADE)
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token = models.TextField(default="")
    objects = models.Manager()


class Subjects(models.Model):
    id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)
    semester_id = models.ForeignKey(Semester,on_delete=models.CASCADE,default=1)  
    staff_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=CASCADE)
    gender = models.CharField(max_length=255)
    profile_pic = models.FileField()
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    semester_id = models.ForeignKey(Semester,on_delete=models.CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    fcm_token = models.TextField(default="")
    objects = models.Manager()


class Attendance(models.Model):
    id = models.AutoField(primary_key=True)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    semester_id = models.ForeignKey(Semester,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class AttendanceReport(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    attendance_id = models.ForeignKey(Attendance, on_delete=models.CASCADE)
    semester_id = models.ForeignKey(Semester,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class LeaveReportStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_end_date = models.CharField(max_length=255,default=0)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    course_id = models.ForeignKey(Courses,on_delete=CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class LeaveReportStaff(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.CharField(max_length=255)
    leave_end_date = models.CharField(max_length=255,default=0)
    leave_message = models.TextField()
    leave_status = models.IntegerField(default=0)
    course_id = models.ForeignKey(Courses,on_delete=CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    course_id = models.ForeignKey(Courses,on_delete=CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class FeedBackStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    feedback = models.TextField()
    feedback_reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStudent(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class NotificationStaffs(models.Model):
    id = models.AutoField(primary_key=True)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

class Question(models.Model):
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200)
    option2=models.CharField(max_length=200)
    option3=models.CharField(max_length=200)
    option4=models.CharField(max_length=200)
    answer=models.CharField(max_length=200)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE,default=1)
    staff_id = models.ForeignKey(Staffs,on_delete=models.CASCADE,default=1)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE,default=1)
    subject_id = models.ForeignKey(Subjects,on_delete=models.CASCADE,default=1)

class StudentResult(models.Model):
    id = models.AutoField(primary_key=True)
    semester = models.ForeignKey(Semester,on_delete=models.CASCADE,default=1)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    subject_exam_marks = models.FloatField(default=0)
    subject_assignment_marks = models.FloatField(default=0)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = models.Manager()

class Assignment(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.CharField(max_length=600)
    answer = FroalaField(blank = True, null=True)
    subject_id = models.ForeignKey(Subjects,on_delete=models.CASCADE)
    staff_id = models.ForeignKey(Staffs,on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses,on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = models.Manager()


class AssignmentAnswer(models.Model):
    id=models.AutoField(primary_key=True)
    question_id = models.ForeignKey(Assignment,on_delete=CASCADE,default="")
    answer = FroalaField(blank = True, null=True)
    subject_id = models.ForeignKey(Subjects,on_delete=models.CASCADE, null=True,blank=True)
    course_id = models.ForeignKey(Courses,on_delete=models.CASCADE,null=True,blank=True)
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)
    objects = models.Manager()

class OnlineClassRoom(models.Model):
    id = models.AutoField(primary_key=True)
    room_name = models.CharField(max_length=255)
    room_pwd = models.CharField(max_length=255)
    subject = models.ForeignKey(Subjects, on_delete=models.CASCADE)
    semester_id = models.ForeignKey(Semester,on_delete=models.CASCADE,default=1)
    started_by = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()


class ThreadManager(models.Manager):
    def by_user(self, **kwargs):
        user = kwargs.get('user')
        lookup = Q(first_person=user) | Q(second_person=user)
        qs = self.get_queryset().filter(lookup).distinct()
        return qs


class Thread(models.Model):
    first_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_first_person')
    second_person = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True,related_name='thread_second_person')
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()
    class Meta:
        unique_together = ['first_person', 'second_person']


class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



class AttendanceSampl(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    subject_id = models.ForeignKey(Subjects, on_delete=models.DO_NOTHING)
    attendance_date = models.DateField()
    semester_id = models.ForeignKey(Semester,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()
    period1 = models.CharField(max_length=50)
    period2 = models.CharField(max_length=50)
    period3 = models.CharField(max_length=50)
    period4 = models.CharField(max_length=50)
    period5 = models.CharField(max_length=50)


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            AdminHOD.objects.create(admin=instance)
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance,address="")
        if instance.user_type == 3:
            Students.objects.create(admin=instance,course_id=Courses.objects.get(id=1),semester_id=Semester.objects.get(id=1),profile_pic="",address="",gender="")


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.adminhod.save()
    if instance.user_type == 2:
        instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()
