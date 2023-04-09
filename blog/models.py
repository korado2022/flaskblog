from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from blog.app import db


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(120), unique=False, nullable=False, default="", server_default="")
    last_name = db.Column(db.String(120), unique=False, nullable=False, default="", server_default="")
    email = db.Column(db.String(255), unique=True, nullable=False, default="")
    password = db.Column(db.String(255))
    is_staff = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, first_name, last_name, username, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

    # def __repr__(self):
    #     return f"<User #{self.id} {self.username!r}>"

# class Article(db.Model):
#     __tablename__ = 'articles'
#
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255))
#     text = db.Column(db.String)
#     author = relationship('User')