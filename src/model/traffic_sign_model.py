# Model: Database & data management
from src.model.database import Database

class TrafficSignModel:
    def __init__(self):
        self.db = Database()

    def save_sign(self, name, confidence):
        """Lưu biển báo vào database"""
        self.db.save_sign(name, confidence)

    def get_history(self):
        """Lấy danh sách lịch sử biển báo"""
        return self.db.get_history()
