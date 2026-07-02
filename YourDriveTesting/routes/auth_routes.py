from flask import Blueprint, request, jsonify
from models.user import User
from models.db import db
from flask_bcrypt import Bcrypt
from utils.auth_helper import generate_token

auth = Blueprint("auth", __name__)
bcrypt = Bcrypt()

@auth.route("/register", methods=["POST"])
def register():
    data = request.json

    hashed_pw = bcrypt.generate_password_hash(data["password"]).decode("utf-8")

    user = User(
        name=data["name"],
        email=data["email"],
        password=hashed_pw,
        role="user"
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered"})


@auth.route("/login", methods=["POST"])
def login():
    data = request.json

    user = User.query.filter_by(email=data["email"]).first()

    if user and bcrypt.check_password_hash(user.password, data["password"]):
        token = generate_token(user.id, user.role)
        return jsonify({"token": token, "role": user.role})

    return jsonify({"message": "Invalid credentials"})