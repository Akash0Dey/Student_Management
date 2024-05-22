from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
import json
from usermodule.models import CustomUser,Student,Staff, Semester, HOD, Courses
from datamodule.models import Attendance, AttendanceReport, Session, Subject, SubjectWithStaff, Routine, TimeSlot

# Create your views here.

usertypedata = {1:"HOD", 2:"Staff",3:"Student"}
SEMdata = ["1st", "2nd", "3rd", "4th", "5th", "6th"]
YEARdata = ["1st", "1st", "2nd", "2nd", "3rd", "3rd"]
DEPTdata = ["CST", "EE", "ME", "ETC"]

def check_approve(request):
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user).first()

    return User.approved==False


def get_str(object, objectlist):
    for ob in objectlist:
        if str(ob) == object:
            return ob
    return None


@login_required(login_url="/login")
def index(request):
    user = request.user
    if int(user.user_type) == 1:
       return redirect("hodDashboard")
    elif int(user.user_type) == 2:       
        return redirect("staffDashboard")
    elif int(user.user_type) == 3:
        return redirect("studentDashboard")


@login_required(login_url="/login")
def ThankYou(request):
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user).first()
    if check_approve(request):
        return redirect("waiting_student")
    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)]
    }
    return render(request, "ThankYou.html", data)


@login_required(login_url="/login")
def Student_list(request):
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()
    if check_approve(request):
        return redirect("waiting_student")
    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)]
    }
    data["studentTable"] =  Student.objects.filter(approved=True)
    return render(request, "student.html", data) 


@login_required(login_url="/login")
def Staff_list(request):
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()
    if check_approve(request):
        return redirect("waiting_student")
    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)]
    }
    data["staffTable"] =  Staff.objects.filter(approved=True)
    return render(request, "staff.html", data) 


@login_required(login_url="/login")
def HOD_list(request):
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()
    if check_approve(request):
        return redirect("waiting_student")
    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)]
    }
    data["HODTable"] =  HOD.objects.filter(approved=True)
    return render(request, "hod.html", data) 


@login_required(login_url="/login")
def HOD_Dashboard(request):
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        return redirect("staffDashboard")
    elif int(user.user_type) == 3:
        return redirect("studentDashboard")
    if check_approve(request):
        return redirect("waiting_student")
    data = {
        "user": User, 
        "usertype": usertypedata[int(user.user_type)],
        "NotStaff": Staff.objects.filter(approved=False),
        "NotHOD": HOD.objects.filter(approved=False),
        "studentNo": Student.objects.filter(approved=True).count(),
        "studentMale": Student.objects.filter(gender="Male", approved=True).count(),
        "studentFemale": Student.objects.filter(gender="Female", approved=True).count(),
        "staffNo": Staff.objects.filter(approved=True).count(),
        "courseNo": Courses.objects.count(),
        "subjectNo": Subject.objects.count(),
        "courses": {(course.course_name, json.dumps([random.randint(40, 100) for _ in range(12)])) for course in Courses.objects.all()},
    }
    return render(request, "hodDashboard.html", data) 


@login_required(login_url="/login")
def Student_Dashboard(request):
    user = request.user
    if int(user.user_type) == 1:
        return redirect("hodDashboard")
    elif int(user.user_type) == 2:
        return redirect("staffDashboard")
    elif int(user.user_type) == 3:
        student = Student.objects.filter(student=user, approved=True).first()
    data = {
        "user": student,
        "Sem": SEMdata, "Dept": DEPTdata,
        "photo": student.photo.url if student else "",
        "RegID": student.reg_id if student else "",
        "Name": student.name if student else "",
        "DOB": student.dob if student else "",
        "Gender": student.gender if student else "Male",
        "Phone": student.phone if student else "",
        "Email": student.email if student else "",
        "semester": student.sem.semester if student else "1st",
        "department": student.course_id.course_name if student else "CST",
        "usertype": usertypedata[int(user.user_type)],
        "studentNo": Student.objects.filter(approved=True).count(),
        "studentMale": Student.objects.filter(gender="Male", approved=True).count(),
        "studentFemale": Student.objects.filter(gender="Female", approved=True).count(),
        "staffNo": Staff.objects.filter(approved=True).count(),
        "courseNo": Courses.objects.count(),
        "subjectNo": Subject.objects.count(),
    }
    return render(request, "studentDashboard.html", data) 


