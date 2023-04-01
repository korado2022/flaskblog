from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.exceptions import NotFound
from werkzeug.security import check_password_hash



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
    if request.method == 'GET':
        return render_template('auth/login.html')

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return render_template('auth/login.html', error='email not passed')

    from blog.models import User
    user = User.query.filter_by(email=email).one_or_none()

    # if not user or check_password_hash(user.password, password):
    if not user:
        flash('Check your login details')
        return redirect(url_for('.login'))
    login_user(user)
    return redirect(url_for('users_app.profile', pk=user.id))


@auth_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('.login'))



# __all__ = [
# "login_manager",
# "auth_app",
# ]