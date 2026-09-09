"""
Secure Todo API with Flask, MySQL, and bcrypt.
Uses connection pooling and environment variables.
"""
import os
import bcrypt
from flask import Flask, request, jsonify, session, g, render_template  # ✅ render_template included
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'mysql+pymysql://root:password@localhost/todo_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
db = SQLAlchemy(app)

# ------------------------- Models -------------------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'username': self.username}

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    text = db.Column(db.String(255), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def to_dict(self):
        return {'id': self.id, 'text': self.text, 'done': self.done}

# Create tables (run once)
with app.app_context():
    db.create_all()

# ------------------------- Decorators -------------------------
def login_required(f):
    """Decorator to require a valid session."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Return current user object or None."""
    user_id = session.get('user_id')
    if user_id:
        return User.query.get(user_id)
    return None

# ------------------------- Routes -------------------------
@app.route('/api/register', methods=['POST'])
def register():
    """
    Register a new user.
    Expects JSON: { "username": "x", "password": "y" }
    """
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400
    if len(username) < 3 or len(password) < 4:
        return jsonify({'error': 'Username min 3, Password min 4 chars'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already taken'}), 400

    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(username=username, password_hash=hashed.decode('utf-8'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    """Login and set session cookie."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'Invalid credentials'}), 401

    if not bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
        return jsonify({'error': 'Invalid credentials'}), 401

    session['user_id'] = user.id
    session.permanent = True
    return jsonify({'message': 'Login successful', 'username': user.username}), 200

@app.route('/api/me', methods=['GET'])
def me():
    """Return current user info."""
    user = get_current_user()
    if not user:
        return jsonify({'error': 'Not logged in'}), 401
    return jsonify({'username': user.username}), 200

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    """Clear session."""
    session.clear()
    return jsonify({'message': 'Logged out'}), 200

# ------------------------- Todo CRUD -------------------------
@app.route('/api/todos', methods=['GET'])
@login_required
def get_todos():
    """Get all todos for the logged-in user."""
    user = get_current_user()
    todos = Todo.query.filter_by(user_id=user.id).order_by(Todo.id.desc()).all()
    return jsonify({'todos': [t.to_dict() for t in todos]}), 200

@app.route('/api/todos', methods=['POST'])
@login_required
def add_todo():
    """Create a new todo."""
    user = get_current_user()
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({'error': 'Text is required'}), 400

    todo = Todo(user_id=user.id, text=text, done=False)
    db.session.add(todo)
    db.session.commit()

    todos = Todo.query.filter_by(user_id=user.id).order_by(Todo.id.desc()).all()
    return jsonify({'todos': [t.to_dict() for t in todos]}), 201

@app.route('/api/todos/<int:todo_id>/toggle', methods=['PATCH'])
@login_required
def toggle_todo(todo_id):
    """Toggle done status of a todo."""
    user = get_current_user()
    todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    todo.done = not todo.done
    db.session.commit()

    todos = Todo.query.filter_by(user_id=user.id).order_by(Todo.id.desc()).all()
    return jsonify({'todos': [t.to_dict() for t in todos]}), 200

@app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
@login_required
def delete_todo(todo_id):
    """Delete a todo."""
    user = get_current_user()
    todo = Todo.query.filter_by(id=todo_id, user_id=user.id).first()
    if not todo:
        return jsonify({'error': 'Todo not found'}), 404

    db.session.delete(todo)
    db.session.commit()

    todos = Todo.query.filter_by(user_id=user.id).order_by(Todo.id.desc()).all()
    return jsonify({'todos': [t.to_dict() for t in todos]}), 200

# ------------------------- Frontend -------------------------
@app.route('/')
def index():
    """Serve the frontend."""
    return render_template('index.html')

# ------------------------- Run -------------------------
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)