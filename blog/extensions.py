from combojsonapi.spec import ApiSpecPlugin
from flask_admin import Admin
from flask_combo_jsonapi import Api
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from blog.admin.views import CustomAdminIndexView

# def create_api_spec_plugin(app):
#     api_spec_plugin = ApiSpecPlugin(
#         app=app,
#         # Declaring tags list with their descriptions,
#         # so API gets organized into groups. it's optional.
#         tags={
#             'Tag': 'Tag API',
#             'User': 'User API',
#             'Author': 'Author API',
#             'Article': 'Article API',
#         }
#     )
#     return api_spec_plugin


login_manager = LoginManager()
db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect()
admin = Admin(
    index_view=CustomAdminIndexView(),
    name='Blog Admin',
    template_mode='bootstrap4')

api = Api()
