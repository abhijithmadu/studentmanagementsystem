from django.conf.urls.static import static
from django.contrib import admin, messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import AdminHOD, Courses, CustomUser, FeedBackStaffs, FeedBackStudent, LeaveReportStaff, LeaveReportStudent, SessionYearModel, Staffs, Students, Subjects

def admin_home(request):
    return render(request,"hod_template/home_content.html")

def add_staff(request):
    admin_id = AdminHOD.objects.get(admin=request.user.id)
    print(admin_id)
    courses=Courses.objects.get(id=admin_id.course_id.id)
    context ={
        "courses":courses,
    }
    return render(request,"hod_template/add_staff_template.html",context)

def add_staff_save(request):
    if request.method != 'POST': 
        return HttpResponse("Method Not Allowed")
    else:
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        try:
            admin_id = AdminHOD.objects.get(admin=request.user.id)
            print(admin_id)
            courses=Courses.objects.get(id=admin_id.course_id.id)
            print(courses)
            user = CustomUser.objects.create_user(username = username,first_name=first_name,last_name=last_name,email=email,password=password,user_type=2)
            user.staffs.address= address
            user.staffs.course_id = courses
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request,"Failed To Add Staff")
            return HttpResponseRedirect("/add_staff") 


def add_course(request):
    return render(request,"hod_template/add_course_template.html")

def add_course_save(request):
    if request.method!= 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        course= request.POST.get("course")
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request,"Failed to Added Course")
            return HttpResponseRedirect("/add_course")

def add_students(request):
    courses=Courses.objects.all()
    sessions = SessionYearModel.objects.all()
    context= {
        "courses":courses,
        "sessions":sessions,
    }
    return render(request,"hod_template/add_student_template.html",context)
def add_students_save(request):
    if request.method != 'POST': 
        return HttpResponse("Method Not Allowed")
    else:
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        address = request.POST.get("address")
        session_year_id=request.POST.get("session_year_id")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")
        try:
            user = CustomUser.objects.create_user(username = username,first_name=first_name,last_name=last_name,email=email,password=password,user_type=3)
            user.students.address= address
            course_obj = Courses.objects.get(id=course_id)
            user.students.course_id = course_obj
            user.students.gender= sex
            session_year=SessionYearModel.objects.get(id=session_year_id)
            user.students.session_year_id=session_year
            user.students.profile_pic = ""
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect("/add_students")
        except:
            messages.error(request,"Failed To Add Student")
            return HttpResponseRedirect("/add_students") 

def add_subject(request):
    admin = AdminHOD.objects.get(admin=request.user.id)
    courses=Courses.objects.get(id=admin.course_id.id)
    staffs=Staffs.objects.filter(course_id=courses)
    print(staffs)
    context={

        "staffs":staffs,
    }
    return render(request,"hod_template/add_subject_template.html",context)

def add_subject_save(request):
    if request.method != 'POST': 
        return HttpResponse("Method Not Allowed")
    else:
        subject_name= request.POST.get("subject_name")
        admin_id = AdminHOD.objects.get(admin=request.user.id)
        course = Courses.objects.get(id=admin_id.course_id.id)
        staff_id = request.POST.get("staff")
        staff = CustomUser.objects.get(id=staff_id)
        try:
            subject = Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect("/add_subject")
        except:
            messages.error(request,"Failed To Added Subject")
            return HttpResponseRedirect("/add_subject")

def manage_staff(request):
    admin_id = AdminHOD.objects.get(admin=request.user.id)
    print(admin_id)
    courses=Courses.objects.get(id=admin_id.course_id.id)
    staffs = Staffs.objects.filter(course_id=courses)
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_students(request):
    students = Students.objects.all()
    return render(request,"hod_template/manage_student_template.html",{"students":students})

def manage_courses(request):
    courses = Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})

def manage_subjects(request):
    admin_id = AdminHOD.objects.get(admin=request.user.id)
    courses=Courses.objects.get(id=admin_id.course_id.id)
    subjects = Subjects.objects.filter(course_id=courses)
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})

def edit_staff(request,staff_id):
    staff = Staffs.objects.get(admin=staff_id)
    return render(request,"hod_template/edit_staff_template.html",{"staff":staff})

