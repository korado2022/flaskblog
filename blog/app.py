from flask import Flask
# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy

# from blog.article.views import articles_app
# from blog.auth.views import auth_app, login_manager
# from blog.user.views import users_app
from blog import commands
from blog.extensions import db, login_manager, migrate, csrf
from blog.models import User

# db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__)
    # app.config['SECRET_KEY'] = '-u%644akr4bplr*b6397=yj6^4-76#_#=2qpmwlpkh#-0zb1i_'
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config.from_object('blog.config')

    # db.init_app(app)

    # login_manager = LoginManager()
    # login_manager.login_view = 'auth_app.login'
    # login_manager.init_app(app)

    # from .models import User
    register_extensions(app)
    register_blueprints(app)
    register_commands(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)

    login_manager.login_view = 'auth_app.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

def register_blueprints(app: Flask):
    # app.register_blueprint(users_app)
    # app.register_blueprint(articles_app)
    # app.register_blueprint(auth_app)

    from blog.auth.views import auth_app
    from blog.user.views import users_app
    from blog.article.views import articles_app
    from blog.author.views import authors_app

    app.register_blueprint(users_app)
    app.register_blueprint(auth_app)
    app.register_blueprint(articles_app)
    app.register_blueprint(authors_app)
def register_commands(app: Flask):
    app.cli.add_command(commands.init_db)
    app.cli.add_command(commands.create_init_user)
