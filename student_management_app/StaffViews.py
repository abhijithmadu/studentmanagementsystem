from django.db.models.fields import DateTimeField
from datetime import datetime
from student_management_app.models import Assignment, AssignmentAnswer, AttendanceSampl, Courses, CustomUser, NotificationStaffs, OnlineClassRoom, Question, Semester, StudentResult
from student_management_app.models import FeedBackStaffs
from django.contrib import messages
from student_management_app.models import Staffs
from student_management_app.models import LeaveReportStaff
from student_management_app.models import Subjects,Students, Attendance, AttendanceReport
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect, request
import json
from uuid import uuid4  
from django.core import serializers
from django.db import models
from django.urls import reverse
from django.template.loader import render_to_string


def staff_home(request):
    subjects = Subjects.objects.filter(staff_id = request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)
    final_course=[]
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count = Students.objects.filter(course_id__in=final_course).count()

    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()
    staff = Staffs.objects.get(admin=request.user.id)
    leave_count = LeaveReportStaff.objects.filter(staff_id=staff.id,leave_status=1).count()
    subject_count = subjects.count()

    subject_list=[]
    attendance_list=[]
    for subject in subjects:
        attendance_count1=Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance=Students.objects.filter(course_id__in=final_course)
    student_list=[]
    student_list_attendance_present=[]
    student_list_attendance_absent=[]
    for student in students_attendance:
        attendance_present_count=AttendanceReport.objects.filter(status=True,student_id=student.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(status=False,student_id=student.id).count()
        student_list.append(student.admin.username)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)
    context={
        "students_count":students_count,
        "attendance_count":attendance_count,
        "leave_count":leave_count,
        "subject_count":subject_count,
        "subject_list":subject_list,
        "attendance_list":attendance_list,
        "student_list":student_list,
        "present_list":student_list_attendance_present,
        "absent_list":student_list_attendance_absent,

    }
    return render(request,"staff_template/staff_home_template.html",context)


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
    period=request.POST.get("period")
    print("----==========",period)
    attendance_date=str(request.POST.get("attendance_date"))
    print(attendance_date)
    semester=request.POST.get("semester")

    subject_model=Subjects.objects.get(id=subject_id)
    semester_model = Semester.objects.get(id=semester)
    print("sssss",student_ids)
    json_sstudent=json.loads(student_ids)
    print("ssssssssssss",json_sstudent)
    print(json_sstudent,"hellomhsbdhbchjds")

    # try:
    print("inside try")
    attendance=Attendance(subject_id=subject_model,attendance_date=attendance_date,semester_id=semester_model)
    attendance.save()
    print(attendance.attendance_date)
    period1 = '1'
    if AttendanceSampl.objects.filter(attendance_date = attendance_date).exists():
        for stud in json_sstudent:
            print(stud,"hai helllop")
            student=Students.objects.get(admin=stud['id'])
            date_lst = []
            date_lst = attendance_date.split("-")
            attendance_repor=AttendanceSampl.objects.get(student_id=student)
            attendance_repor.save()
            if stud['status'] == 0:
                if period == 'period1':
                    attendance_repor.period1 = '0'
                    attendance_repor.save()
                elif period == 'period2':
                    attendance_repor.period2 = '0'
                    attendance_repor.save()
                elif period == 'period3':
                    attendance_repor.period3 = '0'
                    attendance_repor.save()
                elif period == 'period4':
                    attendance_repor.period4 = '0'
                    attendance_repor.save()
                elif period == 'period5':
                    attendance_repor.period5 = '0'
                    attendance_repor.save()
            elif stud['status'] == 1:
                if period == 'period1':
                    attendance_repor.period1 = '1'
                    attendance_repor.save()
                elif period == 'period2':
                    attendance_repor.period2 = '1'
                    attendance_repor.save()
                elif period == 'period3':
                    attendance_repor.period3 = '1'
                    attendance_repor.save()
                elif period == 'period4':
                    attendance_repor.period4 = '1'
                    attendance_repor.save()
                elif period == 'period5':
                    attendance_repor.period5 = '1'
                    attendance_repor.save()
    else:
        for stud in json_sstudent:
            print(stud,"hai helllop")
            student=Students.objects.get(admin=stud['id'])
            date_lst = []
            date_lst = attendance_date.split("-")

            attendance_repor=AttendanceSampl(student_id=student, subject_id=subject_model,attendance_date=attendance_date,semester_id=semester_model,period1='2',period2='2',period3='2',period4='2',period5='2')
            attendance_repor.save()
            if stud['status'] == 0:
                if period == 'period1':
                    attendance_repor.period1 = '0'
                    attendance_repor.save()
                elif period == 'period2':
                    attendance_repor.period2 = '0'
                    attendance_repor.save()
                elif period == 'period3':
                    attendance_repor.period3 = '0'
                    attendance_repor.save()
                elif period == 'period4':
                    attendance_repor.period4 = '0'
                    attendance_repor.save()
                elif period == 'period5':
                    attendance_repor.period5 = '0'
                    attendance_repor.save()
            elif stud['status'] == 1:
                if period == 'period1':
                    attendance_repor.period1 = '1'
                    attendance_repor.save()
                elif period == 'period2':
                    attendance_repor.period2 = '1'
                    attendance_repor.save()
                elif period == 'period3':
                    attendance_repor.period3 = '1'
                    attendance_repor.save()
                elif period == 'period4':
                    attendance_repor.period4 = '1'
                    attendance_repor.save()
                elif period == 'period5':
                    attendance_repor.period5 = '1'
                    attendance_repor.save()
        

        # attendance_report=AttendanceReport(student_id=student.id,attendance_id=attendance,status=stud['status'],semester_id=semester_model)
        # attendance_report.save()
    # for stud in json_sstudent:
    #     print(stud,"hai helllop")
    #     student=Students.objects.get(admin=stud['id'])
        
    return HttpResponse("OK")
    # except:
    #     print("inside exc")
    #     return HttpResponse("ERR")


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
        user = CustomUser.objects.get(id = request.user.id)
        staff = Staffs.objects.get(admin = user)
        print(staff)
        semester = request.GET['semester']
        semester = Semester.objects.get(id=semester)
        print(semester)
        subject = Subjects.objects.filter(semester_id = semester,staff_id=staff.admin.id)
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
            # if password!=None and password!="":
            #     customuser.set_password(password)
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


