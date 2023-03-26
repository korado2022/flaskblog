from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

users_app = Blueprint('users_app', __name__, url_prefix='/users', static_folder='../static')

# USERS = ['Aleks', 'Jon', 'Ivan']
USERS = {
    1: 'Aleks',
    2: 'Jon',
    3: 'Ivan'
}


@users_app.route('/')
def users_list():
    return render_template('users/list.html', users=USERS)

@users_app.route('/<int:pk>')
def get_user(pk: int):
    try:
        user_name = USERS[pk]
    except KeyError:
        raise NotFound(f'User id {pk} not found')
    return render_template('users/details.html', user_name=user_name)

