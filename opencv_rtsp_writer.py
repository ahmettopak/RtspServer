import cv2
import numpy as np
import pyautogui
import time
from multiprocessing import Process, Queue

# Ekran çözünürlüğü
screen_width, screen_height = pyautogui.size()

# RTSP sunucu ayarları
rtsp_url = "rtsp://localhost:8554/screen"
fps = 30
video_codec = cv2.VideoWriter_fourcc(*"H264")

# Ekran görüntüsü alma fonksiyonu
def capture_screen(queue):
    while True:
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        queue.put(frame)

# RTSP sunucu fonksiyonu
def start_rtsp_server(queue):
    server = cv2.VideoWriter(rtsp_url, video_codec, fps, (screen_width, screen_height))

    while True:
        if not queue.empty():
            frame = queue.get()
            server.write(frame)

# Ana program
if __name__ == "__main__":
    # Görüntü kuyruğu
    image_queue = Queue()

    # Ekran görüntüsü alma işlemi
    screen_capture_process = Process(target=capture_screen, args=(image_queue,))
    screen_capture_process.start()

    # RTSP sunucu işlemi
    rtsp_server_process = Process(target=start_rtsp_server, args=(image_queue,))
    rtsp_server_process.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Program kapatıldığında işlemleri sonlandır
        screen_capture_process.terminate()
        rtsp_server_process.terminate()
