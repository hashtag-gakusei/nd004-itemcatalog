#!/usr/bin/env python2
import sys

from flask import Flask, redirect, url_for, \
    flash, render_template, jsonify, request
from flask_login import current_user, login_required, logout_user
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


# JSON SIDE
@app.route('/catalog.json')
def catalogJson():
    items = db.session.query(Item).order_by(Item.id.desc())
    return jsonify(catalog=[i.serialize for i in items])


@app.route('/category/<int:category_id>/item/JSON')
def categoryItemJSON(category_id):
    category = db.session.query(Category).filter_by(id=category_id).one()
    items = db.session.query(Item).filter_by(
        category_id=category_id).all()
    return jsonify(Items=[i.serialize for i in items])


@app.route('/category/<int:category_id>/item/<int:item_id>/JSON')
def itemJSON(category_id, item_id):
    Catalog_Item = db.session.query(Item).filter_by(id=item_id).one()
    return jsonify(Item=Catalog_Item.serialize)


@app.route('/category/JSON')
def categoriesJSON():
    categories = db.session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])

# HTML SIDE

# show all categories
@app.route("/")
@app.route("/category/")
def index():
    categories = db.session.query(Category).all()
    items = db.session.query(Item).all()
    return render_template(
        "categories.html",
        categories=categories,
        items=items
    )


# show items in a category
@app.route("/category/<int:category_id>/")
@app.route("/category/<int:category_id>/item")
@app.route("/category/<int:category_id>/item/")
def showItem(category_id):
    categories = db.session.query(Category).all()
    current_category = db.session.query(Category)\
        .filter_by(id=category_id).one()
    items = db.session.query(Item).filter_by(category_id=category_id).all()
    return render_template(
        "categories.html",
        categories=categories,
        items=items,
        category=current_category
    )

# show item description
@app.route("/category/<int:category_id>/item/<int:item_id>")
@app.route("/category/<int:category_id>/item/<int:item_id>/")
def showItemDescription(category_id, item_id):
    categories = db.session.query(Category).all()
    item = db.session.query(Item).filter_by(id=item_id).one()
    current_category = db.session.query(Category)\
        .filter_by(id=category_id).one()
    return render_template(
        "itemdescription.html",
        item=item,
        categories=categories,
        category=current_category
    )

# create new item in category
@app.route("/category/item/new", methods=['GET', 'POST'])
@login_required
def newItem():
    if request.method == 'POST':
        category = db.session.query(Category)\
                    .filter_by(id=request.form['category']).one()
        new_item = Item(
            item_name=request.form['item_name'],
            item_desc=request.form['item_desc'],
            category=category,
            user=current_user,
        )

        db.session.add(new_item)
        db.session.commit()
        flash('New item successfully created!')
        return redirect(url_for('index'))

    else:
        categories = db.session.query(Category).all()
        return render_template(
            "additem.html",
            categories=categories
        )


# edit catalog item
@app.route(
    "/category/<int:category_id>/item/<int:item_id>/edit",
    methods=['GET', 'POST']
)
@login_required
def editItem(category_id, item_id):
    categories = db.session.query(Category).all()
    item = db.session.query(Item).filter_by(id=item_id).one()
    if request.method == 'POST':
        if request.form['item_name']:
            item.item_name = request.form['item_name']
        if request.form['item_desc']:
            item.item_desc = request.form['item_desc']
        if request.form['category']:
            item.category_id = request.form['category']
        db.session.add(item)
        db.session.commit()
        flash('Item updated!')
        return redirect(
            url_for(
                'editItem',
                category_id=item.category_id,
                item_id=item.id
            )
        )
    else:
        return render_template(
            "edititem.html",
            categories=categories,
            item=item
        )


# delete catalog item
@app.route(
    "/category/<int:category_id>/item/<int:item_id>/delete",
    methods=['GET', 'POST']
)
@login_required
def deleteItem(category_id, item_id):
    category = db.session.query(Category).filter_by(id=category_id).one()
    categories = db.session.query(Category).all()
    item = db.session.query(Item).filter_by(id=item_id).one()
    if request.method == "POST" and current_user.id == item.user_id:
        db.session.delete(item)
        db.session.commit()
        flash("Item deleted")
        return redirect(url_for('index'))
    else:
        return render_template(
            "deleteitem.html",
            item=item,
            category=category,
            categories=categories
        )


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
                item_desc="AC is an adventure stealth video game.",
                category=category,
                user=user,
            )

            item2 = Item(
                item_name="Legend of Zelda",
                item_desc="I actually haven't played this game yet...",
                category=category,
                user=user,
            )

            db.session.add_all([user, category, item, item2])
            db.session.commit()

            user = User(
                name="user2",
                email="user2@ploodle.com",
            )

            category = Category(
                category_name="Action games",
                user=user,
            )

            item = Item(
                item_name="God of War",
                item_desc="Kratos rules!!!!",
                category=category,
                user=user,
            )

            item2 = Item(
                item_name="Matrix",
                item_desc="Will you take the blue pill?",
                category=category,
                user=user,
            )

            db.session.add_all([user, category, item, item2])
            db.session.commit()
    else:
        app.debug = True
        app.run(host='0.0.0.0', port=5000)
