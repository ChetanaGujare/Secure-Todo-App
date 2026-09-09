🔐 Secure Todo App

A full‑stack Todo application with secure user authentication (session‑based, passwords hashed with bcrypt), full CRUD for todos, and a modern glass‑morphism UI.
Built with Flask (Python), MySQL (using SQLAlchemy + connection pooling), and vanilla HTML/CSS/JavaScript.

✨ Features
🔐 User registration & login – passwords hashed with bcrypt

🍪 Session management – cookies store authenticated state

🚫 Protected Todo routes – every endpoint is guarded with @login_required

✅ Full CRUD – create, toggle (done/undone), and delete todos

🧹 Logout – instantly clears the session

🎨 Glass‑morphism UI – responsive, with toast notifications

🗄️ MySQL database – using SQLAlchemy with connection pooling

🔒 Environment variables – secret key and database URL loaded from .env

🧱 Tech Stack
Layer	Technology
Backend	Python 3.8+ + Flask + SQLAlchemy
Database	MySQL 8.0+ (with pymysql)
Password	bcrypt (hash + salt)
Frontend	HTML5, CSS3, Vanilla JavaScript
Icons	Font Awesome 6
Font	Google Fonts (Inter)
Styling	Glass‑morphism, custom CSS
📁 Project Structure
text
todo_secure_app/
│
├── app.py                 # Flask backend (routes, models, auth)
├── .env                   # Environment variables (not committed)
├── .gitignore             # Ignore .env, __pycache__, etc.
├── requirements.txt       # Python dependencies
├── README.md              # This file
└── templates/
    └── index.html         # Frontend (all CSS + JS in one file)
🚀 Getting Started
Prerequisites
Python 3.8 or higher

MySQL Server 8.0 or higher (running locally or remotely)

pip (Python package manager)

Installation
Clone the repository

bash
git clone https://github.com/ChetanaGujare/Secure-Todo-App.git
cd Secure-Todo-App
Create and activate a virtual environment (recommended)

bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
Install dependencies

bash
pip install -r requirements.txt
(Or individually: flask flask-sqlalchemy pymysql bcrypt python-dotenv)

Set up the MySQL database

Create a database (e.g., todo_db):

sql
CREATE DATABASE todo_db;
Create a .env file in the project root with your credentials:

env
FLASK_SECRET_KEY=your-very-secret-key
DATABASE_URL=mysql+pymysql://username:password@host:3306/todo_db
Note: If your password contains special characters like @, #, or %, URL‑encode them (e.g., %40 for @).
Example: mysql+pymysql://root:p%40ssword@127.0.0.1:3306/todo_db

Run the application

bash
python app.py
You should see:

text
* Running on http://127.0.0.1:5000
Open your browser and visit http://127.0.0.1:5000

🔌 API Endpoints
All endpoints return JSON. Except register and login, all require a valid session cookie (automatically handled by the frontend).

Method	Endpoint	Description	Auth required
POST	/api/register	Register a new user	❌
POST	/api/login	Login, sets a session cookie	❌
GET	/api/me	Get current user info	❌ (checks)
POST	/api/logout	Logout and clear session	✅
GET	/api/todos	Fetch all todos for logged‑in user	✅
POST	/api/todos	Add a new todo (body: {text})	✅
PATCH	/api/todos/<id>/toggle	Toggle the done status	✅
DELETE	/api/todos/<id>	Delete a todo by ID	✅
🧪 Testing the Application
Register a new user (min 3‑char username, min 4‑char password).

Login with those credentials – you'll be redirected to the Todo dashboard.

Add a few tasks, click the circle to mark them done, or delete them.

Click Logout – session is cleared, and you're back to the login screen.

Try accessing /api/todos directly in the browser – you'll get a 401 Unauthorized error.

🔧 Troubleshooting
❌ Can't connect to MySQL server on '...'
Ensure MySQL server is running (net start MySQL on Windows, sudo systemctl start mysql on Linux).

Check that your database credentials in .env are correct.

Use 127.0.0.1 instead of localhost if you experience DNS resolution issues.

❌ ImportError: No module named ...
Make sure all dependencies are installed: pip install -r requirements.txt

❌ TemplateNotFound: index.html
Ensure the templates folder exists and is in the same directory as app.py.

❌ Secret key not loaded / DATABASE_URL not found
Verify that .env file is present in the project root and contains the correct keys.

The file name should be exactly .env (dot + env).

🛠️ Developer Notes
The FLASK_SECRET_KEY is used to sign session cookies – never commit the real one to version control.

The application uses SQLAlchemy connection pooling (pool_size=10, pool_recycle=3600) for better performance with MySQL.

Database tables (users and todos) are auto‑created on first run by db.create_all().

The frontend is a single HTML file (all CSS/JS included) – no build tools required.

🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

Fork the repository.

Create a feature branch: git checkout -b feature/your-feature

Commit your changes: git commit -m 'Add some feature'

Push to the branch: git push origin feature/your-feature

Open a pull request.

📄 License
This project is open‑source and available under the MIT License.
You are free to use, modify, and distribute it as per the license terms.

🙌 Acknowledgements
Flask – web framework

SQLAlchemy – ORM & connection pooling

bcrypt – password hashing

Font Awesome – icons

Google Fonts – Inter font family

Made with ❤️ by Chetana Gujare
Happy coding! 🚀


