class Config:
    SECRET_KEY = "yourdrive_secret_key"

    # PostgreSQL (change this later)
    SQLALCHEMY_DATABASE_URI = "sqlite:///yourdrive.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False