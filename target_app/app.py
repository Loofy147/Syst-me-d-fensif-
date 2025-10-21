from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# App setup
app = Flask(__name__)
db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Models ---
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# --- Routes ---
@app.route('/')
def index():
    return """
    <h1>Vulnerable Login</h1>
    <form action="/login" method="POST">
      <input type="text" name="username" placeholder="Username" /><br/>
      <input type="password" name="password" placeholder="Password" /><br/>
      <input type="submit" value="Login" />
    </form>
    """

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    try:
        # INTENTIONALLY VULNERABLE SQL QUERY
        query = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"
        result = db.session.execute(db.text(query))
        user = result.fetchone()

        if user:
            return jsonify({"message": "Login successful!", "user": username}), 200
        else:
            return jsonify({"message": "Invalid credentials"}), 401
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

def init_db():
    """Initializes the database and creates a default user."""
    with app.app_context():
        db.create_all()
        # Check if the admin user already exists
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', password='password123')
            db.session.add(admin_user)
            db.session.commit()
            print("Database initialized and admin user created.")

if __name__ == '__main__':
    init_db()
    # Note: Running in debug mode is not secure for production
    app.run(host='0.0.0.0', port=5000, debug=True)
