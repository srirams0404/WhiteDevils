import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plyer import notification
import psutil

# Mutable object to store face detection stats
face_detection_stats = {'face_detected_count': 0, 'no_face_detected_count': 0}

# Function to submit credentials and start face detection
def submit_credentials(username_entry, password_entry):
    username = username_entry.get()
    password = password_entry.get()

    # Check credentials
    if username == 'WhiteDevils' and password == 'WhiteDevils':
        greeting_label.config(text=f"Hello, {username}!")

        # Start face detection
        run_face_detection()

    else:
        greeting_label.config(text="Invalid username or password")

# Function to update the pie chart
def update_pie_chart():
    # Calculate the percentage of face detected
    total_detections = face_detection_stats['face_detected_count'] + face_detection_stats['no_face_detected_count']
    face_percentage = face_detection_stats['face_detected_count'] / total_detections if total_detections > 0 else 0

    # Update the pie chart
    create_pie_chart(face_percentage)

    # Schedule the next update after 5000 milliseconds (5 seconds)
    root.after(5000, update_pie_chart)

# Function to run face detection
def run_face_detection():
    # Load pre-trained face and eye classifiers
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Open the camera
    cap = cv2.VideoCapture(0)

    # Function to check if PyCharm is running
    def is_pycharm_running():
        for process in psutil.process_iter(['pid', 'name']):
            if 'pycharm64.exe' in process.info['name'].lower():
                return True
        return False

    def detect_faces():
        # Capture frame-by-frame
        ret, frame = cap.read()
        if not ret:
            return

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        # Check if face is detected
        if len(faces) > 0:
            # Check if PyCharm is running
            if is_pycharm_running():
                face_detection_stats['face_detected_count'] += 1
            else:
                # Increment no_face_detected_count and notify
                notification.notify(
                    title='PyCharm Not Found',
                    message='PyCharm is not running!',
                    app_name='Face Detection App',
                    timeout=5
                )
                face_detection_stats['no_face_detected_count'] += 1
        else:
            # Check if PyCharm is running
            if is_pycharm_running():
                # Increment no_face_detected_count and notify
                notification.notify(
                    title='No Face Detected',
                    message='Your face is not seen!',
                    app_name='Face Detection App',
                    timeout=5
                )
                face_detection_stats['no_face_detected_count'] += 1

        # Schedule the next face detection after 5000 milliseconds (5 seconds)
        root.after(5000, detect_faces)

        # Display the frame
        display_frame(frame)

    # Start the face detection loop
    detect_faces()

# Function to display the frame in the Tkinter window
def display_frame(frame):
    # Convert OpenCV frame to PIL format
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)

    # Convert PIL image to Tkinter format
    photo = ImageTk.PhotoImage(image=image)

    # Update the label with the new image
    video_label.config(image=photo)
    video_label.image = photo

# Function to create the pie chart
def create_pie_chart(face_percentage):
    # Create a pie chart
    labels = ['Face Detected', 'No Face Detected']
    sizes = [face_percentage, 1 - face_percentage]

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

    # Display the pie chart in the Tkinter window
    pie_chart_canvas = FigureCanvasTkAgg(fig, master=root)
    pie_chart_canvas_widget = pie_chart_canvas.get_tk_widget()
    pie_chart_canvas_widget.grid(row=4, column=1, pady=10)

# GUI setup
root = tk.Tk()
root.title("Face Detection App")

# Username and password entry
username_label = ttk.Label(root, text="Username:")
username_label.grid(row=0, column=0, padx=10, pady=10)
username_entry = ttk.Entry(root)
username_entry.grid(row=0, column=1, padx=10, pady=10)

password_label = ttk.Label(root, text="Password:")
password_label.grid(row=1, column=0, padx=10, pady=10)
password_entry = ttk.Entry(root, show='*')
password_entry.grid(row=1, column=1, padx=10, pady=10)

# Submit button
submit_button = ttk.Button(root, text="Submit", command=lambda: submit_credentials(username_entry, password_entry))
submit_button.grid(row=2, column=0, columnspan=2, pady=10)

# Greeting label
greeting_label = ttk.Label(root, text="")
greeting_label.grid(row=3, column=0, columnspan=2, pady=10)

# Video label for displaying camera feed
video_label = ttk.Label(root)
video_label.grid(row=4, column=0, pady=10)

# Run the Tkinter event loop
root.after(0, update_pie_chart)
root.mainloop()
