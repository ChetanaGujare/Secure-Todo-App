📋 Secure Todo App
A full‑stack Todo application with user authentication, session management, and a beautiful glass‑morphism UI.
Built with Flask (Python) and vanilla HTML/CSS/JavaScript.
✨ Features
🔐 User Registration – passwords are securely hashed with bcrypt

🍪 Session‑based Login – persistent cookies keep you logged in

🚫 Protected Todo Routes – every API endpoint is guarded with @login_required

✅ Full CRUD – create, toggle (done/undone), and delete your todos

🧹 Logout – instantly clears the session

🎨 Modern UI – glass‑morphism design, fully responsive, with toast notifications

💾 SQLite Database – lightweight and portable, auto‑created on first run

🧱 Tech Stack
Layer	Technology
Backend	Python 3.8+ + Flask
Database	SQLite3
Password	bcrypt (hash + salt)
Frontend	HTML5, CSS3, Vanilla JavaScript
Icons	Font Awesome 6
Font	Google Fonts (Inter)
Styling	Glass‑morphism, custom CSS
📁 Project Structure
text
todo_secure_app/
│
├── app.py                 # Flask backend (routes, DB, auth)
├── database.db            # SQLite file (auto‑created)
├── .gitignore             # Ignore unnecessary files
├── README.md              # This file
└── templates/
    └── index.html         # Frontend (all CSS + JS in one file)
🚀 Getting Started
Prerequisites
Python 3.8 or higher

pip (Python package manager)

Installation
Clone the repository

bash
git clone https://github.com/your-username/todo-secure-app.git
cd todo-secure-app
Create a virtual environment (recommended)

bash
python -m venv venv
# Activate it:
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate
Install dependencies

bash
pip install flask bcrypt
Run the application

bash
python app.py
You should see:

text
* Running on http://127.0.0.1:5000
Open your browser and visit: http://127.0.0.1:5000

🔌 API Endpoints
All endpoints return JSON and (except for register and login) require a valid session cookie.

Method	Endpoint	Description	Auth required
POST	/api/register	Register a new user	❌
POST	/api/login	Login, sets a session cookie	❌
GET	/api/me	Get current user information	❌ (checks)
POST	/api/logout	Logout and clear session	✅
GET	/api/todos	Fetch all todos of logged‑in user	✅
POST	/api/todos	Add a new todo (body: {text})	✅
PATCH	/api/todos/<id>/toggle	Toggle the done status	✅
DELETE	/api/todos/<id>	Delete a todo by its ID	✅
🧪 Testing the Application
Register a new user (username ≥ 3 chars, password ≥ 4 chars).

Login with your credentials – you'll be redirected to the Todo section.

Add a few tasks, click the circle to mark them done, or delete them.

Click Logout to clear your session and return to the login screen.

Try accessing any /api/todos endpoint directly in the browser – you'll get a 401 Unauthorized error.

Make sure bcrypt is installed: pip install bcrypt

In VS Code, select the correct Python interpreter (Ctrl+Shift+P → Python: Select Interpreter)

❌ TemplateNotFound: index.html
Ensure the folder is named templates (lowercase) and located in the same directory as app.py.

❌ Port 5000 already in use
Change the port in app.py (line at the bottom) to a different number, e.g. port=5001, and open http://localhost:5001.

❌ database.db is not created
The database is automatically created on first run. If it fails, check write permissions in the project folder.

📝 Developer Notes
The secret_key in app.py is for development – always change it in production.

The database.db file is local and not meant to be shared. It is ignored by .gitignore.

Passwords are hashed with bcrypt – plain‑text passwords are never stored.

The frontend is fully self‑contained in index.html; no build tools are required.

🤝 Contributing
Contributions are welcome! Feel free to open issues or submit pull requests.

Fork the repository.

Create your feature branch: git checkout -b feature/your-feature

Commit your changes: git commit -m 'Add some feature'

Push to the branch: git push origin feature/your-feature

Open a pull request.

📄 License
This project is open‑source and available under the MIT License.
You are free to use, modify, and distribute it as per the license terms.

🙌 Acknowledgements
Flask – lightweight web framework

bcrypt – password hashing

Font Awesome – beautiful icons

Google Fonts – Inter font family

Made with ❤️ by Chetana 
Happy coding! 🚀
