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
                            fullname TEXT NOT NULL,
                            email TEXT NOT NULL UNIQUE,
                            password TEXT NOT NULL,
                            status BOOLEAN DEFAULT 0,
                            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        print("Users table is created.")

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sectors (
                        id  INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        print("Sectors table is created.")

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS securities(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        sector_id INTEGER NOT NULL,
                        security_name TEXT NOT NULL,
                        symbol TEXT NOT NULL UNIQUE,
                        website TEXT,
                        instrument_type TEXT NOT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (sector_id) REFERENCES sectors(id))''')
        print("securities table is created")

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS security_price_alerts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        security_id TEXT NOT NULL,
                        min_target_price REAL NOT NULL,     
                        max_target_price REAL NOT NULL,
                        status BOOLEAN DEFAULT 0,
                        notified_at TIMESTAMP DEFAULT NULL,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(id),
                        FOREIGN KEY (security_id) REFERENCES securities(id))''')
        print("Stock Tracking table is created.")
        self.connection.commit()

    # Sector Table
    def insertSector(self, name):
        self.cursor.execute("INSERT INTO sectors (name) VALUES (?)", (name,))
        self.connection.commit()
        print("Sector Stored.")

    # Securities Table
    def insertSecurity(self, sector_id, security_name, symbol, website, instrument_type):
        self.cursor.execute("INSERT INTO securities (sector_id, security_name, symbol, website, instrument_type) VALUES (?, ?, ?, ?, ?)", (sector_id, security_name, symbol, website, instrument_type))
        self.connection.commit()
        print("security is inserted")

    # Users Table
    def insertUser(self, username, fullname, email, password):
        self.cursor.execute("INSERT INTO users (username, fullname, email, password) VALUES (?, ?, ?, ?)", (username, fullname, email, password))
        self.connection.commit()
        print('User created.')

    def updateUser(self, user_id, fullname, username, email):
        self.cursor.execute("UPDATE users SET username = ?, fullname = ?, email = ? WHERE id = ?", (username, fullname, email, user_id))
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


    def storePriceTracker(self, user_id, security_id, min_price, max_price, status):
        self.cursor.execute("INSERT INTO security_price_alerts (user_id, security_id, min_target_price, max_target_price, status) VALUES (?, ?, ?, ?, ?)", (user_id, security_id, min_price, max_price, status))
        self.connection.commit()

    def geAllUserPriceTracker(self, user_id):
        self.cursor.execute("SELECT * FROM security_price_alerts WHERE user_id = ?", (user_id,))
        price_tracks = self.cursor.fetchall()
        if price_tracks:
            return price_tracks
        else:
            return None

    def getUserActivePriceTracker(self, user_id):
        self.cursor.execute("SELECT * FROM stock_price_alert WHERE user_id = ? AND status = '1'", (user_id,))
        price_tracks = self.cursor.fetchall()
        if price_tracks:
            return price_tracks
        else:
            return None

    def selectData(self, table_name):
        self.cursor.execute("SELECT * FROM " + table_name)
        rows = self.cursor.fetchall()
        return rows

if __name__ == "__main__":
    print("Welcome to Database Manager.")
    commands = "1> Create Database.\n2> Print All Data of table.\n?> Wild Card.\n"
    print(commands)
    i = input('Enter here: ')
    print("<------------------------------------->")

    db_manager = DatabaseManager()
    if i == '1':
        db_manager.createTable()
    elif i == '2':
        table_name = input('Enter table name: ')
        data = db_manager.selectData(table_name)
        for d in data:
            print(dict(d))
    else:
        print(db_manager.currentUtcTimestamp())

    print("<------------------------------------->")
    print("Closing database manager CLI.")
