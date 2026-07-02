from models.db import db

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String(100))
    model = db.Column(db.String(100))
    price = db.Column(db.Float)
    fuel_type = db.Column(db.String(50))
    car_type = db.Column(db.String(50))