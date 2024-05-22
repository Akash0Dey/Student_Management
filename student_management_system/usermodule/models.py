from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import os

# Create your models here.
class Courses(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

    def __str__(self):
        return self.course_name
    

class Semester(models.Model):
    SEMESTER_CHOICES = (
        ("1st", '1st Semester'),
        ("2nd", '2nd Semester'),
        ("3rd", '3rd Semester'),
        ("4th", '4th Semester'),
        ("5th", '5th Semester'),
        ("6th", '6th Semester'),
    )
    YEAR_CHOICES = (
        ("1st", '1st Year'),
        ("2nd", '2nd Year'),
        ("3rd", '3rd Year'),
    )
    semester = models.CharField(choices=SEMESTER_CHOICES, max_length=100)
    year = models.CharField(choices=SEMESTER_CHOICES, max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return f'{self.year} Year {self.semester} Semester'
    

class CustomUser(AbstractUser):
    user_type_data=((1,"HOD"),(2,"Staff"),(3,"Student"))
    user_type=models.CharField(default=1, choices=user_type_data, max_length=10)


class HOD(models.Model):
    hod=models.OneToOneField(CustomUser,on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True)
    approved = models.BooleanField(default=True)


    def __str__(self):
        return self.hod.username

class Staff(models.Model):
    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        filename = '{}.{}'.format(instance.id, ext)
        
        # return the whole path to the file
        return os.path.join("Staff", filename)

    id=models.AutoField(primary_key=True)
    staff=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    photo = models.FileField(upload_to=wrapper, blank=True)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    phone = models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    objects=models.Manager()

    def __str__(self):
        return self.name
    

class Student(models.Model):

    def wrapper(instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        filename = '{}.{}'.format(instance.id, ext)

        return os.path.join("Student", filename)

        
    id=models.AutoField(primary_key=True)
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    reg_id = models.CharField(max_length=10)
    photo = models.FileField(upload_to=wrapper)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    verified = models.BooleanField(default=False)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    phone = models.IntegerField()
    sem = models.ForeignKey(Semester, on_delete=models.SET_NULL, null=True)
    course_id=models.ForeignKey(Courses,on_delete=models.DO_NOTHING)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)
    objects=models.Manager()

    def __str__(self):
        return self.name
    


class ApproveStudent(models.Model):

    student = models.OneToOneField(Student, on_delete=models.DO_NOTHING)

    by_staff = models.ForeignKey(Staff, on_delete=models.DO_NOTHING)
    

    def __str__(self):

        return self.student + " Approved By "+self.by_staff



class ApproveStaff(models.Model):

    staff = models.OneToOneField(Staff, on_delete=models.DO_NOTHING)
    
    by_hod = models.ForeignKey(HOD, on_delete=models.DO_NOTHING)

    def __str__(self):

        return self.staff + " Approved By "+self.by_hod



class ApproveHOD(models.Model):

    hod = models.OneToOneField(HOD, on_delete=models.DO_NOTHING, related_name="approved_hod")

    by_hod = models.ForeignKey(HOD, on_delete=models.DO_NOTHING, related_name="approver_hod")
    

    def __str__(self):

        return self.hod + " Approved By "+self.by_hod



# @receiver(post_save,sender=CustomUser)
# def create_user_profile(sender,instance,created,**kwargs):
#     if created:
#         if instance.user_type==1:
#             HOD.objects.create(hod=instance)
#         if instance.user_type==2:
#             Staff.objects.create(staff=instance)
#         if instance.user_type==3:
#             Student.objects.create(student=instance)

# @receiver(post_save,sender=CustomUser)
# def save_user_profile(sender,instance,**kwargs):
#     if instance.user_type==1:
#         instance.hod.save()
#     if instance.user_type==2:
#         instance.staff.save()
#     if instance.user_type==3:
#         instance.student.save()