import tkinter as tk
from tkinter import messagebox
import time

# Global variables for time tracking
total_time = 0
productive_time = 0
unproductive_time = 0

# Function to start the tracker
def start_tracker():
    global total_time, productive_time, unproductive_time
    total_time = 0
    productive_time = 0
    unproductive_time = 0
    # Replace the print statements with your code to start the tracker and update time variables

# Function to stop the tracker
def stop_tracker():
    # Replace the print statements with your code to stop the tracker and update time variables
    pass

# Function to exit the application
def exit_tracker():
    if messagebox.askokcancel("Exit Tracker", "Are you sure you want to exit?"):
        root.destroy()

# Create GUI
root = tk.Tk()
root.title("Productivity Tracker")

# Labels to display time information
total_label = tk.Label(root, text="Total Time: " + str(total_time) + " seconds")
total_label.pack()

productive_label = tk.Label(root, text="Productive Time: " + str(productive_time) + " seconds")
productive_label.pack()

unproductive_label = tk.Label(root, text="Unproductive Time: " + str(unproductive_time) + " seconds")
unproductive_label.pack()

# Add Start Tracker button
start_button = tk.Button(root, text="Start Tracker", command=start_tracker)
start_button.pack(pady=10)

# Add Stop Tracker button
stop_button = tk.Button(root, text="Stop Tracker", command=stop_tracker)
stop_button.pack(pady=10)

# Add Exit button
exit_button = tk.Button(root, text="Exit", command=exit_tracker)
exit_button.pack(pady=10)

root.mainloop()
