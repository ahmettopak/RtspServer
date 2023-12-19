import cv2
import numpy as np
import pyaudio
import wave
from flask import Flask, Response, render_template

app = Flask(__name__)

video_capture = cv2.VideoCapture(0)

# Ses kaydı için değişkenler
audio_chunk_size = 1024
audio_format = pyaudio.paInt16
audio_channels = 1
audio_rate = 44100
audio_frames_per_buffer = 2

p = pyaudio.PyAudio()
audio_stream = p.open(format=audio_format,
                      channels=audio_channels,
                      rate=audio_rate,
                      input=True,
                      frames_per_buffer=audio_frames_per_buffer)


def generate_frames():
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        else:
            # Ses verisini oku
            audio_data = audio_stream.read(audio_chunk_size)

            # Video frame ve sesi birleştir
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n' +
                   b'Content-Type: audio/wav\r\n\r\n' + audio_data + b'\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
