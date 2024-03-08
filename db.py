import sqlite3

conn = sqlite3.connect('biggiebot.db')
cursor = conn.cursor()

def create_tables():
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 1000,
            username TEXT
        )
        '''
    )
    conn.commit()   

def create_user(user_id, user_name):
    cursor.execute("INSERT INTO users (id, username) VALUES (?, ?)", (user_id, user_name))
    conn.commit()

def get_user_name(user_id) -> str | None:
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_user_balance(user_id) -> float | None:
    cursor.execute("SELECT balance FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def get_user(user_id) -> tuple | None:
    cursor.execute("SELECT username, balance FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    return result if result else None

def update_user_balance(user_id, balance):
    cursor.execute("UPDATE users SET balance = ? WHERE id = ?", (balance, user_id))
    conn.commit()
    return balance

create_tables()
print("Connection established")

