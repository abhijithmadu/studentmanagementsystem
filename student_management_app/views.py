from django import http
from django.contrib.auth import login, logout
from student_management_app.EmailBackEnd import EmailBackEnd
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.contrib import messages

# Create your views here.

def showDemoPage(request):
    return render(request,"demo.html")

def loginPage(request):
    return render(request,"login_page.html")

def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method not allowed!</h2>")

    else:
        user = EmailBackEnd.authenticate(request,username = request.POST.get("email"),password = request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type == "1":
                return HttpResponseRedirect("/admin_home")
            elif user.user_type == "2":
                return HttpResponse("Staff Login")
            else:
                return HttpResponse("student Login")
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/")

def GetUserDetails(request):
    if request.user!=None:
        return HttpResponse("user : "+request.user.email + "usertype : " +request.user.user_type)

    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

         
        

    
