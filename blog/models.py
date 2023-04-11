from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,Table
from sqlalchemy.orm import relationship

from blog.app import db

article_tag_association_table = Table(
    'article_tag_association',
    db.metadata,
    db.Column('article_id', db.Integer, ForeignKey('articles.id'), nullable=False),
    db.Column('tag_id', db.Integer, ForeignKey('tags.id'), nullable=False),
)

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    first_name = db.Column(db.String(120), unique=False, nullable=False, default='', server_default='')
    last_name = db.Column(db.String(120), unique=False, nullable=False, default='', server_default='')
    email = db.Column(db.String(255), unique=True, nullable=False, default='')
    password = db.Column(db.String(255))
    is_staff = db.Column(db.Boolean, nullable=False, default=False)

    author = relationship('Author', uselist=False, back_populates='user')
    def __init__(self, email, first_name, last_name, username, password):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password

    # def __repr__(self):
    #     return f"<User #{self.id} {self.username!r}>"

class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='author')
    article = relationship('Article', back_populates='author')

class Article(db.Model):
    __tablename__ = 'articles'

    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, ForeignKey('authors.id'), nullable=False)
    title = db.Column(db.String(255))
    text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    author = relationship('Author', back_populates='article')
    tags = relationship('Tag', secondary=article_tag_association_table, back_populates='articles')

class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, default='', server_default='')

    articles = relationship('Article', secondary=article_tag_association_table, back_populates='tags')



# class Article(db.Model):
#     __tablename__ = 'articles'
#
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(255))
#     text = db.Column(db.String)
#     author = relationship('User')