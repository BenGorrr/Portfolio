from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_class):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    with app.app_context():
        db.create_all()
        db.session.commit()

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return app.config['STEAM_API_KEY']
    return app
