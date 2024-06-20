"""
URL configuration for student_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from datamodule import views as d_views
from usermodule import views as u_views
from attendances import views as a_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', d_views.index, name="index"),

    path('attendance/snapshot',a_views.snapshots_cap, name='snapshot'),

    path('process_frame/<int:attendance_id>/', a_views.process_frame, name='process_frame'),

    # user login/logout

    path('login/', u_views.Login, name="login"),

    path('logout/', u_views.Logout, name="logout"),

    path('signup/', u_views.Signup, name="signup"),

    # Email Verify 

    path('email_verify/', u_views.Email_varification, name="email_verify"),

    # Thank You 

    path('thank_you/', d_views.ThankYou, name="ThankYou"),

    # Approval 

    path('waiting/student', u_views.Student_approved, name="waiting_student"),

    path('waiting/staff', u_views.Staff_approved, name="waiting_staff"),

    path('waiting/HOD', u_views.HOD_approved, name="waiting_HOD"),

    # Student Side

    path('student/form', u_views.Student_Form, name="Student_Form"),

    path('student/form/update', u_views.Student_update, name="Student_update"),

    path('student/List', d_views.Student_list, name="studentlist"),

    path('student/edit', d_views.Student_Edit, name="studentEdit"),

    path('student/dashboard', d_views.Student_Dashboard, name="studentDashboard"),

    # Staff Side

    path('staff/form', u_views.Staff_Form, name="Staff_Form"),
    
    path('staff/form/update', u_views.Staff_update, name="Staff_update"),

    path('staff/list', d_views.Staff_list, name="stafflist"),

    path('staff/edit', d_views.Staff_Edit, name="staffEdit"),

    path('staff/dashboard', d_views.Staff_Dashboard, name="staffDashboard"),

    # hod Side

    path('hod/form', u_views.hod_Form, name="hod_Form"),

    path('hod/form/update', u_views.HOD_update, name="HOD_update"),

    path('hod/list', d_views.HOD_list, name="hodlist"),
    
    path('hod/edit', d_views.HOD_Edit, name="hodEdit"),

    path('hod/dashboard', d_views.HOD_Dashboard, name="hodDashboard"),

    # Course

    path('course/add', d_views.add_course, name="addCourse"),

    path('course/list', d_views.Course_list, name="Courselist"),

    # Subject

    path('subject/add', d_views.add_subject, name="addSubject"),

    path('subject/list', d_views.Subject_list, name="Subjectlist"),

    path('subject/staff/list', d_views.SubjectStaff_list, name="SubjectStafflist"),

    path('subject/staff', d_views.SubjectForTeacher, name="SubjectStaff"),

    # Session

    path('session/add', d_views.add_session, name="addSession"),

    path('session/list', d_views.Session_list, name="Sessionlist"),

    # Routine

    path('routine/', d_views.routine, name="routine123"),

    path('routine/<int:semester_id>/<int:major_id>/', d_views.timetable_view, name="routine"),

    path('set-routine/<int:semester_id>/<int:major_id>/', d_views.set_routine_view, name="setRoutine"),

    path('set-routine/', d_views.set_routine, name="setRoutine123"),



    # Attendance

    path('attendance/', d_views.take_attendance, name="take_attendance"),

    path('attendance/manual/<int:attendance_id>/', d_views.attendance, name="attendance"),

    path('attendance/video/<int:attendance_id>/', a_views.video_attendance, name="video_attendance"),

    path('show_attendance/<int:attendance_id>/', d_views.show_attendance, name="show_attendance"),
    
    path('show_attendance/', d_views.show_attendance, name="showAttendance"),
    
    path('update_attendance/<int:attendance_id>/', d_views.attendance, name="update_attendance"),

    path('attendance/monthly/', d_views.monthly_attendance, name="monthly_attendance"),

    # Accept User

    path('Accept/student/<int:student_id>/', d_views.accept_student, name="accept_student"),

    path('Accept/staff/<int:staff_id>/', d_views.accept_staff, name="accept_staff"),

    path('Accept/hod/<int:hod_id>/', d_views.accept_hod, name="accept_hod"),



    
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
