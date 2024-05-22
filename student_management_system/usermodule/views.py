from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from usermodule.models import CustomUser,Student,Staff, Semester, HOD, Courses
from usermodule.email import Email_it
from datamodule.models import Attendance, AttendanceReport, Session, Subject, SubjectWithStaff
import random
# Create your views here.

usertypedata = {1:"HOD", 2:"Staff",3:"Student"}
SEMdata = ["1st", "2nd", "3rd", "4th", "5th", "6th"]
YEARdata = ["1st", "1st", "2nd", "2nd", "3rd", "3rd"]
DEPTdata = ["CST", "EE", "ME", "ETC"]


def generate_random_code():
    return ''.join(random.choices('0123456789012345678901234567890123456789', k=4))

# User login/logout


def Login(request):
    if request.user.is_authenticated:
        return redirect('index')
    data={}
    if request.method=='POST':
        userid = request.POST['user']
        password = request.POST['password']
        if userid == '':
            messages.error(request, 'Please fill up User id')
        elif password == '':
            messages.error(request, 'Please fill up password')
        else:
            user = authenticate(request, username=userid, password=password)
        
            if user is None:
                messages.warning(request, 'UserName or Password is wrong')
                return render(request, 'login.html', data)
            else:
                login(request, user)
                request.session.set_expiry(0)
                messages.success(request, "Account Successfully Logged In, "+usertypedata[int(user.user_type)]+" "+user.username+ " Thank you for joining")
                if int(user.user_type) == 1:
                    return redirect("hod_Form")
                elif int(user.user_type) == 2:
                    return redirect("Staff_Form")
                elif int(user.user_type) == 3:
                    return redirect("Student_Form")
                
    return render(request, 'login.html', data)


@login_required(login_url="/login")
def Logout(request):
    logout(request)
    return redirect("login")



def Signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    data={}
    if request.method=='POST':
        userid = request.POST['user']
        usertype = request.POST['user-type']
        password = request.POST['password']
        repeatPassword = request.POST['repeatPassword']
        if userid == '':
            messages.error(request, 'Please fill up User id')
        elif password == '':
            messages.error(request, 'Please fill up password')
        elif password != repeatPassword : 
            messages.error(request,'Both password don\'t match')

        else:
            if CustomUser.objects.filter(username=userid).exists():
                messages.warning(request, "User Name already Exist")
            else:
                user = CustomUser.objects.create_user(username=userid, password=password, user_type=usertype)
                # user = authenticate(request, username=userid, password=password)
                login(request, user)
                request.session.set_expiry(0)
                messages.success(request, "User account Successfully created   "+user.username+ "  Thank you for joining !")
                if int(user.user_type) == 1:
                    return redirect("hod_Form")
                elif int(user.user_type) == 2:
                    return redirect("Staff_Form")
                elif int(user.user_type) == 3:
                    return redirect("Student_Form")
    return render(request, 'signup.html', data)



# Student views


@login_required(login_url="/login")
def Student_Form(request):
    user = request.user
    if int(user.user_type) == 1:
        return redirect("hod_Form")
    elif int(user.user_type) == 2:
        return redirect("Staff_Form")
    elif int(user.user_type) == 3:
        pass
    student = Student.objects.filter(student=request.user).first()
    if student:
        return redirect("ThankYou")
    if request.method == "POST":
        form_data = request.POST
        form_files = request.FILES

        data = {"Sem": SEMdata, "Dept": DEPTdata,
                "RegID":request.POST["regid"],
                "Name":request.POST["Name"],
                "DOB":request.POST["Birthday"],
                "Gender":request.POST["Gender"],
                "Phone":request.POST["PhoneNumber"],
                "Email":request.POST["Email"],
                "semester":request.POST["CurrentSemester"],
                "department":request.POST["Major"], 
            }
        
        try:
            sem = Semester.objects.get(semester=form_data["CurrentSemester"])
            dep = Courses.objects.get(course_name=form_data["Major"])
        
            # create a new student record
            Student.objects.create( student=request.user, photo=form_files["Photo"], reg_id=form_data["regid"], name=form_data["Name"], dob=form_data["Birthday"], gender=form_data["Gender"], course_id=dep, sem=sem, phone=form_data["PhoneNumber"], email=form_data["Email"],
            ).save()
        
            return redirect("ThankYou")  # Redirect to home page after successful registration/update
        except KeyError:
            messages.error(request, "Fill Up Properly")
        return render(request, "StudentForm.html", data)
    data = {"Sem": SEMdata, "Dept": DEPTdata,
            "Gender": "Male",
            "semester": "1st",
            "department": "CST", 
        }
    return render(request, "StudentForm.html", data)




