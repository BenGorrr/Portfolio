from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

class Account(db.Model):
    __tablename__ = "accounts"
    steamID = db.Column(db.String, primary_key=True, nullable=False)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    community_banned = db.Column(db.Boolean, nullable=False)
    vac_banned = db.Column(db.Boolean, nullable=False)
    numberOfVACBans = db.Column(db.Integer, nullable=False)
    daysSinceLastBan = db.Column(db.Integer, nullable=False)
    personaname =  db.Column(db.String, nullable=False)
