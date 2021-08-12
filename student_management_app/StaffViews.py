from student_management_app.models import Assignment, AssignmentAnswer, Courses, CustomUser, NotificationStaffs, Question, Semester
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
from django.urls import reverse
from django.template.loader import render_to_string


def staff_home(request):
    return render(request,"staff_template/staff_home_template.html")


def staff_take_attendance(request):
    admin = Staffs.objects.get(admin = request.user.id)
    semester = Semester.objects.filter(course = admin.course_id.id)
    context={
       "semester":semester 
       
        }
    return render(request,"staff_template/staff_take_attendance.html",context)

@csrf_exempt
def get_students(request):
    semester_id=request.POST.get("semester")
    semseter = Semester.objects.get(id=semester_id)
    students=Students.objects.filter(semester_id=semseter)
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
    semester=request.POST.get("semester")

    subject_model=Subjects.objects.get(id=subject_id)
    semester_model = Semester.objects.get(id=semester)
    json_sstudent=json.loads(student_ids)
    print(json_sstudent,"hellomhsbdhbchjds")

    try:
        print("inside try")
        attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,semester_id=semester_model)
        attendance.save()
        print(attendance.attendance_date)

        for stud in json_sstudent:
            print(stud,"hai helllop")
            student=Students.objects.get(admin=stud['id'])
            attendance_report=AttendanceReport(student_id=student,attendance_id=attendance,status=stud['status'],semester_id=semester_model)
            attendance_report.save()
        return HttpResponse("OK")
    except:
        print("inside exc")
        return HttpResponse("ERR")


def staff_update_attendance(request):
    admin = Staffs.objects.get(admin = request.user.id)
    semester = Semester.objects.filter(course = admin.course_id.id)
    context={
        "semester":semester,
    }
    return render(request,"staff_template/staff_update_attendance.html",context)


@csrf_exempt
def get_attendance_dates(request):
    subject=request.POST.get("subject")
    semester = request.POST.get("semester")
    subject_obj=Subjects.objects.get(id=subject)
    semester=Semester.objects.get(id=semester)
    attendance=Attendance.objects.filter(subject_id=subject_obj,semester_id=semester)
    attendance_obj=[]
    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"semester_id":attendance_single.semester_id.id}
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
        leave_end_date=request.POST.get("leave_end_date")
        leave_message = request.POST.get("leave_message")
        print(request.user.id)
       
        try:
            staff= Staffs.objects.get(admin=request.user.id)
            course = Courses.objects.get(id=staff.course_id.id)
            leave_report = LeaveReportStaff(staff_id=staff,leave_date=leave_date,leave_end_date=leave_end_date,course_id=course,leave_message=leave_message,leave_status=0)
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

def add_assignments(request):
    admin = Staffs.objects.get(admin=request.user.id)
    semester = Semester.objects.filter(course = admin.course_id.id)
    subject = Subjects.objects.filter(semester_id=semester)
    context = {
        "semester":semester,
    }
    return render(request,"staff_template/add_assignment.html",context)

def add_assigenment_save(request):
    if request.method != 'POST':
        HttpResponse("Method Norequestt Allowed")
    else:
        semester = request.POST.get("semester_id")
        subject = request.POST.get("subject")
        question = request.POST.get("add_question")
        try:
            staff = Staffs.objects.get(admin=request.user.id)
            course = Courses.objects.get(id = staff.course_id.id)
            subject_obj = Subjects.objects.get(id=subject)
            assignment = Assignment(question=question)
            assignment.staff_id = staff
            assignment.semester_id = semester
            assignment.course_id=course
            assignment.subject_id = subject_obj
            assignment.save()
            messages.success(request,"Successfully Added Questions")
            return HttpResponseRedirect("/add_assignments")
        except:
            messages.error(request,"Failed To Added Questions")
            return HttpResponseRedirect("/add_assignments")

