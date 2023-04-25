from combojsonapi.event import EventPlugin
from combojsonapi.permission import PermissionPlugin
from flask import Flask
from flask_combo_jsonapi import Api
from combojsonapi.spec import ApiSpecPlugin

# from flask_login import LoginManager
# from flask_sqlalchemy import SQLAlchemy

# from blog.article.views import articles_app
# from blog.auth.views import auth_app, login_manager
# from blog.user.views import users_app
from blog import commands

from blog.extensions import db, login_manager, migrate, csrf, admin, create_api_spec_plugin, api
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
    register_api(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)
    csrf.init_app(app)
    admin.init_app(app)

    api.plugins = [
        EventPlugin(),
        PermissionPlugin(),
        ApiSpecPlugin(
            app=app,
            tags={
                'Tag': 'Tag API',
                'User': 'User API',
                'Author': 'Author API',
                'Article': 'Article API',
            }
        ),
    ]
    api.init_app(app)

    login_manager.login_view = 'auth_app.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

def register_api(app: Flask):
    from blog.api.tag import TagList, TagDetail
    from blog.api.author import AuthorList, AuthorDetail
    from blog.api.user import UserList, UserDetail
    from blog.api.article import ArticleList, ArticleDetail


    api.route(TagList, 'tag_list', '/api/tags/', tag='Tag')
    api.route(TagDetail, 'tag_detail', '/api/tags/<int:id>/', tag='Tag')

    api.route(UserList, 'user_list', '/api/users/', tag='User')
    api.route(UserDetail, 'user_detail', '/api/users/<int:id>/', tag='User')

    api.route(AuthorList, 'author_list', '/api/authors/', tag='Author')
    api.route(AuthorDetail, 'author_detail', '/api/authors/<int:id>/', tag='Author')

    api.route(ArticleList, 'article_list', '/api/articles/', tag='Aticle')
    api.route(ArticleDetail, 'article_detail', '/api/articles/<int:id>/', tag='Aticle')

def register_blueprints(app: Flask):
    # app.register_blueprint(users_app)
    # app.register_blueprint(articles_app)
    # app.register_blueprint(auth_app)

    from blog.auth.views import auth_app
    from blog.user.views import users_app
    from blog.article.views import articles_app
    from blog.author.views import authors_app
    from blog.admin.views import admin_app
    # from blog import admin

    app.register_blueprint(users_app)
    app.register_blueprint(auth_app)
    app.register_blueprint(articles_app)
    app.register_blueprint(authors_app)
    app.register_blueprint(admin_app)

    # admin.register_views()

def register_commands(app: Flask):
    app.cli.add_command(commands.init_db)
    app.cli.add_command(commands.create_init_user)
    app.cli.add_command(commands.create_init_tags)
