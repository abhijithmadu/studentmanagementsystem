from django import http
from django.contrib.auth import login, logout
from student_management_app.EmailBackEnd import EmailBackEnd
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages

# Create your views here.

def showDemoPage(request):
    return render(request,"demo.html")

def superadminlogin(request):
    return render(request,"superadmintemplate/superadminlogintemplate.html")

def superlogin(request):
    if request.method !='POST':
        HttpResponse("Method Not allowed")
    else:
        username = "super@gmail.com"
        pwd = "super" 
        email = request.POST.get("email")
        password = request.POST.get("password")
        if username == email and pwd == password:
            return HttpResponseRedirect("/superadmin_home")
        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/superadminlogin")

def logout_super(request):
    logout(request)
    return HttpResponseRedirect("/superadminlogin")

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
                return HttpResponseRedirect("/staff_home")
            else:
                return HttpResponseRedirect("/student_home")
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

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.8.1/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.8.1/firebase-messaging.js");' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyBnrjKzEc33BZE_sKA8KrEv336i7sI5k7o",' \
         '        authDomain: "studentmanagementsystem-2fdee.firebaseapp.com",' \
         '        projectId: "studentmanagementsystem-2fdee",' \
         '        storageBucket: "studentmanagementsystem-2fdee.appspot.com",' \
         '        messagingSenderId: "357107424809",' \
         '        appId: "1:357107424809:web:b80271c2deb98080598638",' \
         '        measurementId: "G-PZR89HF1TQ"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")



         
        

    
