import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from plyer import notification
import psutil
import time


class FaceDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Detection App")

        # Mutable object to store face detection stats
        self.face_detection_stats = {'face_detected_count': 0, 'no_face_detected_count': 0}

        # Initialize total_time, productive_time, and unproductive_time
        self.total_time = 0
        self.productive_time = 0
        self.unproductive_time = 0

        # Username and password entry
        self.username_label = ttk.Label(root, text="Username:")
        self.username_label.grid(row=0, column=0, padx=10, pady=10)
        self.username_entry = ttk.Entry(root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=10)

        self.password_label = ttk.Label(root, text="Password:")
        self.password_label.grid(row=1, column=0, padx=10, pady=10)
        self.password_entry = ttk.Entry(root, show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        # Submit button
        self.submit_button = ttk.Button(root, text="Submit", command=self.submit_credentials)
        self.submit_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Greeting label
        self.greeting_label = ttk.Label(root, text="")
        self.greeting_label.grid(row=3, column=0, columnspan=2, pady=10)

        # Video label for displaying camera feed
        self.video_label = ttk.Label(root)
        self.video_label.grid(row=4, column=0, pady=10)

        # Timer label for displaying total time, productive time, and unproductive time
        self.timer_label = ttk.Label(root,
                                     text="Total Time: 0 seconds\nProductive Time: 0 seconds\nUnproductive Time: 0 seconds")
        self.timer_label.grid(row=5, column=0, columnspan=2, pady=10)

        # Run the Tkinter event loop
        self.update_pie_chart()

    def submit_credentials(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Check credentials
        if username == 'WhiteDevils' and password == 'WhiteDevils':
            self.greeting_label.config(text=f"Hello, {username}!")
            # Start face detection
            self.run_face_detection()
            # Start the timer
            self.total_time = 0
            self.productive_time = 0
            self.unproductive_time = 0
            self.update_timer()
        else:
            self.greeting_label.config(text="Invalid username or password")

    def update_pie_chart(self):
        # Calculate the percentage of face detected
        total_detections = self.face_detection_stats['face_detected_count'] + self.face_detection_stats[
            'no_face_detected_count']
        face_percentage = self.face_detection_stats[
                              'face_detected_count'] / total_detections if total_detections > 0 else 0

        # Update the pie chart
        self.create_pie_chart(face_percentage)

        # Schedule the next update after 5000 milliseconds (5 seconds)
        self.root.after(5000, self.update_pie_chart)

    def update_timer(self):
        self.total_time += 1
        self.timer_label.config(
            text=f"Total Time: {self.total_time} seconds\nProductive Time: {self.productive_time} seconds\nUnproductive Time: {self.unproductive_time} seconds")
        # Schedule the next update after 1000 milliseconds (1 second)
        self.root.after(1000, self.update_timer)

    def run_face_detection(self):
        # Load pre-trained face and eye classifiers
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        # Open the camera
        cap = cv2.VideoCapture(0)

        def is_pycharm_running():
            for process in psutil.process_iter(['pid', 'name']):
                if 'pycharm64.exe' in process.info['name'].lower():
                    return True
            return False

        def detect_faces():
            ret, frame = cap.read()
            if not ret:
                return
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            if len(faces) > 0:
                if is_pycharm_running():
                    self.face_detection_stats['face_detected_count'] += 1
                    self.productive_time += 1
                else:
                    notification.notify(
                        title='PyCharm Not Found',
                        message='PyCharm is not running!',
                        app_name='Face Detection App',
                        timeout=5
                    )
                    self.face_detection_stats['no_face_detected_count'] += 1
                    self.unproductive_time += 1
            else:
                if is_pycharm_running():
                    notification.notify(
                        title='No Face Detected',
                        message='Your face is not seen!',
                        app_name='Face Detection App',
                        timeout=5
                    )
                    self.face_detection_stats['no_face_detected_count'] += 1
                    self.unproductive_time += 1
            self.display_frame(frame)
            self.root.after(5000, detect_faces)

        detect_faces()

    def display_frame(self, frame):
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        photo = ImageTk.PhotoImage(image=image)
        self.video_label.config(image=photo)
        self.video_label.image = photo

    def create_pie_chart(self, face_percentage):
        labels = ['Face Detected', 'No Face Detected']
        sizes = [face_percentage, 1 - face_percentage]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=['green', 'red'])
        ax.axis('equal')
        pie_chart_canvas = FigureCanvasTkAgg(fig, master=self.root)
        pie_chart_canvas_widget = pie_chart_canvas.get_tk_widget()
        pie_chart_canvas_widget.grid(row=4, column=1, pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()
