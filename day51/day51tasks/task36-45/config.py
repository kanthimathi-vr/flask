import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'secretkey123')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///users.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
