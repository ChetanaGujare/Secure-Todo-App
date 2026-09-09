import sqlite3
import bcrypt
from flask import Flask, request, jsonify, session, g, render_template
from functools import wraps
import os

app = Flask(__name__)
app.secret_key = 'your-super-secret-key-change-this-in-production'  # production mein change karein
app.config['SESSION_TYPE'] = 'filesystem'

# ----- Database Setup -----
DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        # Todos table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS todos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                done BOOLEAN DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
            )
        ''')
        db.commit()

# Initialize database when app starts
init_db()

# ----- Decorator: Login Required -----
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

# ----- Helper: Get current user -----
def get_current_user():
    user_id = session.get('user_id')
    if not user_id:
        return None
    db = get_db()
    user = db.execute('SELECT id, username FROM users WHERE id = ?', (user_id,)).fetchone()
    return user

# ----- Routes -----

# 1. Register
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if len(username) < 3 or len(password) < 4:
        return jsonify({'error': 'Username min 3, Password min 4 characters'}), 400

    db = get_db()
    # Check if user exists
    existing = db.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
    if existing:
        return jsonify({'error': 'Username already taken'}), 400

    # Hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    db.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed))
    db.commit()
    return jsonify({'message': 'User created successfully'}), 201

# 2. Login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    db = get_db()
    user = db.execute('SELECT id, username, password_hash FROM users WHERE username = ?', (username,)).fetchone()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    # Check password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
        return jsonify({'error': 'Invalid credentials'}), 401

    # Set session cookie
    session['user_id'] = user['id']
    session.permanent = True
    return jsonify({'message': 'Login successful', 'username': user['username']}), 200

# 3. Check current user (for frontend to verify)
@app.route('/api/me', methods=['GET'])
def me():
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401
    return jsonify({'username': user['username']}), 200

# 4. Logout
@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'}), 200

# 5. Get all todos
@app.route('/api/todos', methods=['GET'])
@login_required
def get_todos():
    user = get_current_user()
    db = get_db()
    todos = db.execute('SELECT id, text, done FROM todos WHERE user_id = ? ORDER BY id DESC', (user['id'],)).fetchall()
    return jsonify({'todos': [dict(row) for row in todos]}), 200

# 6. Add todo
@app.route('/api/todos', methods=['POST'])
@login_required
def add_todo():
    user = get_current_user()
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    db = get_db()
    db.execute('INSERT INTO todos (user_id, text) VALUES (?, ?)', (user['id'], text))
    db.commit()

    # Return updated list
    todos = db.execute('SELECT id, text, done FROM todos WHERE user_id = ? ORDER BY id DESC', (user['id'],)).fetchall()
    return jsonify({'todos': [dict(row) for row in todos]}), 201

# 7. Toggle todo
@app.route('/api/todos/<int:todo_id>/toggle', methods=['PATCH'])
@login_required
def toggle_todo(todo_id):
    user = get_current_user()
    db = get_db()
    # Ensure todo belongs to user
    todo = db.execute('SELECT id FROM todos WHERE id = ? AND user_id = ?', (todo_id, user['id'])).fetchone()
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    db.execute('UPDATE todos SET done = NOT done WHERE id = ?', (todo_id,))
    db.commit()

    todos = db.execute('SELECT id, text, done FROM todos WHERE user_id = ? ORDER BY id DESC', (user['id'],)).fetchall()
    return jsonify({'todos': [dict(row) for row in todos]}), 200

# 8. Delete todo
@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@login_required
def delete_todo(todo_id):
    user = get_current_user()
    db = get_db()
    db.execute('DELETE FROM todos WHERE id = ? AND user_id = ?', (todo_id, user['id']))
    db.commit()

    todos = db.execute('SELECT id, text, done FROM todos WHERE user_id = ? ORDER BY id DESC', (user['id'],)).fetchall()
    return jsonify({'todos': [dict(row) for row in todos]}), 200

# ----- Serve Frontend (index.html) -----
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)