@login_required(login_url="/login")
def Staff_Dashboard(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) == 1:
        return redirect("hodDashboard")
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        return redirect("studentDashboard")
    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)],
        "studentNo": Student.objects.filter(approved=True).count(),
        "studentMale": Student.objects.filter(gender="Male", approved=True).count(),
        "studentFemale": Student.objects.filter(gender="Female", approved=True).count(),
        "staffNo": Staff.objects.filter(approved=True).count(),
        "courseNo": Courses.objects.count(),
        "subjectNo": Subject.objects.count(),
        "NotStudent": Student.objects.filter(approved=False),
    }
    return render(request, "staffDashboard.html", data) 


@login_required(login_url="/login")
def Student_Edit(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) != 3:
        return redirect("index")
    else:
        student = Student.objects.filter(student=user, approved=True).first()
        if request.method == "POST":

            form_data = request.POST
            form_files = request.FILES

            sem = Semester.objects.get(semester=form_data["CurrentSemester"])
            dep = Courses.objects.get(course_name=form_data["Major"])

            photo = form_files.get("Photo")
            student.photo =photo if photo else student.photo
            student.reg_id = form_data["regid"]
            student.name = form_data["Name"]
            student.dob = form_data["Birthday"]
            student.gender = form_data["Gender"]
            student.course_id = dep
            student.sem = sem
            student.phone = form_data["PhoneNumber"]
            student.email = form_data["Email"]
            student.save()
            messages.success(request, "Profile Updated successfully")
            return redirect("index")
        
        else:

            data = {
                "user": student,
                "usertype": usertypedata[int(user.user_type)],
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
        return render(request, "studentEdit.html", data)


@login_required(login_url="/login")
def Staff_Edit(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) != 2:
        return redirect("index")
    else:
        staff = Staff.objects.filter(staff=user, approved=True).first()
        if request.method == "POST":

            form_data = request.POST
            form_files = request.FILES

            photo = form_files.get("Photo")
            staff.photo =photo if photo else staff.photo
            staff.name = form_data["Name"]
            staff.dob = form_data["Birthday"]
            staff.gender = form_data["Gender"]
            staff.phone = form_data["PhoneNumber"]
            staff.email = form_data["Email"]
            staff.save()
            messages.success(request, "Profile Updated successfully")
            return redirect("index")
        
        else:

            data = {
                "user": staff,
                "usertype": usertypedata[int(user.user_type)],
                "photo": staff.photo.url,
                "Name": staff.name ,
                "DOB": staff.dob ,
                "Gender": staff.gender ,
                "Phone": staff.phone ,
                "Email": staff.email ,
            }   
        return render(request, "staffEdit.html", data)


@login_required(login_url="/login")
def HOD_Edit(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) != 1:
        return redirect("index")
    else:
        hod = HOD.objects.filter(hod=user, approved=True).first()

        if request.method == "POST":

            form_data = request.POST
            hod.name = form_data["Name"]
            hod.email = form_data["Email"]
            hod.save()
            messages.success(request, "Profile Updated successfully")
            return redirect("index")
        
        else:

            data = {
                "user": hod,
                "usertype": usertypedata[int(user.user_type)],
                "Name": hod.name,
                "Email": hod.email,
            }   
        return render(request, "hodEdit.html", data)
                

@login_required(login_url="/login")
def add_course(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) != 1:
        return redirect("index")
    else:
        hod = HOD.objects.filter(hod=user, approved=True).first()
    if request.method == 'POST':
        name = request.POST.get('Name')
        try:
            Courses.objects.create(course_name=name).save()
            messages.success(request, "Course Successfully Added")
            return redirect('index')
        except:
            pass
        messages.error(request, "Course Adding Unsuccessful")
    else:
        pass
    data = {
            "user": hod,
            "usertype": usertypedata[int(user.user_type)],
    }  
    return render(request, 'courseNew.html', data)  
                

@login_required(login_url="/login")
def Course_list(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()
    courses = Courses.objects.all()

    # Prepare courseTable data
    courseTable = []
    for course in courses:
        course_data = {
            'course_name': course.course_name,
            'subjects': {}
        }
        subject = Subject.objects.filter(course_id=course)
        for subject_id in subject:
        # Group subjects by semester
            subjects = SubjectWithStaff.objects.filter(subject_id=subject_id)
            for subject in subjects:
                semester = subject.subject_id.semester_id.semester  # Assuming subjects have a 'semester' field

                if semester in course_data['subjects']:

                    course_data['subjects'][semester].append(subject.subject_id.subject_name)

                else:

                    course_data['subjects'][semester] = [subject.subject_id.subject_name]

        course_data['subjects']= {semester: course_data['subjects'][semester] for semester in sorted(course_data['subjects'])}

        courseTable.append(course_data)
    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)],
        "courseTable": courseTable,
    }  
    return render(request, 'course.html', data)  