def start_live_classroom(request):
    staff = Staffs.objects.get(admin=request.user.id)
    semester = Semester.objects.filter(course = staff.course_id.id)
    print(semester,"online class")
    subjects=Subjects.objects.filter(staff_id=request.user.id)
    print(subjects,"online")
    context = {
        "subjects":subjects,
        "semester":semester

    }
    return render(request,"staff_template/start_live_classroom.html",context)

def start_live_classroom_process(request):
    semester_id=request.POST.get("semester_id")
    subject=request.POST.get("subject")

    subject_obj=Subjects.objects.get(id=subject)
    semester=Semester.objects.get(id=semester_id)
    checks=OnlineClassRoom.objects.filter(subject=subject_obj,semester_id=semester,is_active=True).exists()
    if checks:
        data=OnlineClassRoom.objects.get(subject=subject_obj,semester_id=semester,is_active=True)
        room_pwd=data.room_pwd
        roomname=data.room_name
    else:
        room_pwd=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        roomname=datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())
        staff_obj=Staffs.objects.get(admin=request.user.id)
        onlineClass=OnlineClassRoom(room_name=roomname,room_pwd=room_pwd,subject=subject_obj,semester_id=semester,started_by=staff_obj,is_active=True)
        onlineClass.save()

    return render(request,"staff_template/live_class_room_start.html",{"username":request.user.username,"password":room_pwd,"roomid":roomname,"subject":subject_obj.subject_name,"semester":semester})

def returnHtmlWidget(request):
    return render(request,"widget.html")

def staff_add_result(request):
    staff = Staffs.objects.get(admin = request.user.id)
    print(staff)
    course = Courses.objects.get(id=staff.course_id.id)
    print(course)
    semester=Semester.objects.filter(course_id=course)
    print(semester) 
    context={
        "semester":semester,
    }
    return render(request,"staff_template/staff_add_result.html",context)

def save_student_result(request):
    if request.method!='POST':
        return HttpResponseRedirect('staff_add_result')
    student_admin_id=request.POST.get('student_list')
    assignment_marks=request.POST.get('assignment_marks')
    semester = request.POST.get('semester_id')
    print(semester)
    exam_marks=request.POST.get('exam_marks')
    subject_id=request.POST.get('subject')

    student_obj=Students.objects.get(admin=student_admin_id)
    subject_obj=Subjects.objects.get(id=subject_id)
    semester_obj=Semester.objects.get(id=semester)

    try:
        check_exist=StudentResult.objects.filter(subject_id=subject_obj,student_id=student_obj,semester=semester_obj).exists()
        if check_exist:
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj,semester=semester_obj)
            result.subject_assignment_marks=assignment_marks
            result.subject_exam_marks=exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("staff_add_result"))
        else:
            result=StudentResult(student_id=student_obj,semester=semester_obj,subject_id=subject_obj,subject_exam_marks=exam_marks,subject_assignment_marks=assignment_marks)
            result.save()
            messages.success(request, "Successfully Added Result")
            return HttpResponseRedirect(reverse("staff_add_result"))
    except:
        messages.error(request, "Failed to Add Result")
        return HttpResponseRedirect(reverse("staff_add_result"))

def timetablesem(request):
    staff = Staffs.objects.get(admin=request.user.id)
    course = Courses.objects.get(id=staff.course_id.id)
    semester = Semester.objects.filter(course_id=course)
    context = {
        "semester":semester,
    }
    return render(request,"staff_template/timetablesem.html",context)

def time_table_staff(request):
    semester_obj = request.POST.get('semester_id')

    try:
        subject =Subjects.objects.filter(semester_id=semester_obj)
        print(subject,"subject")
        Monday = [subject[1].subject_name,subject[3].subject_name,subject[2].subject_name,subject[0].subject_name,subject[4].subject_name]
        Tuesday = [subject[0].subject_name,subject[0].subject_name,subject[4].subject_name,subject[1].subject_name,subject[3].subject_name]
        Wednesday = [subject[3].subject_name,subject[4].subject_name,subject[1].subject_name,subject[2].subject_name,subject[1].subject_name]
        Thursday = [subject[2].subject_name,subject[0].subject_name,subject[1].subject_name,subject[3].subject_name,subject[2].subject_name]
        Friday = [subject[4].subject_name,subject[3].subject_name,subject[2].subject_name,subject[4].subject_name,subject[4].subject_name]
        Saturday = [subject[0].subject_name,subject[4].subject_name,subject[3].subject_name,subject[0].subject_name,subject[0].subject_name]
        context={
            "Monday":Monday,
            "Tuesday":Tuesday,
            "Wednesday":Wednesday,
            "Thursday":Thursday,
            "Friday":Friday,
            "Saturday":Saturday,
        }
        print(Monday,Tuesday,Wednesday,Thursday,Friday,Saturday)

        return render(request,"staff_template/timetableviewstaff.html",context)
    except:
        return render(request,"staff_template/timetableviewstaff.html")

















        






