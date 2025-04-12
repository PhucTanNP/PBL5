import sys
import os
import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt, pyqtSignal
from ultralytics import YOLO
from detection_view import DetectionView  # Import DetectionView để cập nhật kết quả

# Đường dẫn đến mô hình YOLO và nhãn
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, r"D:\My folder\HK8\PBL5\PBL\traffic_sign_recognition\models\best.pt")
LABELS_PATH = os.path.join(BASE_DIR, r"D:\My folder\HK8\PBL5\PBL\traffic_sign_recognition\data\labels.txt")

class RecognitionView(QWidget):
    update_detection_signal = pyqtSignal(str, float)  # Signal gửi kết quả nhận diện

    def __init__(self, vehicle_type):
        super().__init__()
        self.vehicle_type = vehicle_type
        self.cap = None
        self.model = YOLO(MODEL_PATH)  # Load mô hình YOLOv8
        self.labels = self.load_labels()  # Đọc danh sách nhãn
        self.detection_window = None  # Cửa sổ detection_view.py

        self.init_ui()
        self.init_camera()

    def load_labels(self):
        """Đọc danh sách nhãn từ labels.txt"""
        if not os.path.exists(LABELS_PATH):
            print("⚠️ Không tìm thấy labels.txt!")
            return []
        with open(LABELS_PATH, "r", encoding="utf-8") as f:
            return [line.strip() for line in f.readlines()]

    def init_ui(self):
        """Khởi tạo giao diện nhận diện"""
        self.setWindowTitle(f"Nhận diện biển báo - {self.vehicle_type}")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: white;")

        self.layout = QVBoxLayout()

        self.title_label = QLabel(f"Nhận diện biển báo cho {self.vehicle_type}")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        # Camera View
        self.camera_label = QLabel()
        self.camera_label.setStyleSheet("border: 2px solid black; background-color: #f0f0f0; min-height: 400px;")
        self.camera_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.camera_label)

        self.setLayout(self.layout)

        # Kết nối tín hiệu để cập nhật `detection_view.py`
        self.update_detection_signal.connect(self.update_detection_window)

    def init_camera(self):
        """Khởi động camera"""
        self.cap = cv2.VideoCapture(0)  # Mở camera
        if not self.cap.isOpened():
            self.camera_label.setText("Không thể mở camera")
            return

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_frame)
        self.timer.start(30)  # 30ms mỗi khung hình

    def capture_frame(self):
        """Nhận diện biển báo từ camera theo thời gian thực"""
        if self.cap is None or not self.cap.isOpened():
            return

        ret, frame = self.cap.read()
        if not ret:
            self.camera_label.setText("Lỗi khi lấy khung hình từ camera")
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model.predict(frame_rgb)  # Dự đoán với YOLOv8

        detected_label = None
        detected_confidence = 0

        # Vẽ bounding box và lấy nhãn dự đoán
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])  # Lấy tọa độ hộp
                cls = int(box.cls[0])  # Lấy class dự đoán
                label = self.labels[cls] if cls < len(self.labels) else "Unknown"  # Lấy tên biển báo
                conf = box.conf[0]  # Độ chính xác

                # Vẽ bounding box lên ảnh
                cv2.rectangle(frame_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame_rgb, f"{label} ({conf:.2f})", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # Lưu nhãn biển báo mới nhất
                if conf > detected_confidence:
                    detected_label = label
                    detected_confidence = conf

        # Hiển thị ảnh trên giao diện
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        qimg = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
        self.camera_label.setPixmap(QPixmap.fromImage(qimg))

        # Gửi kết quả tới detection_view.py (nếu có biển báo)
        if detected_label:
            self.update_detection_signal.emit(detected_label, detected_confidence)

    def update_detection_window(self, label, confidence):
        """Cập nhật cửa sổ `detection_view.py` theo thời gian thực"""
        if self.detection_window is None:
            self.detection_window = DetectionView()
            self.detection_window.show()

        self.detection_window.update_prediction(label, confidence)

    def closeEvent(self, event):
        """Giải phóng camera khi đóng ứng dụng"""
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        if hasattr(self, 'timer'):
            self.timer.stop()
        event.accept()

# Chạy thử riêng màn hình nhận diện
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecognitionView("Ô Tô")
    window.show()
    sys.exit(app.exec())