@login_required(login_url="/login")
def add_subject(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) != 1:
        return redirect("index")
    else:
        hod = HOD.objects.filter(hod=user, approved=True).first()

    if request.method == 'POST':
        name = request.POST.get('Name')
        course = Courses.objects.filter(course_name=request.POST.get('Major')).first()
        sem = Semester.objects.filter(semester=request.POST.get('Semester')).first()
        
        if Subject.objects.filter(subject_name=name, course_id=course, semester_id=sem).exists():
            messages.error(request, "Subject Name Already Exists!")
        else:
            try:
                Subject.objects.create(subject_name=name, course_id=course, semester_id=sem)
                messages.success(request, "Subject Successfully Added")
                return redirect('index')
            except Exception as e:
                messages.error(request, "Subject Adding Unsuccessful: {}".format(str(e)))

    data = {
        "user": hod,
        "usertype": usertypedata[int(user.user_type)],
        "Sem": SEMdata,
        "Dept": DEPTdata,
    }
    
    return render(request, 'subjectNew.html', data)


@login_required(login_url="/login")
def Subject_list(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()

    subjects = Subject.objects.all()

    # Prepare courseTable data
    subjectTable = []
    for subject in subjects:
        subject_data = {
            'subject_name': subject.subject_name,
            'course_name': subject.course_id.course_name,
            'semester_name': subject.semester_id.semester,
        }
        subjectTable.append(subject_data)
    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)],
        "subjectTable": subjectTable,
    }  
    return render(request, 'subject.html', data)  


@login_required(login_url="/login")
def SubjectStaff_list(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()

    subjects = SubjectWithStaff.objects.all()

    # Prepare courseTable data
    subjectTable = []
    for subject in subjects:
        subject_data = {
            'subject_name': subject.subject_id.subject_name,
            'course_name': subject.subject_id.course_id.course_name,
            'semester_name': subject.subject_id.semester_id.semester,
            'staff': subject.staff_id.name,
            'session': str(subject.session_id.session_start_year.year)+"-"+str(subject.session_id.session_end_year.year),
        }
        subjectTable.append(subject_data)
    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)],
        "subjectTable": subjectTable,
    }  
    return render(request, 'subjectStaffList.html', data)  


@login_required(login_url="/login")
def SubjectForTeacher(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) != 1:
        return redirect("index")
    else:
        hod = HOD.objects.filter(hod=user, approved=True).first()
    data = {
        "user": hod,
        "usertype": usertypedata[int(user.user_type)],
        "Subject": Subject.objects.all(),
        "Staff": Staff.objects.filter(approved=True),
        "Session": Session.objects.all(),
    }

    if request.method == 'POST':

        subject = get_str(request.POST.get('Subject'), data["Subject"])
        staff = get_str(request.POST.get('Staff'), data["Staff"])
        session = get_str(request.POST.get('Session'), data["Session"])

        try:
            
            if SubjectWithStaff.objects.filter(subject_id=subject, session_id=session, staff_id=staff).exists():
                messages.error(request, "This Log Already Exists!")
            elif SubjectWithStaff.objects.filter(subject_id=subject, session_id=session).exists():
                messages.error(request, "Staff for this Session Already Exists!")
            else:
                sub = SubjectWithStaff.objects.create(subject_id=subject, session_id=session, staff_id=staff)
                messages.success(request, "Subject Successfully Added")
                return redirect('index')
        except Exception as e:
            messages.error(request, "Subject Adding Unsuccessful: {}".format(str(e)))
    
    return render(request, 'subjectStaff.html', data)


