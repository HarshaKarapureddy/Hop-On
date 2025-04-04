import sqlite3
from flask import Flask

app = Flask(__name__)

# Initialize global variables
current_user = None
current_user_id = None

def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

def login(username, password):
    global current_user, current_user_id
    
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT id, username FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    
    if user is not None:
        current_user_id, current_user = user
        return True
    return False

def create_user(username, password):
    # Check for minimum length requirements
    if len(username) < 6:
        return False, "Username must be at least 6 characters long"
        
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    # Check if username and password are the same
    if username == password:
        return False, "Username and password cannot be the same"
        
    try:
        with sqlite3.connect('users.db') as conn:
            c = conn.cursor()
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
        return True, "User created successfully"
    except sqlite3.IntegrityError:
        return False, "Username already exists"
 
def logout():
    global current_user, current_user_id
    current_user = None
    current_user_id = None
    return True

def is_logged_in():
    return current_user is not None

def get_current_user():
    return current_user

# Initialize the database
init_db()