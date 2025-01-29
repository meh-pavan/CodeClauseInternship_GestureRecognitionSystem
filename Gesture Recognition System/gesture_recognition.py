import cv2
import mediapipe as mp
import mysql.connector
from flask import Flask, render_template, Response

app = Flask(__name__)

def connect_to_db():
    return mysql.connector.connect(
        host="localhost",  
        user="root",       
        password="pavan.macha",  
        database="GestureRecognitionDB" 
    )

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

@app.route('/')
def index():
    return render_template('index.html')  

def log_gesture_to_db(gesture_name):
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
    query = "INSERT INTO gestures (gesture_name) VALUES (%s)"
    cursor.execute(query, (gesture_name,))
    db_connection.commit()
    cursor.close()
    db_connection.close()

def gen():
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

                gesture_name = "Open Hand" 

                log_gesture_to_db(gesture_name)

        _, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)