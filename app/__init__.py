from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .models import db
from .application import main_page

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()
    app.register_blueprint(main_page) #register all the routes
    
    return app
