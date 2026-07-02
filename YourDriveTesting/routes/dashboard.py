from flask import Blueprint, jsonify
from models.user import User
from models.car import Car
from models.booking import Booking

dashboard = Blueprint("dashboard", __name__)

@dashboard.route("/admin/stats")
def stats():

    return jsonify({
        "users": User.query.count(),
        "cars": Car.query.count(),
        "bookings": Booking.query.count()
    })