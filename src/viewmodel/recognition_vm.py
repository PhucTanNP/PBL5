# ViewModel: Traffic Sign Recognition Logic
from PyQt6.QtCore import QObject, pyqtSignal
from src.model.traffic_sign_model import TrafficSignModel
import cv2
from ultralytics import YOLO

class RecognitionViewModel(QObject):
    sign_detected = pyqtSignal(str, float)  # Gửi tín hiệu khi nhận diện biển báo

    def __init__(self):
        super().__init__()
        self.model = TrafficSignModel()
        self.yolo = YOLO("models/yolo_model.pt")  # Load mô hình YOLO

    def recognize_sign(self, frame):
        """Nhận diện biển báo từ khung hình"""
        results = self.yolo(frame)
        for result in results:
            for box in result.boxes:
                label = result.names[int(box.cls)]
                confidence = float(box.conf)
                self.model.save_sign(label, confidence)
                self.sign_detected.emit(label, confidence)  # Phát tín hiệu
