from django.contrib import admin
from datamodule.models import Subject, SubjectWithStaff, Courses, Attendance, AttendanceReport, Session, Semester
# Register your models here.

admin.site.register(Session)
admin.site.register(Subject)
admin.site.register(SubjectWithStaff)
admin.site.register(Attendance)
admin.site.register(AttendanceReport)

