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
from os import name
from froala_editor import views
from django.conf.urls import include
from student_management_app import  StaffViews,StudentViews,superadminview
# from student_management_app.EditResultViewClass import EditResultViewClass
from student_management_app import HodViews
from student_management_app import views
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from student_management_system import settings


urlpatterns = [
    path('superadminlogin',views.superadminlogin,name="superadminlogin"),
    path('superadmin_home',superadminview.superadmin_home,name="superadmin_home"),
    path('superlogin',views.superlogin,name="superlogin"),
    path('logout_super',views.logout_super,name="logout_super"),
    path('add_course', superadminview.add_course,name="add_course"),
    path('add_course_save', superadminview.add_course_save,name="add_course_save"),
    path('manage_courses',superadminview.manage_courses,name="manage_courses"),
    path('edit_course/<str:course_id>',superadminview.edit_course,name="edit_course"),
    path('edit_course_save',superadminview.edit_course_save,name="edit_course_save"),
    path('add_admin',superadminview.add_admin,name="add_admin"),
    path('add_admin_save',superadminview.add_admin_save,name="add_admin_save"),
    path('manage_admin',superadminview.manage_admin,name="manage_admin"),
    path('edit_admin/<str:admin_id>',superadminview.edit_admin,name="edit_admin"),
    path('edit_admin_save',superadminview.edit_admin_save,name="edit_admin_save"),

    path('demo',views.showDemoPage),
    path('chat/',views.messages_page,name="chat"),
    path('admin/', admin.site.urls),
    path('accounts/',include('django.contrib.auth.urls')),
    path('', views.loginPage,name="loginPage"),
    path('get_user_details',views.GetUserDetails,name="get_user_details"),
    path('logout_user',views.logout_user,name="logout"),
    path('doLogin', views.doLogin,name="doLogin"),
    path('admin_home', HodViews.admin_home,name="admin_home"),
    path('add_staff', HodViews.add_staff,name="add_staff"),
    path('add_staff_save', HodViews.add_staff_save,name="add_staff_save"),
    # path('add_course', HodViews.add_course),
    # path('add_course_save', HodViews.add_course_save),
    path('add_students', HodViews.add_students,name="add_students"),
    path('add_students_save', HodViews.add_students_save,name="add_students_save"),
    path('add_subject', HodViews.add_subject,name="add_subject"),
    path('add_subject_save', HodViews.add_subject_save,name="add_subject_save"),
    path('manage_staff', HodViews.manage_staff,name="manage_staff"),
    path('manage_students/<int:pk>',HodViews.manage_students,name="manage_students"),
    # path('manage_courses',HodViews.manage_courses),
    path('manage_subjects/<int:pk>',HodViews.manage_subjects,name="manage_subjects"),
    path('edit_staff/<str:staff_id>',HodViews.edit_staff,name="edit_staff"),
    path('edit_staff_save',HodViews.edit_staff_save,name="edit_staff_save"),
    # path('edit_course/<str:course_id>',HodViews.edit_course),
    # path('edit_course_save',HodViews.edit_course_save),
    path('edit_subject/<str:subject_id>',HodViews.edit_subject,name="edit_subject"),
    path('edit_subject_save',HodViews.edit_subject_save,name="edit_subject_save"),
    path('edit_student/<str:student_id>',HodViews.edit_student,name="edit_student"),
    path('edit_student_save',HodViews.edit_student_save,name="edit_student_save"),
    path('manage_semester',HodViews.manage_semester,name="manage_semester"),
    path('add_semester_save',HodViews.add_semester_save,name="add_semester_save"),
    # path('manage_session',HodViews.manage_session),
    # path('add_session_save',HodViews.add_session_save),
    path('student_feedback_message',HodViews.student_feedback_message,name="student_feedback_message"),
    path('student_feedback_message_replay',HodViews.student_feedback_message_replay,name="student_feedback_message_replay"),
    path('staff_feedback_message',HodViews.staff_feedback_message,name="staff_feedback_message"),
    path('staff_feedback_message_replay',HodViews.staff_feedback_message_replay,name="staff_feedback_message_replay"),
    path('student_leave_view',HodViews.student_leave_view,name="student_leave_view"),
    path('staff_leave_view',HodViews.staff_leave_view,name="staff_leave_view"),
    path('student_leave_approve/<str:leave_id>',HodViews.student_leave_approve,name="student_leave_approve"),
    path('student_leave_disapprove/<str:leave_id>',HodViews.student_leave_disapprove,name="student_leave_disapprove"),
    path('staff_leave_approve/<str:leave_id>',HodViews.staff_leave_approve,name="staff_leave_approve"),
    path('staff_leave_disapprove/<str:leave_id>',HodViews.staff_leave_disapprove,name="staff_leave_disapprove"),
    path('admin_send_notification_staff', HodViews.admin_send_notification_staff,name="admin_send_notification_staff"),
    path('admin_send_notification_student', HodViews.admin_send_notification_student,name="admin_send_notification_student"),
    path('send_student_notification', HodViews.send_student_notification,name="send_student_notification"),
    path('send_staff_notification', HodViews.send_staff_notification,name="send_staff_notification"),
    path('semester_subject',HodViews.semester_subject,name="semester_subject"),
    path('semester_student',HodViews.semester_student,name="semester_student"),
    path('check_email_exist',HodViews.check_email_exist,name="check_email_exist"),
    path('check_subject_exist',HodViews.check_subject_exist,name="check_subject_exist"),
    path('check_username_exist',HodViews.check_username_exist,name="check_username_exist"),
    path('time_table',HodViews.time_table,name="time_table"),

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
    path('add_question', StaffViews.add_question, name="add_question"),
    path('fetch_subject', StaffViews.fetch_subject, name="fetch_subject"),
    path('add_question_save', StaffViews.add_question_save, name="add_question_save"),
    path('staff_profile', StaffViews.staff_profile, name="staff_profile"),
    path('staff_profile_save', StaffViews.staff_profile_save, name="staff_profile_save"),
    path('staff_fcmtoken_save', StaffViews.staff_fcmtoken_save, name="staff_fcmtoken_save"), 
    path('staff_all_notification', StaffViews.staff_all_notification, name="staff_all_notification"),
    path('add_assignments',StaffViews.add_assignments,name="add_assignments"),
    path('add_assigenment_save',StaffViews.add_assigenment_save,name="add_assigenment_save"),
    path('assignment_check',StaffViews.assignment_check,name="assignment_check"),
    path('get_students_assignment',StaffViews.get_students_assignment,name="get_students_assignment"),
    path('assignment_subejct/<int:id><int:pk>/',StaffViews.assignment_subejct,name="assignment_subejct"),
    path('staff_assignment_answer/<int:id><int:pk>/',StaffViews.staff_assignment_answer,name="staff_assignment_answer"),
    path('staff_add_result',StaffViews.staff_add_result,name="staff_add_result"),
    path('save_student_result', StaffViews.save_student_result, name="save_student_result"),
    # path('edit_student_result',EditResultViewClass.as_view(), name="edit_student_result"),
    # path('fetch_result_student',StaffViews.fetch_result_student, name="fetch_result_student"),
    path('timetablesem',StaffViews.timetablesem, name="timetablesem"),
    path('time_table_staff',StaffViews.time_table_staff, name="time_table_staff"),

    path('start_live_classroom',StaffViews.start_live_classroom, name="start_live_classroom"),
    path('start_live_classroom_process',StaffViews.start_live_classroom_process, name="start_live_classroom_process"),

    #student url
    path('student_home',StudentViews.student_home,name="student_home"),
    path('student_view_attendence',StudentViews.student_view_attendence,name="student_view_attendence"),
    path('student_view_attendence_save',StudentViews.student_view_attendence_save,name="student_view_attendence_save"),
    path('student_apply_leave',StudentViews.student_apply_leave,name="student_apply_leave"),
    path('student_apply_leave_save',StudentViews.student_apply_leave_save,name="student_apply_leave_save"),
    path('student_feedback',StudentViews.student_feedback,name="student_feedback"),
    path('student_feedback_save',StudentViews.student_feedback_save,name="student_feedback_save"),
    path('exam_sub_listing',StudentViews.exam_sub_listing,name="exam_sub_listing"),
    path('exam/<int:id>/',StudentViews.exam,name="exam"),
    path('saveanswer',StudentViews.saveanswer,name="saveanswer"),
    path('exam_save_answer',StudentViews.exam_save_answer,name="exam_save_answer"),
    path('student_profile', StudentViews.student_profile, name="student_profile"),
    path('student_profile_save', StudentViews.student_profile_save, name="student_profile_save"),
    path('student_fcmtoken_save', StudentViews.student_fcmtoken_save, name="student_fcmtoken_save"),
    path('firebase-messaging-sw.js',views.showFirebaseJS,name="show_firebase_js"),
    path('student_all_notification',StudentViews.student_all_notification,name="student_all_notification"),
    path('assignment_student/<int:id>/',StudentViews.assignment_student,name="assignment_student"),
    path('assignment_answer/<int:pk>/',StudentViews.assignment_answer,name="assignment_answer"),
    path('assignment_subject_listing',StudentViews.assignment_subject_listing,name="assignment_subject_listing"),
    path('attendence_view',StudentViews.attendence_view,name="attendence_view"),
    path('student_view_attendance_post',StudentViews.student_view_attendance_post,name="student_view_attendance_post"),
    path('student_view_result',StudentViews.student_view_result,name="student_view_result"),
    path('time_table_student',StudentViews.time_table_student,name="time_table_student"),
    path('join_class_room/<int:subject_id>/<int:semester_id>',StudentViews.join_class_room,name="join_class_room"),
    path('node_modules/canvas-designer/widget.html',StaffViews.returnHtmlWidget,name="returnHtmlWidget"),
    path('froala_editor/',include('froala_editor.urls')),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
