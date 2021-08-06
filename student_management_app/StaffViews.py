from student_management_app.models import Courses, CustomUser, Question, Semester
from student_management_app.models import FeedBackStaffs
from django.contrib import messages
from student_management_app.models import Staffs
from student_management_app.models import LeaveReportStaff
from student_management_app.models import SessionYearModel,Subjects,Students, Attendance, AttendanceReport
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, request
import json
from django.core import serializers
from django.db import models


def staff_home(request):
    return render(request,"staff_template/staff_home_template.html")


def staff_take_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_years=SessionYearModel.objects.all()
    context={
        "subjects":subjects,
        "session_years":session_years
        }
    return render(request,"staff_template/staff_take_attendance.html",context)

@csrf_exempt
def get_students(request):
    subject_id=request.POST.get("subject")
    session_year=request.POST.get("session_year")

    subject=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.objects.get(id=session_year)
    students=Students.objects.filter(course_id=subject.course_id,session_year_id=session_model)
    list_data=[]

    for student in students:
        data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

@csrf_exempt
def save_attendance_data(request):
    student_ids=request.POST.get("student_ids")
    subject_id=request.POST.get("subject_id")
    attendance_date=str(request.POST.get("attendance_date"))
    print(attendance_date)
    session_year_id=request.POST.get("session_year_id")

    subject_model=Subjects.objects.get(id=subject_id)
    session_model=SessionYearModel.objects.get(id=session_year_id)
    json_sstudent=json.loads(student_ids)

    try:
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,session_year_id=session_model)
        attendance.save()
        print(attendance.attendance_date)

        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'])
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def staff_update_attendance(request):
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    session_year_id=SessionYearModel.objects.all()
    return render(request,"staff_template/staff_update_attendance.html",{"subjects":subjects,"session_year_id":session_year_id})


@csrf_exempt
def get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.objects.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)


@csrf_exempt
def get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)


@csrf_exempt
def save_updateattendance_data(request):
    student_ids=request.POST.get("student_ids")
    attendance_date=request.POST.get("attendance_date")
    print("this is for date information",attendance_date)
    attendance=Attendance.objects.get(id=attendance_date)

    json_sstudent=json.loads(student_ids)

    try:
        for stud in json_sstudent:
             student=Students.objects.get(admin=stud['id'])
             attendance_report=AttendanceReport.objects.get(student_id=student,attendance_id=attendance)
             attendance_report.status=stud['status']
             attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")

def staff_apply_leave(request):
    staff= Staffs.objects.get(admin=request.user.id)
    leave_report = LeaveReportStaff.objects.filter(staff_id=staff)
    
    context = {
        "leave_report":leave_report,
    }
    return render(request,"staff_template/staff_apply_leave.html",context)   


def staff_apply_leave_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        leave_date = request.POST.get("leave_date")
        leave_message = request.POST.get("leave_message")
        print(request.user.id)
       
        try:
            staff= Staffs.objects.get(admin=request.user.id)
            course = Courses.objects.get(id=staff.course_id.id)
            leave_report = LeaveReportStaff(staff_id=staff,leave_date=leave_date,course_id=course,leave_message=leave_message,leave_status=0)
            leave_report.save()
            messages.success(request,"Successfully Applied Leave")
            return HttpResponseRedirect("/staff_apply_leave")
        except:
            messages.error(request,"Failed To Apply Leave")
            return HttpResponseRedirect("/staff_apply_leave")

def staff_feedback(request):
    staff = Staffs.objects.get(admin=request.user.id)
    feedback = FeedBackStaffs.objects.filter(staff_id=staff)
    context = {
        "feedback":feedback,
    }
    return render(request,"staff_template/staff_feedback.html",context)

def staff_feedback_save(request):
    if request.method != 'POST':
        HttpResponse("Method Norequestt Allowed")
    else:
        feedback_message = request.POST.get("feedback_message")
        staff = Staffs.objects.get(admin=request.user.id)
        print(request.user.id)
        feedback= FeedBackStaffs(staff_id=staff,feedback=feedback_message)
        feedback.save()
        messages.success(request,"Successfully send message")
        return HttpResponseRedirect("/staff_feedback")

def add_question(request):
   
    # staff = CustomUser.objects.get(id=request.user.id)
    # print(staff)
    # admin = Staffs.objects.get(admin = staff)
    # semester = Semester.objects.filter(course = admin.course_id.id)
    # subjects = Subjects.objects.filter(staff_id = staff)
    # print(subjects)
    # context = {
    #     "subjects":subjects,
    #     "semester":semester,
    # }
    admin = Staffs.objects.get(admin = request.user.id)
    print(admin)
    semester = Semester.objects.filter(course = admin.course_id.id)
    subject = Subjects.objects.filter(semester_id = semester)
    print(semester)
    context = {
        "semester":semester,
        # "subject":subject
    }
    return render(request,"staff_template/add_question_template.html",context)

def fetch_subject(request):
    if request.method == 'GET':
        semester = request.GET['semester']
        semester = Semester.objects.get(id=semester)
        subject = Subjects.objects.filter(semester_id = semester)
        print(subject,"subject")
        sub = subject.values()
    return JsonResponse(list(sub),safe=False)

def add_question_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        semester = request.POST.get("semester_id")
        subject = request.POST.get("subject")
        question = request.POST.get("add_question")
        option1 = request.POST.get("option1")
        option2 = request.POST.get("option2")
        option3 = request.POST.get("option3")
        option4 = request.POST.get("option4")
        answer = request.POST.get("answer")

        




        