@login_required(login_url="/login")
def Staff_Form(request):
    user = request.user
    if int(user.user_type) == 1:
        return redirect("hod_Form")
    elif int(user.user_type) == 2:
        pass
    elif int(user.user_type) == 3:
        return redirect("Student_Form")
    
    staff = Staff.objects.filter(staff=request.user).first()
    if staff:
        return redirect("ThankYou")
    if request.method == "POST":
        form_data = request.POST
        form_files = request.FILES

        data = {
                "Name":request.POST["Name"],
                "DOB":request.POST["Birthday"],
                "Gender":request.POST["Gender"],
                "Phone":request.POST["PhoneNumber"],
                "Email":request.POST["Email"],
            }
        
        try:
        
            # create a new Staff record
            Staff.objects.create(
                staff=request.user,
                photo=form_files.get("Photo"),
                name=form_data["Name"],
                dob=form_data["Birthday"],
                gender=form_data["Gender"],
                phone=form_data["PhoneNumber"],
                email=form_data["Email"],
            )
        
            return redirect("ThankYou")  # Redirect to home page after successful registration/update
        except KeyError:
            messages.error(request, "Fill Up Properly")
        return render(request, "StaffForm.html", data)
    data = {"Gender": "Male"}
    return render(request, "StaffForm.html", data)



@login_required(login_url="/login")
def hod_Form(request):
    user = request.user
    if int(user.user_type) == 1:
        pass
    elif int(user.user_type) == 2:
        return redirect("Staff_Form")
    elif int(user.user_type) == 3:
        return redirect("Student_Form")
    
    hod = HOD.objects.filter(hod=request.user).first()
    if hod:
        return redirect("ThankYou")
    if request.method == "POST":
        form_data = request.POST

        data = {"Name":request.POST["Name"],
                "Email":request.POST["Email"], 
            }
        
        try:

            # create a new HOD record
            HOD.objects.create(
                hod=request.user,
                name=form_data["Name"],
                email=form_data["Email"],
                approved=False,
            )
        
            return redirect("ThankYou")  # Redirect to home page after successful registration/update
        except KeyError:
            messages.error(request, "Fill Up Properly")
        return render(request, "HODForm.html", data)
    data = {"Sem": SEMdata, "Dept": DEPTdata,
            "Gender": "Male",
            "semester": "1st",
            "department": "CST", 
        }
    return render(request, "HODForm.html", data)
            


@login_required(login_url="/login")
def Email_varification(request):

    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user).first()
    
    if not User.email_varified:

        if request.method == "POST":
            email_Verifying_Code = request.POST["Email_Verifying_Code"]
            code = request.POST["code"].split(' ')
            if code[0] == email_Verifying_Code:
                user.email_varified = True
                user.save()
                messages.success(request, "Email Varification Successfully Completed")
                # user = request.user
                # if int(user.user_type) == 1:
                #     pass
                # elif int(user.user_type) == 2:
                #     return redirect("Staff_Form")
                # elif int(user.user_type) == 3:
                #     return redirect("Student_Form")
                return redirect("ThankYou")
            else:
                if int(code[1]) < 3:
                    data = {
                        "number": int(code[1])+1,
                        "code": code[0],
                        "Email": user.email
                    }
                else:
                    code = generate_random_code()
                    Email_it(email_to=user.email, subject="Email Verification Code ( "+request.user.user_type+" )", msg1=f"New Email Verification Code For {request.user.username} : ", 
                            code=code, msg2="\nEnter this code to verify youe Email\nSomeone Tried Three times in your account But failed")
                    data = {
                        "number": 0,
                        "code": code,
                        "Email": user.email
                    }
            return render(request, "EmailVerify.html", data)

        else:
            code = generate_random_code()
            Email_it(email_to=user.email, subject="Email Verification Code ( "+request.user.user_type+" )", msg1=f"Email Verification Code For {request.user.username} : ", 
                     code=code, msg2="\nEnter this code to verify youe Email")
            data = {
                "number": 0,
                "code": code,
                "Email": user.email
            }
            return render(request, "EmailVerify.html", data)

    else:
            user = request.user
            if int(user.user_type) == 1:
                return redirect("hod_Form")
            elif int(user.user_type) == 2:
                return redirect("Staff_Form")
            elif int(user.user_type) == 3:
                return redirect("Student_Form")
            


@login_required(login_url="/login")
def Student_approved(request):

    user = request.user
    if int(user.user_type) == 1:
        return redirect("waiting_HOD")
    elif int(user.user_type) == 2:
        return redirect("waiting_staff")
    elif int(user.user_type) == 3:
        pass

    User = Student.objects.filter(student=user).first()

    data ={ 
        'Student': User,
    }
    if User.approved:
        return redirect("ThankYou")
    else:
        return render(request, "Student_wait.html", data)


@login_required(login_url="/login")
def Staff_approved(request):

    user = request.user
    if int(user.user_type) == 1:
        return redirect("waiting_HOD")
    elif int(user.user_type) == 2:
        pass
    elif int(user.user_type) == 3:
        return redirect("waiting_student")
    User = Staff.objects.filter(staff=user).first()

    data ={ 
        'Staff': User,
    }
    if User.approved:
        return redirect("ThankYou")
    else:
        return render(request, "Staff_wait.html", data)


