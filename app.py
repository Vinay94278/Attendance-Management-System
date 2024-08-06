import cv2
import streamlit as st
from datetime import datetime

# Function to detect face using Haar cascades
def detect_faces(frame, face_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return len(faces) > 0

# Initialize the face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Streamlit app
st.title("Attendance Management System")

run = st.checkbox('Run')
FRAME_WINDOW = st.image([])

appearance_time = None
disappearance_time = None
face_present = False

# Video capture from webcam
cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    if not ret:
        break

    face_detected = detect_faces(frame, face_cascade)

    # Check if a face is detected and wasn't previously
    if face_detected and not face_present:
        appearance_time = datetime.now()
        st.write(f"Person appeared at: {appearance_time.strftime('%H:%M:%S')}")
        face_present = True

    # Check if no face is detected and one was previously detected
    elif not face_detected and face_present:
        disappearance_time = datetime.now()
        st.write(f"Person disappeared at: {disappearance_time.strftime('%H:%M:%S')}")
        duration = disappearance_time - appearance_time
        st.write(f"Duration: {duration}")
        face_present = False

    # Display the frame in Streamlit
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    FRAME_WINDOW.image(frame)

cap.release()
