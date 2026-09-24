import sqlite3
import os
import tempfile
from datetime import datetime

# In serverless environments like Vercel, the project root is read-only.
# We store the sqlite DB in the OS temp directory (/tmp).
if os.environ.get('VERCEL') or os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
    DB_NAME = os.path.join(tempfile.gettempdir(), "signup.db")
else:
    DB_NAME = "signup.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            password TEXT NOT NULL,
            registration_date TEXT NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            image_path TEXT NOT NULL,
            model_used TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL,
            date TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_user(name, username, email, phone, password):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        reg_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO users (name, username, email, phone, password, registration_date) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, username, email, phone, password, reg_date))
        conn.commit()
        conn.close()
        return True, "User registered successfully."
    except sqlite3.IntegrityError:
        return False, "Username or Email already exists."
    except Exception as e:
        return False, str(e)

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    return user is not None

def get_all_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name, username, email, phone, registration_date FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def save_prediction(username, image_path, model_used, prediction, confidence):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO predictions (username, image_path, model_used, prediction, confidence, date) VALUES (?, ?, ?, ?, ?, ?)",
                   (username, image_path, model_used, prediction, confidence, date))
    conn.commit()
    conn.close()

def get_user_predictions(username, search_query=""):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    if search_query:
        query = "%" + search_query + "%"
        cursor.execute("SELECT image_path, model_used, prediction, confidence, date FROM predictions WHERE username=? AND (date LIKE ? OR model_used LIKE ? OR prediction LIKE ?) ORDER BY date DESC", (username, query, query, query))
    else:
        cursor.execute("SELECT image_path, model_used, prediction, confidence, date FROM predictions WHERE username=? ORDER BY date DESC", (username,))
    preds = cursor.fetchall()
    conn.close()
    return preds

def get_total_users():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_total_predictions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM predictions")
    count = cursor.fetchone()[0]
    conn.close()
    return count
