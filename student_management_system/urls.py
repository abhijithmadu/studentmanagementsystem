"""student_management_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from student_management_app import StaffViews,StudentViews
from student_management_app import HodViews
from student_management_app import views
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from student_management_system import settings

urlpatterns = [
    
    path('demo',views.showDemoPage),
    path('admin/', admin.site.urls),
    path('', views.loginPage),
    path('get_user_details',views.GetUserDetails,name="get_user_details"),
    path('logout_user',views.logout_user,name="logout"),
    path('doLogin', views.doLogin,name="doLogin"),
    path('admin_home', HodViews.admin_home),
    path('add_staff', HodViews.add_staff),
    path('add_staff_save', HodViews.add_staff_save),
    path('add_course', HodViews.add_course),
    path('add_course_save', HodViews.add_course_save),
    path('add_students', HodViews.add_students),
    path('add_students_save', HodViews.add_students_save),
    path('add_subject', HodViews.add_subject),
    path('add_subject_save', HodViews.add_subject_save),
    path('manage_staff', HodViews.manage_staff),
    path('manage_students',HodViews.manage_students),
    path('manage_courses',HodViews.manage_courses),
    path('manage_subjects',HodViews.manage_subjects),
    path('edit_staff/<str:staff_id>',HodViews.edit_staff),
    path('edit_staff_save',HodViews.edit_staff_save),
    path('edit_course/<str:course_id>',HodViews.edit_course),
    path('edit_course_save',HodViews.edit_course_save),
    path('edit_subject/<str:subject_id>',HodViews.edit_subject),
    path('edit_subject_save',HodViews.edit_subject_save),
    path('edit_student/<str:student_id>',HodViews.edit_student),
    path('edit_student_save',HodViews.edit_student_save),
    path('manage_session',HodViews.manage_session),
    path('add_session_save',HodViews.add_session_save),
    path('student_feedback_message',HodViews.student_feedback_message,name="student_feedback_message"),
    path('student_feedback_message_replay',HodViews.student_feedback_message_replay,name="student_feedback_message_replay"),
    path('staff_feedback_message',HodViews.staff_feedback_message,name="staff_feedback_message"),
    path('staff_feedback_message_replay',HodViews.staff_feedback_message_replay,name="staff_feedback_message_replay"),
    


    # staff url
    path('staff_home',StaffViews.staff_home,name="staff_home"),
    path('staff_take_attendance', StaffViews.staff_take_attendance, name="staff_take_attendance"),
    path('get_students', StaffViews.get_students, name="get_students"),
    path('get_attendance_dates', StaffViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student', StaffViews.get_attendance_student, name="get_attendance_student"),
    path('save_attendance_data', StaffViews.save_attendance_data, name="save_attendance_data"),
    path('staff_update_attendance', StaffViews.staff_update_attendance, name="staff_update_attendance"),
    path('save_updateattendance_data', StaffViews.save_updateattendance_data, name="save_updateattendance_data"),
    path('staff_apply_leave', StaffViews.staff_apply_leave, name="staff_apply_leave"),
    path('staff_apply_leave_save', StaffViews.staff_apply_leave_save, name="staff_apply_leave_save"),
    path('staff_feedback', StaffViews.staff_feedback, name="staff_feedback"),
    path('staff_feedback_save', StaffViews.staff_feedback_save, name="staff_feedback_save"),
    #student url
    path('student_home',StudentViews.student_home,name="student_home"),
    path('student_apply_leave',StudentViews.student_apply_leave,name="student_apply_leave"),
    path('student_apply_leave_save',StudentViews.student_apply_leave_save,name="student_apply_leave_save"),
    path('student_feedback',StudentViews.student_feedback,name="student_feedback"),
    path('student_feedback_save',StudentViews.student_feedback_save,name="student_feedback_save"),
    
    

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
