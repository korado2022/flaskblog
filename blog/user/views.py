from flask import Blueprint, render_template
from flask_login import login_required
from werkzeug.exceptions import NotFound

from blog.models import User

users_app = Blueprint('users_app', __name__, url_prefix='/users', static_folder='../static')

# USERS = ['Aleks', 'Jon', 'Ivan']
# USERS = {
#     1: 'Aleks',
#     2: 'Jon',
#     3: 'Ivan'
# }


@users_app.route('/')
def users_list():
    # from blog.models import User
    users = User.query.all()
    return render_template('users/list.html', users=users)

@users_app.route('/<int:pk>')
@login_required
def profile(pk: int):
    # try:
    #     user_name = USERS[pk]
    # except KeyError:
    #     raise NotFound(f'User id {pk} not found')
    # from blog.models import User
    user = User.query.filter_by(id=pk).one_or_none()
    if user is None:
        raise NotFound(f"User #{pk} doesn't exist!")

    return render_template('users/details.html', user=user)