def add_question(request):
    admin = Staffs.objects.get(admin = request.user.id)
    print(admin)
    semester = Semester.objects.filter(course = admin.course_id.id)
    subject = Subjects.objects.filter(semester_id = semester)
    print(semester)
    context = {
        "semester":semester,
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
        print(subject,"this is for testing")
        question = request.POST.get("add_question")
        option1 = request.POST.get("option1")
        option2 = request.POST.get("option2")
        option3 = request.POST.get("option3")
        option4 = request.POST.get("option4")
        mark = request.POST.get("mark")
        ans = request.POST.get("answer")

        if ans == 'option1':
            answer = option1
        elif ans == 'option2':
            answer = option2
        elif ans == 'option3':
            answer = option3
        elif ans == 'option4':
            answer = option4


        staff = Staffs.objects.get(admin=request.user.id)
        course = Courses.objects.get(id = staff.course_id.id)
        subject_obj = Subjects.objects.get(id=subject)
        print(semester)
        questions_models = Question(question=question,option1=option1,option2=option2,option3=option3,option4=option4,answer=answer,marks=mark)
        questions_models.semester_id = semester
        questions_models.course_id=course
        questions_models.subject_id = subject_obj
        questions_models.save()
        messages.success(request,"Successfully Added Questions")
        return HttpResponseRedirect("/add_question")

def staff_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    staff = Staffs.objects.get(admin = user)
    return render(request,"staff_template/staff_profile.html",{"user":user,"staff":staff})

def staff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("staff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            staff=Staffs.objects.get(admin=customuser.id)
            staff.address=address
            staff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("staff_profile"))
    
@csrf_exempt
def staff_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        staff=Staffs.objects.get(admin=request.user.id)
        staff.fcm_token=token
        staff.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def staff_all_notification(request):
    staff=Staffs.objects.get(admin=request.user.id)
    notifications=NotificationStaffs.objects.filter(staff_id=staff.id)
    return render(request,"staff_template/all_notification.html",{"notifications":notifications})


def assignment_check(request):
    staff = Staffs.objects.get(admin = request.user.id)
    course_id = Courses.objects.get(id=staff.course_id.id)
    semester = Semester.objects.filter(course=course_id)
    context = {
        "semester":semester,
    }
    return render(request,"staff_template/assignment_view.html",context)

@csrf_exempt
def get_students_assignment(request):
    semester=request.POST.get("semester")
    semester_model=Semester.objects.get(id=semester)
    students=Students.objects.filter(semester_id=semester_model)
    context = {
        "students":students,
    }
    print(students,"hai he;llooooooooo")
    data = render_to_string("staff_template/assignment_student_details.html",context)
    return JsonResponse({"key":data})
    # list_data=[]

    # for student in students:
    #     data_small={"id":student.admin.id,"name":student.admin.first_name+" "+student.admin.last_name}
    #     list_data.append(data_small)
    # return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

def assignment_subejct(request,id,pk):
    # staff = Staffs.objects.get(admin = request.user.id)
    # course_id = Courses.objects.get(id = staff.course_id.id)
    student = Students.objects.get(id=pk)
    print(student)
    semester = Semester.objects.get(id=id)
    subject = Subjects.objects.filter(semester_id = semester)
    print(semester)
    print(subject,"subject")
    context = {
        "student":student,
        "subject":subject
    }
    return render(request,"staff_template/assignment_subject.html",context)

def staff_assignment_answer(request,id,pk):
    # student = Students.objects.get(id=id)
    subject = Subjects.objects.get(id=pk)
    print(subject)
    # answer = AssignmentAnswer.objects.filter(student_id=id)
    assign_ans = AssignmentAnswer.objects.filter(student_id=id,subject_id=subject)
   

    #question = Assignment.objects.filter(id=answer.question_id)
    # for i in answer:
    #     print(answer,"athif")
    #     print(i.question_id,"singam abhi")
    #     print(i.answer,"thakkudu")
    # ques_lis = []

    # for i in answer:
    #     ques_lis.append(i.question_id)
    # print(ques_lis)
    
  
    context={
        
        "answer":assign_ans, 
    }
    return render(request,"staff_template/assignement_answer.html",context)
   
















        






