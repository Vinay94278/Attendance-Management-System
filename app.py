import cv2
import streamlit as st
from datetime import datetime, timedelta

# Function to detect face using Haar cascades
def detect_faces(frame, face_cascade):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return len(faces) > 0

# Initialize the face cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Streamlit app
st.title("Attendance Management System with Pre-recorded Video")

uploaded_file = st.file_uploader("Upload a video file...", type=["mp4", "avi", "mov"])

if uploaded_file is not None:
    # Convert the uploaded file to a video file
    temp_file = "temp_video.mp4"
    with open(temp_file, "wb") as f:
        f.write(uploaded_file.read())

    # Video capture from the uploaded video file
    cap = cv2.VideoCapture(temp_file)

    run = st.checkbox('Run')
    FRAME_WINDOW = st.image([])

    appearance_time = None
    previous_appearance_time = None
    disappearance_time = None
    face_present = False
    min_duration = timedelta(seconds=1)  # Minimum duration threshold

    while run and cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        face_detected = detect_faces(frame, face_cascade)

        # Check if a face is detected and wasn't previously
        if face_detected and not face_present:
            appearance_time = datetime.now()
            if previous_appearance_time is None or (appearance_time - previous_appearance_time) >= min_duration:
                st.write(f"Person appeared at: {appearance_time.strftime('%H:%M:%S')}")
            previous_appearance_time = appearance_time
            face_present = True

        # Check if no face is detected and one was previously detected
        elif not face_detected and face_present:
            disappearance_time = datetime.now()
            duration = disappearance_time - appearance_time
            if duration >= min_duration:
                st.write(f"Person disappeared at: {disappearance_time.strftime('%H:%M:%S')}")
                st.write(f"Duration: {duration}")
            face_present = False

        # Display the frame in Streamlit
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW.image(frame)

    cap.release()
else:
    st.write("Please upload a video file.")
