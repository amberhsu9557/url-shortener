import requests
import os
from datetime import timedelta
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, render_template, jsonify

from flask_babel import Babel
from flask_wtf.csrf import CSRFProtect


babel = Babel()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', default='XFRAOpmX8DOg1Q1VLk6tCaD17KacVQUe')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=14)
    app.config['WTF_CSRF_ENABLED'] = True
    register_logger(app)
    register_extensions(app)
    register_errorhandlers(app)

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/healthz/liveness")
    def liveness():
        return jsonify({"status": "OK", "code": 200}), 200

    @app.route("/healthz/readiness")
    def readiness():
        return jsonify({"status": "OK", "code": 200}), 200

    return app

def register_logger(app):
    log_dir = '/tmp/logs'
    log_level = logging.DEBUG if app.debug else logging.WARNING
    handler = TimedRotatingFileHandler(os.path.join(log_dir, 'flask.log'), 
        when="D", interval=1, backupCount=5, encoding="UTF-8", delay=False, utc=False)
    handler.setLevel(log_level)
    handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s()][%(levelname)s] %(message)s'))
    app.logger.addHandler(handler)

def register_extensions(app):
    """Register extensions with the Flask application."""
    babel.init_app(app)
    csrf.init_app(app)


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