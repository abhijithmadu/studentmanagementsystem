from student_management_app.form import AssignementForm
from django.views.decorators.csrf import csrf_exempt
from student_management_app.models import Assignment, AssignmentAnswer, AttendanceReport, AttendanceSampl, NotificationStudent, OnlineClassRoom, Question, Semester, Staffs, StudentResult, Thread
from student_management_app.models import Attendance, CustomUser
from student_management_app.models import Courses, Subjects
from student_management_app.models import FeedBackStudent
from django.contrib import admin, messages
from student_management_app.models import LeaveReportStudent, Students
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
import datetime
from django.core.paginator import EmptyPage, InvalidPage, Paginator

def student_home(request):
    student = Students.objects.get(admin=request.user.id)
    attendence_total = AttendanceReport.objects.filter(student_id=student).count()
    attendence_present = AttendanceReport.objects.filter(student_id=student,status=True).count()
    attendence_absent = AttendanceReport.objects.filter(student_id=student,status=False).count()
    course = Courses.objects.get(id=student.course_id.id) 
    semseter = Semester.objects.get(id=student.semester_id.id)
    subjects = Subjects.objects.filter(semester_id=semseter).count()
    subjects_data = Subjects.objects.filter(semester_id=semseter)
    class_room=OnlineClassRoom.objects.filter(subject__in=subjects_data,is_active=True,semester_id=semseter)


    # staff = Staffs.objects.filter(course_id=course.id)
    # print(staff)
    # for stf in staff:
    #     try:
    #         Thread.objects.filter(first_person=stf.admin,second_person=request.user).exists()
    #         print("exist",request.user,stf.admin)
    #         pass

    #     except:
    #         print("dont exist")
    #         thread = Thread(first_person=stf.admin,second_person=request.user)
    #         thread.save()

    subject_name = []
    data_present = []
    data_absent = []
    subject_data = Subjects.objects.filter(semester_id=student.semester_id)
    for subject in subject_data:
        attendence = Attendance.objects.filter(subject_id=subject.id)
        attendence_present_count = AttendanceReport.objects.filter(attendance_id__in=attendence,status=True,student_id=student.id).count()
        attendence_absent_count = AttendanceReport.objects.filter(attendance_id__in=attendence,status=False,student_id=student.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendence_present_count)
        data_absent.append(attendence_absent_count)
    context={
        "attendence_total":attendence_total,
        "attendence_present":attendence_present,
        "attendence_absent":attendence_absent,
        "subjects":subjects,
        "data_name":subject_name,
        "data1":data_present,
        "data2":data_absent,
        "class_room":class_room,
        "student":student,

    }
    return render(request,"student_template/student_home_template.html",context)

def join_class_room(request,subject_id,semester_id):
    semester =Semester.objects.get(id=semester_id)
    subjects=Subjects.objects.filter(id=subject_id)
    if subjects.exists():
        session=Semester.objects.filter(id=semester.id)
        if session.exists():
            subject_obj=Subjects.objects.get(id=subject_id)
            course=Courses.objects.get(id=subject_obj.course_id.id)
            check_course=Students.objects.filter(admin=request.user.id,course_id=course.id)
            if check_course.exists():
                session_check=Students.objects.filter(admin=request.user.id,semester_id=semester.id)
                if session_check.exists():
                    onlineclass=OnlineClassRoom.objects.get(semester_id=semester_id,subject=subject_id)
                    return render(request,"student_template/join_class_room_start.html",{"username":request.user.username,"password":onlineclass.room_pwd,"roomid":onlineclass.room_name})

                else:
                    return HttpResponse("This Online Session is Not For You")
            else:
                return HttpResponse("This Subject is Not For You")
        else:
            return HttpResponse("Semester Not found")
    else:
        return HttpResponse("Subject Not Found")


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

    attendence = Attendance.objects.filter(attendance_date=(start_data,end_data),subject_id=subject_obj)
    attendence_report = AttendanceReport.objects.filter(attendance_id__in=attendence,student_id=student_obj)
    return render(request,"student_template/student_attendence_details.html",{"attendence_report":attendence_report})
    # print(attendence)
    # for attendence_report in attendence_report:
    #     print("Date: "+str(attendence_report.attendance_id.attendance_date),"Status: " +str(attendence_report.status)) 
    #     print(start_data)
    #     print(end_data)
    #     return HttpResponse("OK")

