import click
from werkzeug.security import generate_password_hash

from blog.extensions import db


@click.command('init-db')
def init_db():
    from wsgi import app

    # import models for creating tables
    from blog.models import User

    db.create_all(app=app)
    print("done!")

@click.command('create-init-user')
def create_init_user():
    from blog.models import User
    from wsgi import app

    with app.app_context():
        admin = User(username="admin", email='admin@m.ru', password=generate_password_hash('test123'), is_staff=True)
        james = User(username="james", email='james@m.ru', password=generate_password_hash('test456'))
        db.session.add(admin)
        db.session.add(james)
        db.session.commit()
        print("done! created users:", admin, james)

