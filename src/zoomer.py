import cv2

def zoom(frame, x1,y1, x2,y2):
    h,w = frame.shape[:2]

    cx = (x1 + x2) // 2 # center x
    cy = (y1 + y2) // 2 # center y

    pad = int(max(x2 - x1, y2 - y1) * 2.5) #2.5 times  zoom the size of the bounding box

    zx1 = max(0, cx - pad) #left side of the bounding box
    zy1 = max(0, cy - pad) #top side of the bounding box
    zx2 = min(w, cx + pad) #right side of the bounding box
    zy2 = min(h, cy + pad) #bottom side of the bounding box

    zoomed_frame = frame[zy1:zy2, zx1:zx2] #crop the frame to the size of the bounding box
    return cv2.resize(zoomed_frame, (w //3 ,h //3)) #resize the frame to 1/3 of the original size