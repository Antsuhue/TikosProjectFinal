from flask import Flask
from .extensions import views
from .extensions.db import mongo

def create_app(config_object="tikos.config.settings"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    views.init_app(app)
    mongo.init_app(app)

    return app