def edit_staff_save(request):
    if request.method!= 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        print("sjhdsdfsbdhf")
        staff_id = request.POST.get("staff_id")
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        email= request.POST.get("email")
        address = request.POST.get("address")
        username= request.POST.get("username") 
    try:
        print("mjb")
        user = CustomUser.objects.get(id=staff_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()

        staff_model= Staffs.objects.get(admin=staff_id)
        staff_model.address= address
        staff_model.save()
        messages.success(request,"Successfully Edited Staff ")
        return HttpResponseRedirect("/edit_staff/"+staff_id)
    except:
        messages.error(request,"Failed To Edit Staff ")
        return HttpResponseRedirect("/edit_staff/"+staff_id)

def edit_course(request,course_id):
    course= Courses.objects.get(id=course_id)
    return render(request,"hod_template/edit_course_template.html",{"course":course})


def edit_course_save(request):
    if request.method!='POST':
        return HttpResponse("Method Not Allowed")
    else:
        course_id = request.POST.get("course_id")
        course_name = request.POST.get("course")
        print(course_name)
    try:
        course= Courses.objects.get(id=course_id)
        print( course.course_name)
        course.course_name= course_name
        course.save()
        messages.success(request,"Successfully Edited Course ")
        return HttpResponseRedirect("/edit_course/"+course_id)
    except:
        messages.error(request,"Failed To Edit Staff ")
        return HttpResponseRedirect("/edit_course/"+course_id)

def edit_subject(request,subject_id):
    subject = Subjects.objects.get(id=subject_id)
    admin = AdminHOD.objects.get(admin=request.user.id)
    courses=Courses.objects.get(id=admin.course_id.id)
    staffs=Staffs.objects.filter(course_id=courses)
    context= {
        "subject":subject,
        "staffs":staffs,
    }
    return render(request,"hod_template/edit_subject_template.html",context)


def edit_subject_save(request):
    if request.method!='POST':
        return HttpResponse("Method Not Allowed")
    else:
        subject_id = request.POST.get("subject_id")
        subject_name = request.POST.get("subject_name")
        staff_id = request.POST.get("staff")
        try:
            subject=Subjects.objects.get(id=subject_id)
            subject.subject_name=subject_name
            staff=CustomUser.objects.get(id=staff_id)
            subject.staff_id= staff
            subject.save()
            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect("/edit_subject/" +subject_id)
        except:
            messages.error(request,"Failed To Edited Subject")
            return HttpResponseRedirect("/edit_subject/" +subject_id)

def edit_student(request,student_id):
    student=Students.objects.get(admin=student_id)
    courses = Courses.objects.all()
    sessions = SessionYearModel.objects.all()
    context= {
        "student":student,
        "courses":courses,
        "sessions":sessions,
    }
    return render(request,"hod_template/edit_student_template.html",context)

def edit_student_save(request):
    if request.method!='POST':
        return HttpResponse("Method Not Allowed")
    else:
        student_id = request.POST.get("student_id")
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        
        address = request.POST.get("address")
        session_year_id=request.POST.get("session_year_id")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")
        try:
            user = CustomUser.objects.get(id=student_id)
            user.first_name= first_name
            user.last_name = last_name
            user.username= username
            user.email=email
            user.save()

            student_model= Students.objects.get(admin=student_id)
            student_model.address=address
            sessions= SessionYearModel.objects.get(id=session_year_id)
            student_model.session_year_id=sessions
            student_model.gender=sex
            course = Courses.objects.get(id=course_id)
            student_model.course_id= course
            student_model.save()
            messages.success(request,"Successfully Edited Student")
            return HttpResponseRedirect("/edit_student/" +student_id)
        except:
            messages.error(request,"Failed To Edited Student")
            return HttpResponseRedirect("/edit_student/" +student_id)

def manage_session(request):
    return render(request,"hod_template/manage_session_template.html")

def add_session_save(request):
    if request.method!='POST':
        return HttpResponse("Method Not Allowed")
    else:
        session_start_year = request.POST.get("session_start")
        session_end_year = request.POST.get("session_end")
        try:
            session_year = SessionYearModel(session_start_year=session_start_year,session_end_year=session_end_year)
            session_year.save()
            messages.success(request,"Successfully Added Session Year")
            return HttpResponseRedirect("/manage_session")
        except:
            messages.error(request,"Failed To Added Session Year")
            return HttpResponseRedirect("/manage_session")

def student_feedback_message(request):
    feedback = FeedBackStudent.objects.all()
    context = {
        "feedback":feedback,
    }
    return render(request,"hod_template/student_feedback_template.html",context)

@csrf_exempt
def student_feedback_message_replay(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")


def staff_feedback_message(request):
    feedback = FeedBackStaffs.objects.all()
    context = {
        "feedback":feedback,
    }
    return render(request,"hod_template/staff_feedback_template.html",context)

@csrf_exempt
def staff_feedback_message_replay(request):
    feedback_id = request.POST.get("id")
    feedback_message = request.POST.get("message")
    try:
        feedback = FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply = feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def student_leave_view(request):
    leave_report = LeaveReportStudent.objects.all()
    context= {
        "leave_report":leave_report
    }
    return render(request,"hod_template/student_leave_view.html",context)

def staff_leave_view(request):
    leave_report = LeaveReportStaff.objects.all()
    context ={
        "leave_report":leave_report,
    }
    return render(request,"hod_template/staff_leave_view.html",context)

def student_leave_approve(request,leave_id):
    leave= LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect("/student_leave_view")

def student_leave_disapprove(request,leave_id):
    leave=LeaveReportStudent.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect("/student_leave_view")


def staff_leave_approve(request,leave_id):
    leave= LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=1
    leave.save()
    return HttpResponseRedirect("/staff_leave_view")

def staff_leave_disapprove(request,leave_id):
    leave=LeaveReportStaff.objects.get(id=leave_id)
    leave.leave_status=2
    leave.save()
    return HttpResponseRedirect("/staff_leave_view")







    


            






        





       
         
    
