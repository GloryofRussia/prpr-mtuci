from ultralytics import YOLO
import cv2

model = YOLO("yolov8n.pt")

def count_people(video_path: str) -> int:
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise RuntimeError("Cannot open video")

    max_people = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            results = model(frame)[0]
            persons = [obj for obj in results.boxes if int(obj.cls) == 0]
            max_people = max(max_people, len(persons))
        except Exception:
            raise RuntimeError("YOLO inference failed")

    cap.release()
    return max_people