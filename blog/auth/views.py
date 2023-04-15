from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.exceptions import NotFound
from werkzeug.security import check_password_hash, generate_password_hash

from blog.forms.user import LoginForm

# from blog.models import User


auth_app = Blueprint('auth_app', __name__, static_folder='../static')

login_manager = LoginManager()
login_manager.login_view = "auth_app.login"

@login_manager.user_loader
def load_user(user_id):
    from blog.models import User
    return User.query.filter_by(id=user_id).one_or_none()


@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for("auth_app.login"))


@auth_app.route('/login', methods=['POST', 'GET'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('users_app.profile', pk=current_user.id))

    errors = []
    form = LoginForm(request.form)
    if request.method == 'GET':
        flash('Need a method POST')
        return render_template('auth/login.html', form=form, errors=errors)

    if request.method == 'POST':
        email = form.email.data
        password = generate_password_hash(form.password.data)
        if not email:
            form.email.errors = ["email not passed"]
            return render_template('auth/login.html', form=form, errors=errors)

        from blog.models import User
        _user = User.query.filter_by(email=form.email.data).one_or_none()

        if not _user or check_password_hash(_user.password, password):
        # if not _user:
            form.password.errors = ['Check your login details']
            return redirect(url_for('.login', form=form, errors=errors))

        login_user(_user)
        return redirect(url_for('users_app.profile', pk=_user.id))


@auth_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))



# __all__ = [
# "login_manager",
# "auth_app",
# ]