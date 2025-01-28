import streamlit as st
import cv2
import mediapipe as mp

st.title('Gesture Recognition')

# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Open a webcam feed
cap = cv2.VideoCapture(0)

# Create an empty container to hold the video feed
frame_container = st.empty()

# Stop button outside the loop
if st.button("Stop", key="stop_button"):
    cap.release()
    st.write("Video Feed Stopped.")
    st.stop()

# Display live video feed
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame for mirror effect
    frame = cv2.flip(frame, 1)
    
    # Convert frame to RGB for MediaPipe processing
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    # If hands are detected, draw landmarks on the frame
    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

    # Use the placeholder to display the image, this will update the frame each time
    frame_container.image(frame, channels="BGR", use_column_width=True)

cap.release()
