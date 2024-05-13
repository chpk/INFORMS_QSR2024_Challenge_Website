import sqlite3

DATABASE_LOCATION = 'users.db'

# Context manager for SQLite database connections
class DatabaseContextManager:
    def __enter__(self):
        self.conn = sqlite3.connect(DATABASE_LOCATION)
        self.cursor = self.conn.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.conn.close()

# Function to create users table
def create_table():
    with DatabaseContextManager() as db:
        db.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

# Function to add a new user
def add_userdata(username, password):
    with DatabaseContextManager() as db:
        db.execute('INSERT INTO userstable(username, password) VALUES (?,?)', (username, password))

# Function for user login
def login_user(username, password):
    with DatabaseContextManager() as db:
        db.execute('SELECT * FROM userstable WHERE username =? AND password = ?', (username, password))
        data = db.fetchall()
    return data
