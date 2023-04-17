from flask import Blueprint, redirect, url_for
from flask_admin import AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from blog import models
from blog.extensions import db, admin

admin_app = Blueprint("admin_app", __name__, url_prefix='/admin')




# admin_app.add_view(ModelView, models.Tag, db.session, category='Models')

class CustomAdminView(ModelView):

    # def create_blueprint(self, admin):
    #     blueprint = super().create_blueprint(admin)
    #     blueprint.name = f'{blueprint.name}_admin'
    #     return blueprint

    # def get_url(self, endpoint, **kwargs):
    #     if not (endpoint.startswith('.') or endpoint.startswith('admin.')):
    #         endpoint = endpoint.replace('.', '_admin.')
    #     return super().get_url(endpoint, **kwargs)

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_staff

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth_app.login'))


class CustomAdminIndexView(AdminIndexView):

    @expose()
    def index(self):
        if not (current_user.is_authenticated and current_user.is_staff):
            return redirect(url_for('auth_app.login'))
        return super().index()


class TagAdminView(CustomAdminView):
    column_searchable_list = ('name',)
    create_modal = True
    edit_modal = True


class ArticleAdminView(CustomAdminView):
    can_export = True
    export_types = ('csv', 'xlsx')
    column_filters = ('author_id',)


class UserAdminView(CustomAdminView):
    column_exclude_list = ('password',)
    column_details_exclude_list = ('password',)
    column_export_exclude_list = ('password',)
    form_columns = ('first_name', 'last_name', 'is_staff')
    can_delete = False
    can_edit = True
    can_create = False
    can_view_details = False
    column_editable_list = ('first_name', 'last_name', 'is_staff')


admin.add_view(ArticleAdminView(models.Article, db.session, category='Models'))
admin.add_view(TagAdminView(models.Tag, db.session, category='Models'))
admin.add_view(UserAdminView(models.User, db.session, category='Models'))
