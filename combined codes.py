import cv2
import psutil
import time
import matplotlib.pyplot as plt

# Load the pre-trained face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Initialize variables for tracking time
productive_time = 0
unproductive_time = 0

# Variables for tracking time when face is not detected
time_face_not_detected = 0
last_face_detected_time = time.time()

# Function to check if PyCharm is running
def is_pycharm_running():
    return any(proc.name() == 'pycharm64.exe' or proc.name() == 'pycharm.exe' for proc in psutil.process_iter())

# Main loop
while True:
    # Read the frame
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Update time when face is not detected
    if len(faces) == 0:
        time_face_not_detected = time.time() - last_face_detected_time
    else:
        last_face_detected_time = time.time()

    # Draw rectangle around the face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

    # Display the timer
    if len(faces) == 1:
        productive_time += 1
    else:
        # Increment unproductive time without decimal values
        unproductive_time += int(time_face_not_detected)
        time_face_not_detected = 0

    # Calculate total time
    total_time = productive_time + unproductive_time

    # Display the frame
    cv2.imshow('Face Detection', frame)

    # Check if PyCharm is running
    if is_pycharm_running() and len(faces) == 1:
        # Increment productive time by 1 second
        pass  # Already counted in the timer
    else:
        # Increment unproductive time by the time when face is not detected
        pass  # Already counted in the timer

    # Print the time spent in productive and unproductive activities
    print(f"Productive time (PyCharm): {productive_time} seconds")
    print(f"Unproductive time (Other apps): {unproductive_time} seconds")
    print(f"Total time: {total_time} seconds")

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture
cap.release()
cv2.destroyAllWindows()
