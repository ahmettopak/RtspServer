import cv2
from flask import Flask, Response, render_template, request

app = Flask(__name__)

# Open a connection to the default camera (camera index 0)
video_capture = cv2.VideoCapture(0)


def set_resolution(width, height):
    # Set the video resolution to the specified width and height
    video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


def generate_frames():
    while True:
        # Read a frame from the camera
        success, frame = video_capture.read()
        if not success:
            break
        else:
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
