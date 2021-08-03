from student_management_app.models import AdminHOD
from student_management_app.models import CustomUser
from student_management_app.models import Courses
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

def superadmin_home(request):
    return render(request,"superadmintemplate/superadmin_home_content.html")

def add_course(request):
    return render(request,"superadmintemplate/add_course_template.html")

def add_course_save(request):
    if request.method!= 'POST':
        return HttpResponse("Method Not Allowed")
    else:
        course= request.POST.get("course")
        semester = request.POST.get("semester")
        try:
            course_model = Courses(course_name=course,semesters=semester)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect("/add_course")
        except:
            messages.error(request,"Failed to Added Course")
            return HttpResponseRedirect("/add_course")

def manage_courses(request):
    courses = Courses.objects.all()
    return render(request,"superadmintemplate/manage_course_template.html",{"courses":courses})

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

def add_admin(request):
    courses=Courses.objects.all()
    context= {
        "courses":courses,
    }
    return render(request,"superadmintemplate/add_admin_template.html",context)
def add_admin_save(request):
    if request.method != 'POST': 
        return HttpResponse("Method Not Allowed")
    else:
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        course_id = request.POST.get("course")
        try:
            user = CustomUser.objects.create_user(username = username,first_name=first_name,last_name=last_name,email=email,password=password,user_type=1)
            course_obj = Courses.objects.get(id=course_id)
            user.adminhod.course_id = course_obj
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect("/add_admin")
        except:
            messages.error(request,"Failed To Add Student")
            return HttpResponseRedirect("/add_admin")

def manage_admin(request):
    admin = AdminHOD.objects.all()
    return render(request,"superadmintemplate/manage_admin_template.html",{"admin":admin})

def edit_admin(request,admin_id):
    admin=AdminHOD.objects.get(admin=admin_id)
    courses = Courses.objects.all()
    context= {
        "admin":admin,
        "courses":courses,
    }
    return render(request,"superadmintemplate/edit_admin_template.html",context)

def edit_admin_save(request):
    if request.method!='POST':
        return HttpResponse("Method Not Allowed")
    else:
        admin_id = request.POST.get("admin_id")
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        course_id = request.POST.get("course")
        try:
            user = CustomUser.objects.get(id=admin_id)
            user.first_name= first_name
            user.last_name = last_name
            user.username= username
            user.email=email
            user.save()

            admin_model= AdminHOD.objects.get(admin=admin_id)
            course = Courses.objects.get(id=course_id)
            admin_model.course_id= course
            admin_model.save()
            messages.success(request,"Successfully Edited Student")
            return HttpResponseRedirect("/edit_admin/" +admin_id)
        except:
            messages.error(request,"Failed To Edited Student")
            return HttpResponseRedirect("/edit_admin/" +admin_id)
