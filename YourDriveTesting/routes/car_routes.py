from flask import Blueprint, request, jsonify
from models.car import Car
from models.db import db

car = Blueprint("car", __name__)

@car.route("/add", methods=["POST"])
def add_car():
    data = request.json

    new_car = Car(**data)
    db.session.add(new_car)
    db.session.commit()

    return jsonify({"message": "Car added"})