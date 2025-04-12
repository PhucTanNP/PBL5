# Database connection
import sqlite3

class Database:
    def __init__(self, db_name="data/traffic_signs.db"):
        """Kết nối với database SQLite"""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        """Tạo bảng lưu lịch sử biển báo nếu chưa có"""
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS signs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                confidence REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def save_sign(self, name, confidence):
        """Lưu biển báo vào database"""
        self.cursor.execute("INSERT INTO signs (name, confidence) VALUES (?, ?)", (name, confidence))
        self.conn.commit()

    def get_history(self):
        """Lấy danh sách biển báo đã nhận diện"""
        self.cursor.execute("SELECT * FROM signs ORDER BY timestamp DESC")
        return self.cursor.fetchall()

    def close(self):
        """Đóng kết nối database"""
        self.conn.close()
