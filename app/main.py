from flask import Flask, Blueprint
from .config import Config

def create_app():
	app = Flask(__name__)
	app.config.from_object(Config)


	from .views import web_bp
	from .api import api_bp
	app.register_blueprint(web_bp)
	app.register_blueprint(api_bp)

	return app
