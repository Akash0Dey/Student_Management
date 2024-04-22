from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import os
from usermodule.models import Student, Staff, HOD, Semester, Courses

# Create your models here.

class Session(models.Model):
    session_start_year=models.DateField("Year")
    session_end_year=models.DateField("Year")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.session_start_year.year} to {self.session_end_year.year}'


class Subject(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    semester_id=models.ForeignKey(Semester,on_delete=models.CASCADE,default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.subject_name+" "+self.course_id.course_name


class SubjectWithStaff(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    session_id=models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    staff_id=models.ForeignKey(Staff,on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.subject_id.subject_name+" "+self.staff_id.name+" "+self.subject_id.course_id.course_name


class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(SubjectWithStaff,on_delete=models.DO_NOTHING)
    attendance_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.attendance_date+" "+self.subject_id.subject_id.subject_name

class AttendanceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    attendance_id=models.ForeignKey(Attendance,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.student_id.name +" "+self.attendance_id.attendance_date+" "+self.attendance_id.subject_id.subject_id.subject_name