@login_required(login_url="/login")
def HOD_approved(request):

    user = request.user
    if int(user.user_type) == 1:
        pass
    elif int(user.user_type) == 2:
        return redirect("waiting_staff")
    elif int(user.user_type) == 3:
        return redirect("waiting_student")
    User = HOD.objects.filter(hod=user).first()

    data ={ 
        'HOD': User,
    }
    if User.approved:
        return redirect("ThankYou")
    else:
        return render(request, "HOD_wait.html", data)


@login_required(login_url="/login")
def Student_update(request):

    user = request.user
    if int(user.user_type) == 1:
        return redirect("HOD_update")
    elif int(user.user_type) == 2:
        return redirect("Staff_update")
    elif int(user.user_type) == 3:
        pass
    student = Student.objects.filter(student=request.user).first()

    if request.method == "POST":
        form_data = request.POST
        form_files = request.FILES

        data = {"Sem": SEMdata, "Dept": DEPTdata,
                "RegID":request.POST["regid"],
                "Name":request.POST["Name"],
                "DOB":request.POST["Birthday"],
                "Gender":request.POST["Gender"],
                "Phone":request.POST["PhoneNumber"],
                "Email":request.POST["Email"],
                "semester":request.POST["CurrentSemester"],
                "department":request.POST["Major"], 
            }
        
        try:
            sem = Semester.objects.get(semester=form_data["CurrentSemester"])
            dep = Courses.objects.get(course_name=form_data["Major"])
        
            # create a new student record
                 
            student.photo=form_files["Photo"]  if form_files.get("Photo") else student.photo
            student.reg_id=form_data["regid"]
            student.name=form_data["Name"]
            student.dob=form_data["Birthday"]
            student.gender=form_data["Gender"]
            student.course_id=dep
            student.sem=sem 
            student.phone=form_data["PhoneNumber"] 
            student.email=form_data["Email"]
            student.save()
        
            return redirect("ThankYou")  # Redirect to home page after successful registration/update
        except KeyError:
            messages.error(request, "Fill Up Properly")
        return render(request, "studentUpdate.html", data)
    data = {
        "Sem": SEMdata, "Dept": DEPTdata,
        "photo": student.photo.url,
        "RegID": student.reg_id ,
        "Name": student.name ,
        "DOB": student.dob ,
        "Gender": student.gender ,
        "Phone": student.phone ,
        "Email": student.email ,
        "semester": student.sem.semester ,
        "department": student.course_id.course_name ,
    }
    return render(request, "studentUpdate.html", data)


@login_required(login_url="/login")
def Staff_update(request):

    user = request.user
    if int(user.user_type) == 1:
        return redirect("HOD_update")
    elif int(user.user_type) == 2:
        pass
    elif int(user.user_type) == 3:
        return redirect("Student_update")
    
    staff = Staff.objects.filter(staff=request.user).first()
    if request.method == "POST":
        form_data = request.POST
        form_files = request.FILES

        data = {
                "Name":request.POST["Name"],
                "DOB":request.POST["Birthday"],
                "Gender":request.POST["Gender"],
                "Phone":request.POST["PhoneNumber"],
                "Email":request.POST["Email"],
            }
        
        try:
        
            # create a new Staff record
            
            staff.photo=form_files.get("Photo") if form_files.get("Photo") else staff.photo
            staff.name=form_data["Name"]
            staff.dob=form_data["Birthday"]
            staff.gender=form_data["Gender"]
            staff.phone=form_data["PhoneNumber"]
            staff.email=form_data["Email"]
            staff.save()
        
            return redirect("ThankYou")  # Redirect to home page after successful registration/update
        except KeyError:
            messages.error(request, "Fill Up Properly")
        return render(request, "staffUpdate.html", data)
    data = {
            "photo": staff.photo.url,
            "Name": staff.name ,
            "DOB": staff.dob ,
            "Gender": staff.gender ,
            "Phone": staff.phone ,
            "Email": staff.email ,
            }
    return render(request, "staffUpdate.html", data)



@login_required(login_url="/login")
def HOD_update(request):

    user = request.user
    if int(user.user_type) == 1:
        pass
    elif int(user.user_type) == 2:
        return redirect("Staff_update")
    elif int(user.user_type) == 3:
        return redirect("Student_update")
    
    hod = HOD.objects.filter(hod=request.user).first()

    if request.method == "POST":
        form_data = request.POST

        data = {"Name":request.POST["Name"],
                "Email":request.POST["Email"], 
            }
        
        try:

            # create a new HOD record
            
            hod.name=form_data["Name"]
            hod.email=form_data["Email"]
            hod.save()
        
            return redirect("ThankYou")  # Redirect to home page after successful registration/update
        except KeyError:
            messages.error(request, "Fill Up Properly")
        return render(request, "hodUpdate.html", data)
    data = {
        "Name":hod.name,
        "Email":hod.email, 
    }
    return render(request, "hodUpdate.html", data)