@login_required(login_url="/login")
def add_session(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) != 1:
        return redirect("index")
    else:
        hod = HOD.objects.filter(hod=user, approved=True).first()

    if request.method == 'POST':
        session_start_year = request.POST.get('session_start_year')
        session_end_year = request.POST.get('session_end_year')

        if not Session.objects.filter(session_start_year=session_start_year, session_end_year=session_end_year).exists():

        # Create a new Session object
            try:
                Session.objects.create(
                    session_start_year=session_start_year,
                    session_end_year=session_end_year
                ).save()
                messages.success(request, "Session Adding Successful")
                return redirect('index')
            except Exception as e:
                messages.error(request, "Session Adding Unsuccessful: {}".format(str(e)))

        else:
            messages.error(request, "Session Already Exist ! ")
    data = {
        "user": hod,
        "usertype": usertypedata[int(user.user_type)],
    }
    
    return render(request, 'session.html', data)


@login_required(login_url="/login")
def Session_list(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()

    sessions = Session.objects.all()

    # Prepare courseTable data
    sessionTable = []
    for n,session in enumerate(sessions):
        session_data = (n+1, str(session.session_start_year.year)+'-'+str(session.session_end_year.year))
        sessionTable.append(session_data)
    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)],
        "sessionTable": sessionTable,
    }  
    return render(request, 'sessionlist.html', data)  
 

@login_required(login_url="/login")
def timetable_view(request, semester_id, major_id):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()

        # Get the selected semester and major
    semester = Semester.objects.get(id=semester_id)
    major = Courses.objects.get(id=major_id)


    # Get routines for the selected semester and major
    routines = Routine.objects.filter(semester=semester, course=major).order_by('timeslot').order_by('day')
    timeslot = TimeSlot.objects.all().order_by("start_time")

    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)],
        'sem': semester,
        'maj': major,
        'day': ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
        'routines': routines,
        'timeslots': timeslot,
        }  # For initial load, no data
    return render(request, 'timetable.html', data)


@login_required(login_url="/login")
def routine(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()

    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)],
        'semester': Semester.objects.all(),
        'major': Courses.objects.all(),
        }  # For initial load, no data
    return render(request, 'routine.html', data)


@login_required(login_url="/login")
def set_routine(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()

    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)],
        'semester': Semester.objects.all(),
        'major': Courses.objects.all(),
        }  # For initial load, no data
    return render(request, 'set-routine.html', data)


@login_required(login_url="/login")
def set_routine_view(request, semester_id, major_id):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()

        # Get the selected semester and major
    semester = Semester.objects.get(id=semester_id)
    major = Courses.objects.get(id=major_id)
    routines = Routine.objects.filter(semester=semester, course=major).order_by('timeslot').order_by('day')

    if request.method == "POST":
        form_data = request.POST
        for routine in routines:
            routine_data = form_data[f'routine_{routine.id}']
            if routine_data != 'blank':
                timetable = Routine.objects.get(id = routine.id)
                timetable.subject = SubjectWithStaff.objects.get(id = routine_data)
                timetable.save()
            else:
                timetable = Routine.objects.get(id = routine.id)
                timetable.subject = None
                timetable.save()

        return redirect(reverse("routine", args=(semester_id, major_id)))
    else:
        # Get routines for the selected semester and major
        timeslot = TimeSlot.objects.all().order_by("start_time")
        session = Session.objects.last()

        subjects = SubjectWithStaff.objects.all()

        # Prepare courseTable data
        subjectTable = []
        for subject in subjects:
            
            if subject.subject_id.semester_id == semester and subject.subject_id.course_id == major and subject.session_id == session:
                subjectTable.append(subject)

        data = {
            "user": User,
            "usertype": usertypedata[int(user.user_type)],
            'sem': semester,
            'maj': major,
            'day': ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'),
            'routines': routines,
            'timeslots': timeslot,
            'subject': subjectTable
            }  # For initial load, no data
    return render(request, 'setTable.html', data)