# def attendence_view(request):
#     return render(request,"student_template/student_attendance_view.html")

# def student_view_attendance_post(request):
#     date = request.POST.get("date")
#     print(date)
#     date_lst = []
#     date_lst = date.split("-")
#     print(date_lst)

#     # data =datetime.datetime.strptime(date,"%Y-%m-%d").date()
#     # print(data)
#     student =Students.objects.get(admin=request.user.id)
#     semester = Semester.objects.get(id = student.semester_id.id)
#     # subject = Subjects.objects.filter(semester_id=semester.id)
#     print(semester)
#     attendence = Attendance.objects.filter(attendance_date__month=date_lst[1],semester_id=semester)
#     print(attendence)
#     attendence_report = AttendanceReport.objects.filter(attendance_id__in=attendence,student_id=student)
#     print(attendence_report)
#     attendence_sample = AttendanceSampl.objects.filter(attendance_date__month=date_lst[1],student_id=student)
#     print("sampleeeeeeeeeeeeeee",attendence_sample)
#     context = {
#         "attendence_report":attendence_report,
#         "attendence_sample":attendence_sample,
#     }
#     return render(request,"student_template/student_attendance_post.html",context)

def attendence_view(request):
    return render(request,"student_template/student_attendance_view.html")

def student_view_attendance_post(request):
    date = request.POST.get("date")
    print(date)
    # date_lst = []
    # date_lst = date.split("-")
    # print(date_lst)

    data =datetime.datetime.strptime(date,"%Y-%m-%d").date()
    print(data)
    student =Students.objects.get(admin=request.user.id)
    semester = Semester.objects.get(id = student.semester_id.id)
    # subject = Subjects.objects.filter(semester_id=semester.id)
    print(semester)
    attendence = Attendance.objects.filter(attendance_date=data,semester_id=semester)
    print(attendence)
    attendence_report = AttendanceReport.objects.filter(attendance_id__in=attendence,student_id=student)
    print(attendence_report)
    context = {
        "attendence_report":attendence_report,
    }
    return render(request,"student_template/student_attendance_post.html",context)

def exam_sub_listing(request):
    student = Students.objects.get(admin=request.user.id)
    semester = Semester.objects.get(id = student.semester_id.id) 
    subject = Subjects.objects.filter(semester_id = semester)
    print(subject)
    context = {
        "subject":subject,
    }
    return render(request,"student_template/exam_subject_list.html",context)

def exam(request,id):
    count = 0
    student = Students.objects.get(admin=request.user.id)
    print(student)
    semester = Semester.objects.get(id = student.semester_id.id)
    print(semester)
    subject = Subjects.objects.get(id = id)
    
    print(subject,"usahkuhaSKDHSDKHSADKJHKASIDJJDJ")
    try:
        question = Question.objects.filter(subject_id = subject)
    except:
        question = None
    print(question,"hello")
    if not question:
        messages.error(request,"No Questions Available")
        return redirect("exam_sub_listing")
        
    else:
        print("illa")
   
    for ques in question:
        request.session['answer'+str(count)]=ques.answer
        count +=1
    
    print(request.session['answer0'],"answer load")
    print(request.session['answer1'],"answer load")
    print(request.session['answer2'],"answer load")
 
    paginator = Paginator(question, 1)
    try:
        page=int(request.GET.get('page','1'))
    except:
        page=1
    try:
        page_obj = paginator.page(page)
    except(EmptyPage,InvalidPage):
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "question":question,
        "page_obj":page_obj,
    }
    return render(request,"student_template/student_exam_template.html",context) 

answer_list = []

def saveanswer(request):
    if request.method == 'GET':
        option = request.GET['ans']
        answer_list.append(option)
        print(answer_list)
    print(answer_list)    
    return JsonResponse({"key":"value"})

