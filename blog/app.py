from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from blog.article.views import articles_app
from blog.auth.views import auth_app, login_manager
from blog.user.views import users_app

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = '-u%644akr4bplr*b6397=yj6^4-76#_#=2qpmwlpkh#-0zb1i_'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth_app.login'
    login_manager.init_app(app)

    # from .models import User

    register_blueprints(app)
    return app

def register_blueprints(app: Flask):
    app.register_blueprint(users_app)
    app.register_blueprint(articles_app)
    app.register_blueprint(auth_app)

