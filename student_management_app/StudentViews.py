from student_management_app.models import AttendanceReport
from student_management_app.models import Attendance, CustomUser
from student_management_app.models import Courses, Subjects
from student_management_app.models import FeedBackStudent
from django.contrib import admin, messages
from student_management_app.models import LeaveReportStudent, Students
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
import datetime

def student_home(request):
    student = Students.objects.get(admin=request.user.id)
    attendence_total = AttendanceReport.objects.filter(student_id=student).count()
    attendence_present = AttendanceReport.objects.filter(student_id=student,status=True).count()
    attendence_absent = AttendanceReport.objects.filter(student_id=student,status=False).count()
    course = Courses.objects.get(id=student.course_id.id) 
    subjects = Subjects.objects.filter(course_id=course).count()
    context={
        "attendence_total":attendence_total,
        "attendence_present":attendence_present,
        "attendence_absent":attendence_absent,
        "subjects":subjects,
    }
    return render(request,"student_template/student_home_template.html",context)

def student_apply_leave(request):
    student_id=Students.objects.get(admin=request.user.id)
    leave = LeaveReportStudent.objects.filter(student_id = student_id)
    context = {
        "leave":leave,
    }
    return render(request,"student_template/student_leave_template.html",context)
    
def student_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Is Not Allowed")
    else:
        user= request.user
        print(user)
        print(request.user.id)
        leave_date = request.POST.get("leave_date")
        leave_end_date=request.POST.get("leave_end_date")
        leave_message = request.POST.get("leave_message")
        student_id=Students.objects.get(admin=request.user.id)
        try:
            # student = Students.objects.get(admin=request.user.id)
            course = Courses.objects.get(id=student_id.course_id.id)
            leave_report = LeaveReportStudent(student_id=student_id,course_id=course,leave_date=leave_date,leave_end_date=leave_end_date,leave_message=leave_message,leave_status=0)
            leave_report.save()
            messages.success(request,"Successfully Applied Leave")
            return HttpResponseRedirect("/student_apply_leave")
        except:
            messages.error(request,"Failed To Applied Leave")
            return HttpResponseRedirect("/student_apply_leave")

def student_feedback(request):
    student = Students.objects.get(admin=request.user.id)
    feedback = FeedBackStudent.objects.filter(student_id=student)
    context = {
        "feedback":feedback,
    }
    return render(request,"student_template/student_feedback.html",context)


def student_feedback_save(request):
    if request.method != 'POST':
        return HttpResponse("Method is Not Allowed")
    else:
        feedback_message = request.POST.get("feedback_message")

        student = Students.objects.get(admin=request.user.id)
        try:
            student = Students.objects.get(admin=request.user.id)
            course = Courses.objects.get(id=student.course_id.id)
            feedback = FeedBackStudent(student_id=student,feedback=feedback_message,course_id=course)
            feedback.save()
            messages.success(request,"Successfully Send Feedback")
            return HttpResponseRedirect("/student_feedback")
        except:
            messages.error(request,"Failed To Send Feedback")
            return HttpResponseRedirect("/student_feedback")


def student_view_attendence(request):
    student =Students.objects.get(admin=request.user.id)
    print(student)
    print(student.course_id)
    course=student.course_id
    print(course)
    subject = Subjects.objects.filter(course_id=course)
    return render(request,"student_template/student_view_attendence.html",{"subject":subject})

def student_view_attendence_save(request):
    subject_id = request.POST.get("subject")
    print(subject_id)
    start_date = request.POST.get("start_date")
    print(start_date)
    end_date = request.POST.get("end_date")
    print(end_date)

    start_data =datetime.datetime.strptime(start_date,"%Y-%m-%d").date()
    end_data = datetime.datetime.strptime(end_date,"%Y-%m-%d").date()
    subject_obj = Subjects.objects.get(id=subject_id)
    user_obj = CustomUser.objects.get(id=request.user.id)
    student_obj=Students.objects.get(admin=user_obj)

    attendence = Attendance.objects.filter(attendance_date__range=(start_data,end_data),subject_id=subject_obj)
    attendence_report = AttendanceReport.objects.filter(attendance_id__in=attendence,student_id=student_obj)
    return render(request,"student_template/student_attendence_details.html",{"attendence_report":attendence_report})
    # print(attendence)
    # for attendence_report in attendence_report:
    #     print("Date: "+str(attendence_report.attendance_id.attendance_date),"Status: " +str(attendence_report.status)) 
    #     print(start_data)
    #     print(end_data)
    #     return HttpResponse("OK")