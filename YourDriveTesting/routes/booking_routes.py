from flask import Blueprint, request, jsonify
from models.booking import Booking
from models.db import db

booking = Blueprint("booking", __name__)

@booking.route("/book", methods=["POST"])
def book():
    data = request.json

    b = Booking(**data)
    db.session.add(b)
    db.session.commit()

    return jsonify({"message": "Test drive booked"})