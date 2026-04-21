import cv2
import time
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtGui import QImage
from src.detector import detect
from src.zoomer import zoom
from src.display import draw

class VideoWorker(QThread):
    frame_ready = pyqtSignal(QImage)
    stats_ready = pyqtSignal(float, int, float)

    def __init__(self, video_path):
        super().__init__()
        self.video_path = video_path
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(self.video_path)
        prev_time = time.time()

        while self.running:
            ret, frame = cap.read()

            if not ret:
                break

            curr_time = time.time()
            fps = 1 / (curr_time - prev_time + 0.0001)
            prev_time = curr_time

            # Her frame'de tespit yap, sonucu hemen kullan
            result = detect(frame)

            drone_count = 0
            conf = 0.0

            if result is not None:
                x1, y1, x2, y2, conf = result
                drone_count = 1
                frame = draw(frame, x1, y1, x2, y2, conf)
                frame = zoom(frame, x1, y1, x2, y2)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            image = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)
            self.frame_ready.emit(image)
            self.stats_ready.emit(fps, drone_count, conf)

        cap.release()

    def stop(self):
        self.running = False