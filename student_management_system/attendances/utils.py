# attendance/utils.py
import cv2
import os
import pandas as pd
import joblib
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from usermodule.models import CustomUser,Student,Staff, Semester, HOD, Courses
from student_management_system.settings import BASE_DIR
from datetime import date, datetime

attendance_file_path = os.path.join(BASE_DIR, 'Attendance', 'Attendance-{datetoday}.csv')

datetoday = date.today().strftime("%m_%d_%y")
datetoday2 = date.today().strftime("%d-%B-%Y")

HAARCASCADE_PATH = os.path.join(os.path.join(BASE_DIR, 'attendances', 'haarcascade_frontalface_default.xml'))
face_detector = cv2.CascadeClassifier(HAARCASCADE_PATH)

def totalreg():
    return Student.objects.count()

def identify_face(facearray):
    model = joblib.load('static/face_recognition_model.pkl')
    return model.predict(facearray)

def add_attendance(name):
    username = name.split('_')[0]
    userid = name.split('_')[1]
    current_time = datetime.now().strftime("%H:%M:%S")

    df = pd.read_csv(attendance_file_path)
    if int(userid) not in list(df['Roll']):
        with open(attendance_file_path, 'a') as f:
            f.write(f'\n{username},{userid},{current_time}')


def extract_faces(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_points = face_detector.detectMultiScale(gray, 1.2, 5, minSize=(20, 20))
        return face_points
    except:
        return []

def train_model():
    faces = []
    labels = []
    if os.path.exists('static/Student'):
        userlist = os.listdir('static/Student')
        for user in userlist:
            for imgname in os.listdir(f'static/Student/{user}'):
                img = cv2.imread(f'static/Student/{user}/{imgname}')
                resized_face = cv2.resize(img, (50, 50))
                faces.append(resized_face.ravel())
                labels.append(user)
    faces = np.array(faces)
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(faces, labels)
    joblib.dump(knn, 'static/face_recognition_model.pkl')

