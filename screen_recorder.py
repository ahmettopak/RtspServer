import cv2
import numpy as np
import pyautogui

# Ekran genişlik ve yükseklik değerlerini al
screen_width, screen_height = pyautogui.size()

# Video çıkışı için VideoWriter nesnesini oluştur
output_video = cv2.VideoWriter('screen_capture.avi', cv2.VideoWriter_fourcc(*'XVID'), 10.0, (screen_width, screen_height))

try:
    while True:
        # Ekran görüntüsünü al
        screenshot = pyautogui.screenshot()

        # OpenCV formatına dönüştür
        frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

        # Video dosyasına frame'i yaz
        output_video.write(frame)

        # Ekran görüntüsünü göster
        cv2.imshow('Screen Capture', frame)

        # Herhangi bir tuşa basıldığında döngüyü sonlandır
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Video dosyasını kapat
    output_video.release()

    # OpenCV penceresini kapat
    cv2.destroyAllWindows()
