# Productivity tracker 

The Productivity tracker is a Python application that detects faces in real-time using the webcam of your computer. It provides a user-friendly interface built with Tkinter and displays the camera feed along with face detection statistics.

## Features

- **User Authentication**: Users can log in with their username and password.
- **Real-time Face Detection**: Utilizes OpenCV to detect faces in real-time.
- **Productivity Tracking**: Tracks the user's productive and unproductive time based on face detection while PyCharm is running.

## Installation

1. Clone the repository:

    ```bash
    git clone <repository_url>
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:

    ```bash
    python main.py
    ```

## Usage

1. Launch the application.
2. Enter your username and password.
3. Click the "Submit" button to log in.
4. The application will start detecting faces in the camera feed.
5. Face detection statistics, including total time, productive time, and unproductive time, are displayed below the camera feed.

## Dependencies

- Python 3.x
- OpenCV
- Tkinter
- PIL
- matplotlib
- plyer
- psutil

## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
