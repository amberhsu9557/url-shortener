import os
import requests
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, jsonify, redirect, url_for, render_template

from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect
# from flask_jwt_extended import JWTManager
# from flask_marshmallow import Marshmallow

from .config.config import config

db = SQLAlchemy()
cache = Cache()
babel = Babel()
csrf = CSRFProtect()
# jwt = JWTManager()
# ma = Marshmallow()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    register_logger(app)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    @app.route("/")
    def index():
        return jsonify({"status": "OK", "code": 200}), 200

    @app.route("/healthz/liveness")
    def liveness():
        return jsonify({"status": "OK", "code": 200}), 200

    @app.route("/healthz/readiness")
    def readiness():
        return jsonify({"status": "OK", "code": 200}), 200

    @app.route("/<string:req_key>", methods=["GET"])
    def getkey(req_key):
        return redirect(url_for('transfer.page_redirect', req_key=req_key))

    return app

def register_logger(app):
    log_dir = app.config["LOG_DIR"] if "LOG_DIR" in app.config else "/tmp/logs"
    log_level = logging.DEBUG if app.debug else logging.WARNING
    handler = TimedRotatingFileHandler(os.path.join(log_dir, 'flask.log'), 
        when="D", interval=1, backupCount=5, encoding="UTF-8", delay=False, utc=False)
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s()][%(levelname)s] %(message)s'))
    app.logger.addHandler(handler)

def register_extensions(app):
    """Register extensions with the Flask application."""
    cache.init_app(app)
    babel.init_app(app)
    csrf.init_app(app)
    # jwt.init_app(app)    
    # ma.init_app(app)
    db.init_app(app)
    # with app.app_context():
    #     db.create_all()

def register_blueprints(app):
    """Register blueprints with the Flask application."""
    from .transfer.views import transfer_bp

    app.register_blueprint(transfer_bp, url_prefix="/v1/api/transfer")   

def register_errorhandlers(app):
    """Register error handlers with the Flask application."""

    def render_error(e):
        return render_template("errors/%s.html" % e.code, error=e), e.code

    for e in [
        requests.codes.INTERNAL_SERVER_ERROR,
        requests.codes.NOT_FOUND,
        requests.codes.UNAUTHORIZED,
    ]:
        app.errorhandler(e)(render_error)
