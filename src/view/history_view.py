# View for history logs
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget
from src.model.traffic_sign_model import TrafficSignModel

class HistoryView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        """Khởi tạo giao diện lịch sử dự đoán"""
        self.setWindowTitle("Lịch sử dự đoán")
        self.setGeometry(200, 100, 400, 300)
        self.setStyleSheet("background-color: white;")

        self.layout = QVBoxLayout()

        self.title_label = QLabel("Lịch sử nhận diện")
        self.title_label.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        self.layout.addWidget(self.title_label)

        self.history_list = QListWidget()
        self.layout.addWidget(self.history_list)

        self.setLayout(self.layout)
        self.load_history()

    def load_history(self):
        """Tải lịch sử từ database"""
        model = TrafficSignModel()
        history = model.get_history()
        for item in history:
            self.history_list.addItem(f"{item[1]} - {item[2]:.2f} - {item[3]}")

# Chạy riêng
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HistoryView()
    window.show()
    sys.exit(app.exec())
