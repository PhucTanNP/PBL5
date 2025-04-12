import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont

class DetectionView(QWidget):
    update_label_signal = pyqtSignal(str, float)  # Signal nhận dữ liệu

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.update_label_signal.connect(self.update_prediction)  # Kết nối signal

    def init_ui(self):
        """Khởi tạo giao diện hiển thị dự đoán"""
        self.setWindowTitle("Nhận diện biển báo")
        self.setGeometry(650, 100, 400, 200)
        self.setStyleSheet("background-color: white;")

        self.layout = QVBoxLayout()

        self.prediction_label = QLabel("Dự đoán: ")
        self.prediction_label.setFont(QFont("Arial", 20, QFont.Weight.Bold))
        self.prediction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.prediction_label)

        self.alert_label = QLabel("")
        self.alert_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.alert_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.alert_label.setStyleSheet("color: red;")
        self.layout.addWidget(self.alert_label)

        self.setLayout(self.layout)

    def update_prediction(self, label, confidence):
        """Cập nhật nhãn dự đoán"""
        self.prediction_label.setText(f"Dự đoán: {label} ({confidence:.2f})")

# Chạy thử
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DetectionView()
    window.show()
    sys.exit(app.exec())
