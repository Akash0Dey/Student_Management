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
        return f'{self.session_start_year.year}-{self.session_end_year.year}'


class Subject(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=255)
    course_id=models.ForeignKey(Courses,on_delete=models.CASCADE,default=1)
    semester_id=models.ForeignKey(Semester,on_delete=models.CASCADE,default=1)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.subject_name+" "+self.course_id.course_name+" "+self.semester_id.semester


class SubjectWithStaff(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    session_id=models.ForeignKey(Session,on_delete=models.DO_NOTHING)
    staff_id=models.ForeignKey(Staff,on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.subject_id.subject_name+" "+self.subject_id.course_id.course_name+" "+self.subject_id.semester_id.semester+" "+self.staff_id.name+" "+str(self.session_id.session_start_year.year)+"-"+str(self.session_id.session_end_year.year)


class Attendance(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(SubjectWithStaff,on_delete=models.DO_NOTHING)
    attendance_date=models.DateTimeField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.attendance_date.strftime("%Y-%m-%d %H:%M:%S")+" "+self.subject_id.subject_id.subject_name

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
    


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}"

class Routine(models.Model):

    id=models.AutoField(primary_key=True)

    course=models.ForeignKey(Courses,on_delete=models.DO_NOTHING)

    semester = models.ForeignKey(Semester, on_delete=models.DO_NOTHING)

    day = models.CharField(max_length=10, choices=[('Monday', 'Monday'), ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'),
                                                   ('Thursday', 'Thursday'), ('Friday', 'Friday'), ('Saturday', 'Saturday')])

    timeslot = models.ForeignKey(TimeSlot, on_delete=models.DO_NOTHING)

    subject = models.ForeignKey(SubjectWithStaff, on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
    
        return f"{self.course} {self.semester.semester}  {self.day} - {self.timeslot}"

