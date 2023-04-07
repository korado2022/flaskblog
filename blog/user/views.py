from flask import Blueprint, render_template, redirect, url_for, request, current_app
from flask_login import login_required, current_user, login_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import NotFound
from werkzeug.security import generate_password_hash

from blog.extensions import db
from blog.forms.user import UserRegisterForm
from blog.models import User

users_app = Blueprint('users_app', __name__, url_prefix='/users', static_folder='../static')

# USERS = ['Aleks', 'Jon', 'Ivan']
# USERS = {
#     1: 'Aleks',
#     2: 'Jon',
#     3: 'Ivan'
# }


@users_app.route('register', methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users_app.profile', pk=current_user.id))

    errors = None
    form = UserRegisterForm(request.form)
    if request.method == "POST" and form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).count():
            form.email.errors.append("email not uniq")
            return render_template("users/register.html", form=form)

    _user = User(
        first_name=form.first_name.data,
        last_name=form.last_name.data,
        username=form.username.data,
        email=form.email.data,
        password=generate_password_hash(form.password.data),
    )

    db.session.add(_user)
    try:
        db.session.commit()
    except IntegrityError:
        current_app.logger.exception("Could not create user!")
        error = "Could not create user!"
    else:
        current_app.logger.info("Created user %s", _user)
        login_user(_user)
        return redirect(url_for("users_app.profile", pk=current_user.id))

    return render_template('users/register.html', form=form, errors=errors)

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

