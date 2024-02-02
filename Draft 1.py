import psutil
import time
import matplotlib.pyplot as plt

# Function to check if an application is running
def is_app_running(app_name):
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() == app_name.lower():
            return True
    return False

# Function to check if any application other than PyCharm is running
def is_unproductive():
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'].lower() != "pycharm64.exe" and proc.info['name'].lower() != "pycharm.exe":
            return True
    return False

# Initialize variables for tracking time
total_time = 0
productive_time = 0
unproductive_time = 0

# List of applications to check
apps = ["pycharm64.exe"]

# Set to store running processes to track new ones
running_processes = set()

# Main loop
while True:
    # Check if PyCharm is running
    if is_app_running(apps[0]):
        # Increment productive time by 1 second
        productive_time += 1
    else:
        # Increment unproductive time by 1 second if any other app is running
        if is_unproductive():
            unproductive_time += 1

    # Check for new processes
    new_processes = set(p.info['name'].lower() for p in psutil.process_iter(['pid', 'name'])) - {"system", "idle"}
    for new_process in new_processes - running_processes:
        unproductive_time += 1

    # Update running processes set
    running_processes = new_processes

    # Increment total time by 1 second
    total_time += 1

    # Print the time spent in productive and unproductive activities
    print(f"Productive time (PyCharm): {productive_time} seconds")
    print(f"Unproductive time (Other apps): {unproductive_time} seconds")
    print(f"Total time: {total_time} seconds")

    # Pie chart
    labels = 'Productive', 'Unproductive', 'Total'
    sizes = [max(productive_time, 0), max(unproductive_time, 0), max(total_time - productive_time - unproductive_time, 0)]
    colors = ['lightgreen', 'lightcoral', 'lightskyblue']
    explode = (0.1, 0, 0)  # explode the 1st slice

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    plt.title('Productivity Tracker')
    plt.show()

    # Wait for 1 second before checking again
    time.sleep(1)
