from flask import Flask

from .views import views
from .auth import auth

from flask_sqlalchemy import SQLAlchemy

from .models import User, Note

from os import path


db = SQLAlchemy
DB_NAME = "database.db"

def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'hshshsh'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

	db.init_app(app)

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	with app.app_context():
		db.create_all()

	return app
