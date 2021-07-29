from student_management_app.models import FeedBackStudent
from django.contrib import messages
from student_management_app.models import LeaveReportStudent, Students
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

def student_home(request):
    return render(request,"student_template/student_home_template.html")

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
        leave_message = request.POST.get("leave_message")
        student_id=Students.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportStudent(student_id=student_id,leave_date=leave_date,leave_message=leave_message,leave_status=1)
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
            feedback = FeedBackStudent(student_id=student,feedback=feedback_message)
            feedback.save()
            messages.success(request,"Successfully Send Feedback")
            return HttpResponseRedirect("/student_feedback")
        except:
            messages.error(request,"Failed To Send Feedback")
            return HttpResponseRedirect("/student_feedback")


