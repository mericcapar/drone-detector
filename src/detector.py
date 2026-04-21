from ultralytics import YOLO

model = YOLO("best.pt")
model.to("mps")

def detect(frame):
    results = model(frame, conf=0.3, verbose=False)[0]
    
    best_box = None
    best_conf = 0

    for box in results.boxes:
        conf = float(box.conf[0])
        if conf > best_conf:
            best_conf = conf
            best_box = box

    if best_box is None:
        return None

    x1, y1, x2, y2 = map(int, best_box.xyxy[0])
    return x1, y1, x2, y2, best_conf