@login_required(login_url="/login")
def take_attendance(request):
    if check_approve(request):
        return redirect("waiting_student")

    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()

    if request.method == "POST":
        subject = request.POST["subject"]
        sub = SubjectWithStaff.objects.get(id=subject)
        attendance_id = Attendance.objects.create(subject_id=sub)
        return redirect(reverse("attendance", args=(attendance_id.id,)))
    else:

        data = {
            "user": User,
            "usertype": usertypedata[int(user.user_type)],
            'subjects': SubjectWithStaff.objects.filter(staff_id=User)
            }  # For initial load, no data
    return render(request, 'take_attendance.html', data)


@login_required(login_url="/login")
def attendance(request, attendance_id):
    if check_approve(request):
        return redirect("waiting_student")

    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()

    if request.method == "POST":
        att = Attendance.objects.get(id=attendance_id)
        for st in Student.objects.filter(sem = att.subject_id.subject_id.semester_id, course_id=att.subject_id.subject_id.course_id).order_by("reg_id"):
            
            if str(st.id) in request.POST:
                Att = AttendanceReport.objects.get(attendance_id=att, student_id=st)
                Att.status = True
                Att.save()
            else:
                Att = AttendanceReport.objects.get(attendance_id=att, student_id=st)
                Att.status = False
                Att.save()

        return redirect(reverse("show_attendance", args=(att.id, )))

    else:
        att = Attendance.objects.get(id=attendance_id)

        if AttendanceReport.objects.filter(attendance_id=att).exists():

            for st in Student.objects.filter(sem = att.subject_id.subject_id.semester_id, course_id=att.subject_id.subject_id.course_id).order_by("reg_id"):

                AttendanceReport.objects.create(attendance_id=att, student_id=st, status=False)

        data = {
            "user": User,
            "usertype": usertypedata[int(user.user_type)],
            "student": AttendanceReport.objects.filter(attendance_id=att)
            
            }  # For initial load, no data
        
    return render(request, 'attendance.html', data)


@login_required(login_url="/login")
def show_attendance(request, attendance_id=None, student=None):
    if check_approve(request):
        return redirect("waiting_student")

    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user, approved=True).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user, approved=True).first()

    data = {
        "user": User,
        "usertype": usertypedata[int(user.user_type)],
        "student": student
    }

    if attendance_id:

        att = Attendance.objects.get(id=attendance_id)

        data["attendance"] = AttendanceReport.objects.filter(attendance_id=att)#.order_by("student_id__reg_id")


        return render(request, 'show_attendance.html', data)


    else :

        data ["attendances"] =[ (Att, max([ A.updated_at for A in AttendanceReport.objects.filter(attendance_id=Att)])) for Att in Attendance.objects.all().order_by("-attendance_date")]
        data ["show"] =  True


    return render(request, 'show_attendance.html', data)
    


@login_required(login_url="/login")
def accept_student(request, student_id):
    if request.user.user_type != 2:
        return redirect("index") 
    st = Student.objects.get(id=f'{student_id}', approved=True)
    st.approved = True
    st.save()
    return redirect("index")


@login_required(login_url="/login")
def accept_staff(request, staff_id):
    if request.user.user_type != 1:
        return redirect("index") 
    st = Staff.objects.get(id=f'{staff_id}', approved=True)
    st.approved = True
    st.save()
    return redirect("index")


@login_required(login_url="/login")
def accept_hod(request, hod_id):
    if request.user.user_type != 1:
        return redirect("index") 
    st = HOD.objects.get(id=f'{hod_id}', approved=True)
    st.approved = True
    st.save()
    return redirect("index")




