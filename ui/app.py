from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from ui.worker import VideoWorker

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.setWindowTitle("Drone Tracker")
        self.setMinimumSize(900, 700)
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)

        #Video 
        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setStyleSheet("background-color: black;")
        self.video_label.setMinimumHeight(500)
        main_layout.addWidget(self.video_label)

        #Info Panel
        info_layout = QHBoxLayout()
        self.fps_label = QLabel("Fps: -")
        self.drone_label = QLabel("Detected: -")
        self.conf_label = QLabel("Conf: -")
        info_layout.addWidget(self.fps_label)
        info_layout.addWidget(self.drone_label)
        info_layout.addWidget(self.conf_label)
        main_layout.addLayout(info_layout)

        #Buttons
        button_layout = QHBoxLayout()
        self.select_button = QPushButton("Select Video")
        self.start_button = QPushButton("Start")
        self.stop_button = QPushButton("Stop")
        self.quit_button = QPushButton("Quit")

        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(False)

        self.select_button.clicked.connect(self.select_video)
        self.start_button.clicked.connect(self.start_video)
        self.stop_button.clicked.connect(self.stop_video)
        self.quit_button.clicked.connect(self.close)

        button_layout.addWidget(self.select_button)
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.quit_button)
        main_layout.addLayout(button_layout)


    def select_video(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Video" , "", "Video Files (*.mp4 *.avi *.mov)")

        if path:
            self.video_path = path
            self.start_button.setEnabled(True)

    def start_video(self):
        self.worker = VideoWorker(self.video_path)
        self.worker.frame_ready.connect(self.update_frame)
        self.worker.stats_ready.connect(self.update_stats)
        self.worker.start()
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_video(self):
        if self.worker:
            self.worker.stop()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)

    def update_frame(self, image):
        pixmap = QPixmap.fromImage(image)
        self.video_label.setPixmap(pixmap.scaled(
            self.video_label.size(), Qt.KeepAspectRatio))

    def update_stats(self, fps, drone_count, conf):
        self.fps_label.setText(f"FPS: {int(fps)}")
        self.drone_label.setText(f"Detected: {drone_count}")
        self.conf_label.setText(f"Score: %{int(conf * 100)}")