from django import http
from django.contrib.auth import login, logout
from student_management_app.EmailBackEnd import EmailBackEnd
from django.http import response
from django.http.response import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate
from django.contrib import messages
from django.urls import reverse
from .models import Thread
from django.contrib.auth.decorators import login_required

# Create your views here.

def showDemoPage(request):
    return render(request,"demo.html")

def superadminlogin(request):
    return render(request,"superadmintemplate/superadminlogintemplate.html")

def superlogin(request):
    print("helllosupwer")
    if request.method !='POST':
        HttpResponse("Method Not allowed")
    else:
        username = "super@gmail.com"
        pword = "12345" 
        email = request.POST.get("email")
        print(email)
        password = request.POST.get("password")
        print(password)
        if username == email and pword == password:
            print("just a sample")
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
                return HttpResponseRedirect(reverse("staff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
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
    data='importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js");' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyCJ8KrGXMqXpcIqB0B1LSR4_XxPBIqh8Sw",' \
         '        authDomain: "studentmanagementsystem-6a09b.firebaseapp.com",' \
         '        projectId: "studentmanagementsystem-6a09b",' \
         '        storageBucket: "studentmanagementsystem-6a09b.appspot.com",' \
         '        messagingSenderId: "733206703450",' \
         '        appId: "1:733206703450:web:e0cfb5ba5ba4b6a7fe9763",' \
         '        measurementId: "G-JJ41EM0XK5"' \
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


def messages_page(request):
    print("hello url")
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    context = {
        'Threads': threads
    }
    return render(request, 'chat_template/messages.html', context)



         
        

    
