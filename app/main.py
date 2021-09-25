from flask import Flask, Blueprint
from .config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	migrate.init_app(app, db)
	from .views import web_bp
	from .api import api_bp
	app.register_blueprint(web_bp)
	app.register_blueprint(api_bp)

	return app
