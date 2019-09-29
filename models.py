from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)
    email = db.Column(db.String(256))


class OAuth(OAuthConsumerMixin, db.Model):
    provider_user_id = db.Column(db.String(256), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship(User)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship(User)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(100), nullable=False)
    item_desc = db.Column(db.String(256))
    cat_id = db.Column(db.Integer, db.ForeignKey("category.id"))
    category = db.relationship(Category)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship(User)


# setup login manager
login_manager = LoginManager()
login_manager.login_view = "github.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
