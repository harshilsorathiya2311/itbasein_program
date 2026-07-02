from models.db import db

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    car_id = db.Column(db.Integer)
    test_drive_date = db.Column(db.String(50))
    status = db.Column(db.String(20), default="Pending")
    