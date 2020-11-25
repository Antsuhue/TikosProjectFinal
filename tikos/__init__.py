from flask import Flask
from .extensions import views
from .extensions.db import mongo
from .functions import erro, login

def create_app(config_object="tikos.config.settings"):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "Secret"
    app.config.from_object(config_object)
    app.register_error_handler(404, erro.page_not_found)
    views.init_app(app)
    mongo.init_app(app)
    return app