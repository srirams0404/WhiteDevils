import cv2
import numpy as np
import math
import threading
import time

# Global variables for time calculation
total_time = 0
start_time = 0
end_time = 0
looked_away = False


# Timer thread function
def timer_thread():
    global total_time, start_time, end_time, looked_away
    while True:
        if start_time != 0 and not looked_away:
            end_time = time.time()
            total_time += end_time - start_time
            start_time = time.time()
        time.sleep(1)


# Start the timer thread
timer = threading.Thread(target=timer_thread, daemon=True)
timer.start()

# Load pre-trained face and eye classifiers
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Reset timer if face is not detected
    if len(faces) == 0:
        looked_away = True
        start_time = 0
        end_time = 0
    else:
        looked_away = False

    # Iterate through each face found
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Extract region of interest (ROI) for eyes
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]

        # Detect eyes in the face ROI
        eyes = eye_cascade.detectMultiScale(roi_gray)

        # Check if two eyes are detected
        if len(eyes) == 2:
            # Sort eyes by x-coordinate to ensure consistent ordering
            eyes = sorted(eyes, key=lambda x: x[0])

            # Extract eye coordinates
            (ex1, ey1, ew1, eh1) = eyes[0]
            (ex2, ey2, ew2, eh2) = eyes[1]

            # Calculate eye centers
            eye_center1 = (x + ex1 + ew1 // 2, y + ey1 + eh1 // 2)
            eye_center2 = (x + ex2 + ew2 // 2, y + ey2 + eh2 // 2)

            # Draw circles around the eyes
            cv2.circle(frame, eye_center1, 2, (0, 255, 0), 2)
            cv2.circle(frame, eye_center2, 2, (0, 255, 0), 2)

            # Calculate angle between the line connecting the eyes and the line perpendicular to the camera plane
            dy = eye_center2[1] - eye_center1[1]
            dx = eye_center2[0] - eye_center1[0]
            angle = math.atan2(dy, dx) * 180.0 / math.pi

            # Threshold for considering eyes looking directly at the camera (adjust as needed)
            threshold = 5

            # Check if angle is within threshold
            if abs(angle) < threshold:
                cv2.putText(frame, 'Looking at camera', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the total time on the frame
    cv2.putText(frame, f'Total time: {total_time:.2f} seconds', (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Face Detection', frame)

    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Start timer when a frame is displayed
    start_time = time.time()

# Release the capture
cap.release()
cv2.destroyAllWindows()
