from flask_combo_jsonapi import ResourceDetail, ResourceList

from blog.api.permissions.user import UserListPermission, UserPatchPermission
from blog.schemas import UserSchema
from blog.extensions import db
from blog.models import User


class UserList(ResourceList):
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User,
        'permission_get': [UserListPermission],
    }
class UserDetail(ResourceDetail):
    schema = UserSchema
    data_layer = {
        'session': db.session,
        'model': User,
        'short_format': [
            'id',
            'first_name',
            'last_name',
            'username',
            'is_staff',
            'email',
        ],
        'permission_patch': [UserPatchPermission],
    }