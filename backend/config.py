import os


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///clothing_store.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your_secret_key'
    current_directory = os.getcwd()
    UPLOAD_FOLDER = os.path.join(current_directory, 'uploads')
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}