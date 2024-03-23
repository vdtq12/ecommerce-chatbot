from flask import Flask
from .extensions import db
from .routes.main import main
import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI']=os.getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(main)

    return app

    
