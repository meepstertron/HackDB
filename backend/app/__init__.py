# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import redis
from rq import Queue
import os
from flask_cors import CORS

db = SQLAlchemy()
rq = None

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    CORS(app, supports_credentials=True)

    # Set up Redis Queue
    global rq
    redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')
    redis_conn = redis.from_url(redis_url)
    rq = Queue(connection=redis_conn)

    from .routes.main import main as main_blueprint
    from .routes.userdbs import udb as userdb_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(userdb_blueprint)

    from . import models 
    return app
