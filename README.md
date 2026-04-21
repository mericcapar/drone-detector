# DroneTracker

A real-time drone detection and tracking application built with YOLOv8 and PyQt5.

## Features
- Real-time drone detection using YOLOv8
- Auto zoom on detected drone
- Desktop application with simple UI
- FPS and confidence score display
- Supports video files (mp4, avi, mov)

## Tech Stack
- Python
- YOLOv8 (Ultralytics)
- OpenCV
- PyQt5

## Installation

1. Clone the repository
git clone https://github.com/username/DroneTracker.git
cd DroneTracker
2. Install dependencies
pip install ultralytics opencv-python PyQt5
3. Download the model
Place your best.pt file in the root directory.
4. Run
python main.py


## Dataset
Trained on DroneSpotter dataset from Roboflow Universe.
https://universe.roboflow.com/test-ao5um/dronespotter-azabi

