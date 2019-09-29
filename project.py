#!/usr/bin/env python2
import sys

from flask import Flask, redirect, url_for, flash, render_template
from flask_login import login_required, logout_user
from config import Config
from models import db, login_manager, User, Category, Item
from oauth import blueprint

# Disable https check for OAuth 2 since we are on dev environment
import os
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'


app = Flask(__name__)
app.config.from_object(Config)
app.register_blueprint(blueprint, url_prefix="/login")
db.init_app(app)
login_manager.init_app(app)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for("index"))


# show all categories
@app.route("/")
@app.route("/category/")
def index():
    return render_template("categories.html")

# create new category
@app.route("/category/new", methods=['GET', 'POST'])
@login_required
    return "TODO"


# edit a category
@app.route("/category/<int:category_id>/edit", methods=['GET', 'POST'])
@login_required
    return "TODO"


# edit a category
@app.route("/category/<int:category_id>/delete", methods=['GET', 'POST'])
@login_required
    return "TODO"


# show items in a category


# create new item in category


#


# hook up extensions to app
db.init_app(app)
login_manager.init_app(app)

if __name__ == '__main__':
    if "--setup" in sys.argv:
        with app.app_context():
            db.create_all()
            db.session.commit()
            print("Database tables created")

            user = User(
                name="user1",
                email="user1@ploodle.com",
            )

            category = Category(
                category_name="Adventure games",
                user=user,
            )

            item = Item(
                item_name="Assasin's Creed",
                item_desc="Assassin's Creed is an adventure stealth video game.",
                category=category,
                user=user,
            )

            db.session.add_all([user, category, item])
            db.session.commit()
    else:
        app.debug = True
        app.run(host='0.0.0.0', port=5000)