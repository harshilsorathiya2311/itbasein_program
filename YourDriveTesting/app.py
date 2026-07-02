from flask import Flask
from models.db import db
from config import Config

from routes.auth import auth
from routes.car import car
from routes.booking import booking
from routes.dashboard import dashboard

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(car, url_prefix="/car")
app.register_blueprint(booking, url_prefix="/booking")
app.register_blueprint(dashboard)

@app.route("/")
def home():
    return "🚗 YourDrive System Running Successfully"

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)