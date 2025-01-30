import sqlite3, os
import datetime
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect("database/nepsetracker.db")
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
            print('Database connection closed.')

    def currentUtcTimestamp(self):
        utc_timestamp = datetime.datetime.now(datetime.UTC).replace(microsecond=0)
        return utc_timestamp

    def createTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            status BOOLEAN DEFAULT 0,
                            updated_at TIMESTAMP DEFAULT NULL,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        print("Users table is created.")

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stock_tracking (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        symbol TEXT NOT NULL,
                        min_target_price REAL NOT NULL,     
                        max_target_price REAL NOT NULL,
                        status BOOLEAN DEFAULT 0,
                        notified_at TIMESTAMP DEFAULT NULL,
                        updated_at TIMESTAMP DEFAULT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')
        print("Stock Tracking table is created.")
        self.connection.commit()

    def insertUser(self, username, email, password):
        self.cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        self.connection.commit()
        print('User created.')

    def updateUser(self, user_id, username, email):
        self.cursor.execute("UPDATE users SET username = ?, email = ? WHERE id = ?", (username, email, user_id))
        self.connection.commit()

    def getAllUsers(self):
        self.cursor.execute("SELECT * FROM users")
        users = self.cursor.fetchall()
        if users:
            return users
        else:
            return None


    def getUser(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ? LIMIT 1", (email,))
        user = self.cursor.fetchone()
        if user:
            return user
        else:
            return None


    def storePriceTracker(self, user_id, symbol, min_price, max_price, status):
        self.cursor.execute("INSERT INTO stock_tracking (user_id, symbol, min_target_price, max_target_price, status) VALUES (?, ?, ?, ?, ?)", (user_id, symbol.upper(), min_price, max_price, status))
        self.connection.commit()

    def geAllUserPriceTracker(self, user_id):
        self.cursor.execute("SELECT * FROM stock_tracking WHERE user_id = ?", (user_id,))
        price_tracks = self.cursor.fetchall()
        if price_tracks:
            return price_tracks
        else:
            return None

    def getUserActivePriceTracker(self, user_id):
        self.cursor.execute("SELECT * FROM stock_tracking WHERE user_id = ? AND status = '1'", (user_id,))
        price_tracks = self.cursor.fetchall()
        if price_tracks:
            return price_tracks
        else:
            return None

    def selectData(self):
        self.cursor.execute("SELECT * FROM stock_tracking")
        rows = self.cursor.fetchall()
        return rows

if __name__ == "__main__":
    db_manager = DatabaseManager()
    # db_manager.createTable()
    print(db_manager.currentUtcTimestamp())
    # data = db_manager.selectData()
    # for d in data:
    #     print(d[0])
