import cv2
import time

# Load the pre-trained face detection model from OpenCV
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize variables
start_time = None
total_time_face_detected = 0
total_time_face_not_detected = 0
prev_face_detected = False

# Start capturing video from the default camera (usually the built-in webcam)
cap = cv2.VideoCapture(0)

try:
    while True:
        # Read a frame from the camera
        ret, frame = cap.read()

        # Convert the frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # If faces are detected, update the timer
        if len(faces) > 0:
            if not prev_face_detected:
                start_time = time.time()
                prev_face_detected = True
        else:
            if prev_face_detected:
                total_time_face_detected += time.time() - start_time
                prev_face_detected = False
                start_time = None
            else:
                total_time_face_not_detected += 1  # Assuming 1 second per iteration

        # Draw rectangles around the detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

        # Display the frame
        cv2.imshow('Face Detection', frame)

        # Check for user input to stop the code
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Release the camera and close all windows
    cap.release()
    cv2.destroyAllWindows()

    # Calculate and print the total time face detected and total time face not detected
    print(f"Total time face detected: {total_time_face_detected:.2f} seconds")
    print(f"Total time face not detected: {total_time_face_not_detected:.2f} seconds")