def exam_save_answer(request):
    print(answer_list)
    mark = 0
    for i in range(3):
        if request.session['answer'+str(i)] == answer_list[i]:
            mark+=5
    answer_list.clear()
    context = {
        "mark":mark,
    }
    return render(request,"student_template/congragulation.html",context)

def student_profile(request):
    print(request.user.id,"hai kelllo")
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin = user)
    print("hhdjksahdkjhALKSHDkajdhkAJH")
    # return HttpResponse("hai hello")
    return render(request,"student_template/student_profile.html",{"user":user,"student":student})

def student_profile_save(request):
    if request.method != 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        # try:
        customuser = CustomUser.objects.get(id = request.user.id)
        customuser.first_name = first_name
        customuser.last_name = last_name
        # if password!=None and password!="":
        #     customuser.set_password(password)
        customuser.save()

        student = Students.objects.get(admin=customuser.id)
        student.address = address
        student.save()
        messages.success(request,"Successfully Update Profile")
        return redirect("student_profile")
        # except:
        #     messages.error(request,"Failed To Update Profile")
        #     return HttpResponseRedirect("/student_profile")
@csrf_exempt
def student_fcmtoken_save(request):
    token=request.POST.get("token")
    try:
        student=Students.objects.get(admin=request.user.id)
        student.fcm_token=token
        student.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def student_all_notification(request):
    student=Students.objects.get(admin=request.user.id)
    notifications=NotificationStudent.objects.filter(student_id=student.id)
    return render(request,"student_template/all_notification.html",{"notifications":notifications})



def assignment_subject_listing(request):
    student = Students.objects.get(admin=request.user.id)
    semester = Semester.objects.get(id = student.semester_id.id) 
    subject = Subjects.objects.filter(semester_id = semester)
    print(subject)
    context = {
        "subject":subject,
    }
    return render(request,"student_template/assignment_sub_listing.html",context)


def assignment_student(request,id):
    
    student = Students.objects.get(admin=request.user.id)
    semester = Semester.objects.get(id = student.semester_id.id)
    subject = Subjects.objects.get(id = id)
    assignment = Assignment.objects.filter(subject_id = subject)
    form = AssignementForm()
    context = {
        "assignment":assignment,
        "form":form,
    }

    return render(request,"student_template/student_assignment.html",context)

def assignment_answer(request,pk):
    # form = AssignementForm()
    # if request.method == 'POST':
    #     assign = Assignment.objects.get(id=pk)
    #     answer = request.POST['answer']
    #     assign.answer=answer
    #     assign.save()
    # return redirect("assignment_subject_listing")
    if request.method != 'POST':
        HttpResponse("Method Not Allowed")
    else:    
        student = Students.objects.get(admin=request.user.id)
        print("student---",student)
        assign = Assignment.objects.get(id=pk)
        print("--assign---",assign)
        course = Courses.objects.get(id = student.course_id.id)
        print("course----",course)
        answer = request.POST.get('answer')
        subject = Subjects.objects.get(id=assign.subject_id.id)
        try:
            assignment_answer = AssignmentAnswer()
            assignment_answer.answer = answer
            assignment_answer.subject_id = subject
            assignment_answer.question_id = assign
            assignment_answer.student_id = student
            assignment_answer.save()
            messages.success(request,"Successfully Add Answer")
            return HttpResponseRedirect("/assignment_subject_listing")
    
        except:
            messages.error(request,"Successfully Add Answer")
            return HttpResponseRedirect("/assignment_subject_listing")


def student_view_result(request):
    student = Students.objects.get(admin=request.user.id)
    studentresult =StudentResult.objects.filter(student_id=student.id)
    context={
        "studentresult":studentresult,
    }
    return render(request,"student_template/student_result.html ",context)

def time_table_student(request):
    student = Students.objects.get(admin=request.user.id)
    course = Courses.objects.get(id=student.course_id.id)
    semester = Semester.objects.get(id=student.semester_id.id)
    print(semester)
    
    subject =Subjects.objects.filter(semester_id=semester)
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

    return render(request,"student_template/timetableviewstudent.html",context)


    





        
        
    


    
    


