from django.shortcuts import render

# Create your views here.
# attendance/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .utils import train_model, totalreg, extract_faces, identify_face
from django.views.decorators.csrf import csrf_exempt
import os
import cv2
import numpy as np
import base64
import shutil
import json
from datetime import date, datetime
# attendance/views.py
from django.urls import reverse
from django.shortcuts import render
import pandas as pd
from student_management_system.settings import BASE_DIR
from usermodule.models import CustomUser,Student,Staff, Semester, HOD, Courses, ApproveHOD, ApproveStaff, ApproveStudent
from datamodule.models import Attendance, AttendanceReport, Session, Subject, SubjectWithStaff, Routine, TimeSlot
usertypedata = {1:"HOD", 2:"Staff",3:"Student"}


face_detector = cv2.CascadeClassifier(os.path.join(BASE_DIR, 'attendances', 'haarcascade_frontalface_default.xml'))
attendance_file_path = os.path.join(BASE_DIR, 'Attendance', 'Attendance-{datetoday}.csv')

nimgs = 10
datetoday2 = date.today().strftime("%d-%B-%Y")
def check_approve(request):
    user = request.user
    if int(user.user_type) == 1:
        User = HOD.objects.filter(hod=user).first()
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user).first()
    elif int(user.user_type) == 3:
        User = Student.objects.filter(student=user).first()

    return User.approved==False

def snapshots_cap(request):
    if check_approve(request):
        return redirect("waiting_student")
    user = request.user
    if int(user.user_type) != 3:
        return redirect("index")
    if request.method == 'POST':
        image_data = request.POST['imageData']
        images = image_data.split('^')[:-1]  # Remove the last empty split

        userimagefolder = os.path.join(BASE_DIR, 'static', f'{usertypedata[int(user.user_type)]}', f'{user.username}')
        if not os.path.exists(userimagefolder):
            os.makedirs(userimagefolder)
        else:
            shutil.rmtree(userimagefolder)
            os.makedirs(userimagefolder)

        for idx, image in enumerate(images):
            image_data = base64.b64decode(image.split(',')[1])
            image_array = np.frombuffer(image_data, np.uint8)
            img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            img_path = os.path.join(userimagefolder, f'{user.username}_{idx}.jpg')
            cv2.imwrite(img_path, img)

        train_model()
        return redirect('index')

    return render(request, 'snapshots.html', {})


@csrf_exempt
@require_http_methods(["POST"])
def process_frame(request, attendance_id):
    data = json.loads(request.body)
    image_data = data.get('image')
    if not image_data:
        return JsonResponse({'status': 'error', 'message': 'No image data received'})
    image_data = image_data.split(',')[1]
    image_data = base64.b64decode(image_data)
    image_array = np.frombuffer(image_data, np.uint8)
    img = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    
    faces = extract_faces(img)
    if len(faces):
        (x, y, w, h) = faces[0]
        face = cv2.resize(img[y:y+h, x:x+w], (50, 50))
        identified_person = identify_face(face.reshape(1, -1))[0]
        user = CustomUser.objects.filter(username=identified_person)[0]
        print(user.username)
        st =Student.objects.filter(student=user).first()
        att = Attendance.objects.get(id=attendance_id)
        if st in Student.objects.filter(sem = att.subject_id.subject_id.semester_id, course_id=att.subject_id.subject_id.course_id) :
            Att = AttendanceReport.objects.get(attendance_id=att, student_id=st)
            Att.status = True
            Att.save()

            response = {'status': 'success', 'person': {"id": st.id}}
        else:
            response = {'status': 'no_face'}
    else:
        response = {'status': 'no_face'}

    print(f"Received image data: {response}")
    
    
    return JsonResponse(response)


def video_attendance(request, attendance_id):
    user = request.user
    if int(user.user_type) == 1:
        return redirect("index")
    elif int(user.user_type) == 2:
        User = Staff.objects.filter(staff=user, approved=True).first()
    elif int(user.user_type) == 3:
        return redirect("index")

    if request.method == "POST":

        att = Attendance.objects.get(id=attendance_id)

        return redirect(reverse("show_attendance", args=(att.id, )))

    else:
        att = Attendance.objects.get(id=attendance_id)

        if not AttendanceReport.objects.filter(attendance_id=att).count():

            for st in Student.objects.filter(sem = att.subject_id.subject_id.semester_id, course_id=att.subject_id.subject_id.course_id).order_by("reg_id"):

                if not AttendanceReport.objects.filter(attendance_id=att, student_id=st).exists():
                    AttendanceReport.objects.create(attendance_id=att, student_id=st, status=False)

        data = {
            "user": User,
            "usertype": usertypedata[int(user.user_type)],
            "student": AttendanceReport.objects.filter(attendance_id=att),
            "attend": att,
            
            }  # For initial load, no data
        
    return render(request, 'video_attendance.html', data)

