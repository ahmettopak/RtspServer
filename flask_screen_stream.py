import cv2
import numpy as np
import pyautogui
from flask import Flask, Response, render_template, request

app = Flask(__name__)

screen_width, screen_height = pyautogui.size()

def generate_frames():
    while True:
        # Read a frame from the camera
        screenshot = pyautogui.screenshot()

        # OpenCV formatına dönüştür
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Encode the frame to JPEG format
        ret, buffer = cv2.imencode('.jpg', frame)
        # Convert the frame to bytes
        frame = buffer.tobytes()
        # Yield the frame with MIME boundary for displaying in the browser
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def index():
    # Render the HTML template with the video stream
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    # Return the video frames as a multipart response with MIME boundary
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    # Run the Flask app on host 0.0.0.0 (accessible from outside the local machine) and port 5000
    app.run(host='0.0.0.0', port=5000)
