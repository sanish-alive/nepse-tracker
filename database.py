import sqlite3, os
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect(os.getenv('SQLITE_DATABASE_NAME'))
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def __del__(self):
        if hasattr(self, 'connection') and self.connection:
            self.connection.close()
            print('Database connection closed.')
    

    def createTable(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL UNIQUE,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL)''')
        print("Users table is created.")
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS stock_tracking (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        symbol TEXT NOT NULL,
                        min_target_price REAL NOT NULL,     
                        max_target_price REAL NOT NULL,
                        status BOOLEAN DEFAULT 0,
                        FOREIGN KEY (user_id) REFERENCES users(id))''')
        print("Stock Tracking table is created.")

    def insertUser(self, username, email, password):
        self.cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
        self.connection.commit()
        print('User created.')

    def getUser(self, email):
        self.cursor.execute("SELECT * FROM users WHERE email = ? LIMIT 1", (email,))
        user = self.cursor.fetchone()
        if user:
            return user
        else:
            return None


    def insertData(self, symbol, min_price, max_price, email):
        self.cursor.execute("INSERT INTO stock_tracking VALUES (?, ?, ?, ?)", (symbol.upper(), min_price, max_price, email))
        self.connection.commit()
        print('Inserted.')

    def selectData(self):
        self.cursor.execute("SELECT * FROM stock_tracking")
        rows = self.cursor.fetchall()
        return rows

if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.createTable()
    # data = db_manager.selectData()
    # for d in data:
    #     print(d[0])
