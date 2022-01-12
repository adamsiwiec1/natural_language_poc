from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()


def init_db(app):
    db.init_app(app)
    db.create_all(app=app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))