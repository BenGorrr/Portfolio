from os import environ

class Config:
    STEAM_API_KEY = environ.get('STEAM_API_KEY')
    SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
