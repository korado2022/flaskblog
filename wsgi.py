from blog.app import create_app, db
# from werkzeug.security import generate_password_hash

# from blog.models import User

app = create_app()

#
# @app.cli.command('init-db')
# def init_db():
#     db.create_all()
#     print("done!")
#
#
# @app.cli.command("create-users")
# def create_users():
#     """
#         Run in your terminal:
#         flask create-users
#         > done! created users: <User #1 'admin'> <User #2 'james'>
#     """
#
#     # from blog.models import User
#     admin = User(username="admin", email='admin@m.ru', password=generate_password_hash('test123'), is_staff=True)
#     james = User(username="james", email='james@m.ru', password=generate_password_hash('test456'))
#     db.session.add(admin)
#     db.session.add(james)
#     db.session.commit()
#     print("done! created users:", admin, james)
#


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5001,
        debug=True,
    )