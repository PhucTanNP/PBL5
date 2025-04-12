import sys
from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from PBL.traffic_sign_recognition.src.view.detection_view import DetectionView
# from PBL.traffic_sign_recognition.src.view.history_view import HistoryView
from recognition_view import RecognitionView

def load_stylesheet():
    """Tải file QSS và áp dụng"""
    try:
        with open(r"D:\My folder\HK8\PBL5\PBL\traffic_sign_recognition\src\view\styles.qss", "r",encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print("⚠️ Không tìm thấy file styles.qss")
        return ""  # Tránh lỗi nếu file không tồn tại

class TrafficSignApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện chính"""
        self.setWindowTitle("NHẬN DIỆN BIỂN BÁO GIAO THÔNG")
        self.setGeometry(300, 300, 800, 400)
        self.setStyleSheet("background-color: #00FFFF;")

        # Layout chính
        main_layout = QVBoxLayout()

        # Tiêu đề
        title_label = QLabel("Hãy chọn loại phương tiện")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: black; margin-bottom: 20px;")
        main_layout.addWidget(title_label)

        # Layout cho các ô lựa chọn
        choice_layout = QHBoxLayout()

        # Ô lựa chọn "Ô Tô"
        car_button = QPushButton()
        car_button.setObjectName("carButton")  # Gán ID để QSS nhận diện
        car_button.setFixedSize(220, 220)

        car_icon = QLabel()
        car_pixmap = QPixmap(r"D:\My folder\HK8\PBL5\PBL\traffic_sign_recognition\assets\icons\oto.png")
        car_icon.setPixmap(car_pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        car_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        car_label = QLabel("Ô TÔ")
        car_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        car_layout = QVBoxLayout()
        car_layout.addWidget(car_icon)
        car_layout.addWidget(car_label)
        car_button.setLayout(car_layout)

        car_button.clicked.connect(lambda: self.open_recognition("Ô Tô"))
        choice_layout.addWidget(car_button)

        # Ô lựa chọn "Xe Tải"
        truck_button = QPushButton()
        truck_button.setObjectName("truckButton")  # Gán ID để QSS nhận diện
        truck_button.setFixedSize(220, 220)

        truck_icon = QLabel()
        truck_pixmap = QPixmap(r"D:\My folder\HK8\PBL5\PBL\traffic_sign_recognition\assets\icons\xetai.jpg")
        truck_icon.setPixmap(truck_pixmap.scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio))
        truck_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        truck_label = QLabel("XE TẢI")
        truck_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        truck_layout = QVBoxLayout()
        truck_layout.addWidget(truck_icon)
        truck_layout.addWidget(truck_label)
        truck_button.setLayout(truck_layout)

        truck_button.clicked.connect(lambda: self.open_recognition("Xe Tải"))
        choice_layout.addWidget(truck_button)

        # Thêm layout lựa chọn vào layout chính
        main_layout.addLayout(choice_layout)
        self.setLayout(main_layout)

    def open_recognition(self, vehicle_type):
        """Mở màn hình nhận diện biển báo giao thông"""
        self.recognition_window = RecognitionView(vehicle_type)
        # self.history_window = HistoryView()
        self.detection_window = DetectionView()

        self.recognition_window.show()
        # self.history_window.show()
        self.detection_window.show()
        self.close()  # Đóng cửa sổ chọn phương tiện

# Chạy ứng dụng
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())  # Tải và áp dụng QSS
    window = TrafficSignApp()
    window.show()
    sys.exit(app.exec())
