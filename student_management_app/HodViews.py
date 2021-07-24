from django.contrib import messages
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .models import Courses, CustomUser, Staffs, Students, Subjects

def admin_home(request):
    return render(request,"hod_template/home_content.html")

def add_staff(request):
    return render(request,"hod_template/add_staff_template.html")

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
            user = CustomUser.objects.create_user(username = username,first_name=first_name,last_name=last_name,email=email,password=password,user_type=2)
            user.staffs.address= address
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
    return render(request,"hod_template/add_student_template.html",{"courses":courses})
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
        session_start=request.POST.get("session_start")
        session_end=request.POST.get("session_end")
        course_id = request.POST.get("course")
        sex = request.POST.get("sex")
        try:
            user = CustomUser.objects.create_user(username = username,first_name=first_name,last_name=last_name,email=email,password=password,user_type=3)
            user.students.address= address
            course_obj = Courses.objects.get(id=course_id)
            user.students.course_id = course_obj
            user.students.gender= sex
            user.students.session_start_year=session_start
            user.students.session_end_year=session_end
            user.students.profile_pic = ""
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect("/add_students")
        except:
            messages.error(request,"Failed To Add Student")
            return HttpResponseRedirect("/add_students") 

def add_subject(request):
    courses = Courses.objects.all()
    staffs=CustomUser.objects.filter(user_type=2)
    context={
        "courses":courses,
        "staffs":staffs,
    }
    return render(request,"hod_template/add_subject_template.html",context)

def add_subject_save(request):
    if request.method != 'POST': 
        return HttpResponse("Method Not Allowed")
    else:
        subject_name= request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course = Courses.objects.get(id=course_id)
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
    staffs = Staffs.objects.all()
    return render(request,"hod_template/manage_staff_template.html",{"staffs":staffs})

def manage_students(request):
    students = Students.objects.all()
    return render(request,"hod_template/manage_student_template.html",{"students":students})

def manage_courses(request):
    courses = Courses.objects.all()
    return render(request,"hod_template/manage_course_template.html",{"courses":courses})

def manage_subjects(request):
    subjects = Subjects.objects.all()
    return render(request,"hod_template/manage_subject_template.html",{"subjects":subjects})



       
         
    
