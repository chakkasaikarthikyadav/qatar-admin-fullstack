from flask import Blueprint, request, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import Admin
from extensions import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json

    if not all([data.get('name'), data.get('email'), data.get('password'), data.get('confirm')]):
        return {"error": "All fields required"}, 400

    if data['password'] != data['confirm']:
        return {"error": "Passwords do not match"}, 400

    if len(data['password']) < 8:
        return {"error": "Password must be 8+ chars"}, 400

    if Admin.query.filter_by(email=data['email']).first():
        return {"error": "Email already exists"}, 400

    user = Admin(
        name=data['name'],
        email=data['email'],
        password=generate_password_hash(data['password'])
    )

    db.session.add(user)
    db.session.commit()

    return {"message": "Signup successful"}

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json

    user = Admin.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password, data['password']):
        return {"error": "Invalid email or password"}, 401

    session['admin_id'] = user.id

    if data.get("remember"):
        session.permanent = True

    return {"message": "Login successful"}

@auth_bp.route('/logout')
def logout():
    session.clear()
    return {"message": "Logged out"}

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot():
    return {"message": "If email exists, reset link sent"}