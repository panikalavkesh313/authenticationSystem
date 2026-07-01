from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from flask_cors import CORS
from datetime import timedelta

# -----------------------------
# App Configuration
# -----------------------------
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["JWT_SECRET_KEY"] = "your_super_secret_key_change_this"

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Allow React frontend
CORS(app)

# -----------------------------
# Database Model
# -----------------------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }


# Create database
with app.app_context():
    db.create_all()

# -----------------------------
# Home Route
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "message": "Flask Authentication API Running"
    })


# -----------------------------
# Register
# -----------------------------
@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    user = User.query.filter_by(email=email).first()

    if user:
        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 400

    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")

    new_user = User(
        name=name,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Registration Successful"
    })


# -----------------------------
# Login
# -----------------------------
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "success": False,
            "message": "Invalid Email"
        }), 401

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({
            "success": False,
            "message": "Wrong Password"
        }), 401

    # Identity must be a string
    token = create_access_token(identity=str(user.id))

    return jsonify({
        "success": True,
        "token": token,
        "user": user.to_dict()
    })


# -----------------------------
# Profile
# -----------------------------
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    # Convert string back to integer
    user_id = int(get_jwt_identity())

    user = User.query.get(user_id)

    if not user:
        return jsonify({
            "success": False,
            "message": "User Not Found"
        }), 404

    return jsonify({
        "success": True,
        "user": user.to_dict()
    })


# -----------------------------
# Logout
# -----------------------------
@app.route("/logout", methods=["POST"])
@jwt_required()
def logout():

    return jsonify({

        "success": True,

        "message": "Logout Successful"

    })


# -----------------------------
# Verify Token
# -----------------------------
@app.route("/verify-token")
@jwt_required()
def verify():

    return jsonify({

        "success": True,

        "message": "Token Valid"

    })


# -----------------------------
# Run Server
# -----------------------------
if __name__ == "__main__":
    app.run(
        debug=True,
        port=5000
    )