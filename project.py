#!/usr/bin/env python2
import sys

from flask import Flask, redirect, url_for, flash, render_template
from flask_login import login_required, logout_user
from config import Config
from models import db, login_manager
from oauth import blueprint
from cli import create_db

# Disable https check for OAuth 2 since we are on dev environment
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(blueprint, url_prefix="/login")
app.cli.add_command(create_db)
db.init_app(app)
login_manager.init_app(app)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))


@app.route("/")
def index():
    return render_template("home.html")


# hook up extensions to app
db.init_app(app)
login_manager.init_app(app)

if __name__ == '__main__':
    if "--setup" in sys.argv:
        with app.app_context():
            db.create_all()
            db.session.commit()
            print("Database tables created")
    else:
        app.debug = True
        app.run(host='0.0.0.0', port=5000)