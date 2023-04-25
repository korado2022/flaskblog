from sqlite3 import IntegrityError

import requests as requests
from flask import Blueprint, render_template, request, current_app, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound

from blog.extensions import db
from blog.forms.article import CreateArticleForm
from blog.models import Article, Author, Tag

articles_app = Blueprint("articles_app", __name__, url_prefix='/articles', static_folder='../static')

# ARTICLES = {
#     1: {
#         'title': 'title_1',
#         'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
#                 'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
#                 'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
#                 'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
#                 'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
#                 'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
#                 'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
#                 'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
#                 'metus consequat. In congue sodales condimentum.',
#         'author': {
#             'name': 'Aleks',
#             'id': 1,
#         },
#     },
#     2: {
#         'title': 'title_2',
#         'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
#                 'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
#                 'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
#                 'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
#                 'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
#                 'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
#                 'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
#                 'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
#                 'metus consequat. In congue sodales condimentum.',
#         'author': {
#             'name': 'Jon',
#             'id': 2,
#         },
#     },
#     3: {
#         'title': 'title_3',
#         'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
#                 'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
#                 'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
#                 'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
#                 'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
#                 'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
#                 'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
#                 'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
#                 'metus consequat. In congue sodales condimentum.',
#         'author': {
#             'name': 'Ivan',
#             'id': 3,
#         },
#     },
#     4: {
#         'title': 'title_4',
#         'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
#                 'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
#                 'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
#                 'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
#                 'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
#                 'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
#                 'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
#                 'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
#                 'metus consequat. In congue sodales condimentum.',
#         'author': {
#             'name': 'Aleks',
#             'id': 1,
#         },
#     },
#     5: {
#         'title': 'title_5',
#         'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
#                 'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
#                 'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
#                 'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
#                 'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
#                 'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
#                 'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
#                 'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
#                 'metus consequat. In congue sodales condimentum.',
#         'author': {
#             'name': 'Jon',
#             'id': 2,
#         },
#     },
#     6: {
#         'title': 'title_6',
#         'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
#                 'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
#                 'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
#                 'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
#                 'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
#                 'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
#                 'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
#                 'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
#                 'metus consequat. In congue sodales condimentum.',
#         'author': {
#             'name': 'Ivan',
#             'id': 3,
#         },
#     }
# }
#

@articles_app.route("/", methods=["GET"])
@login_required
def articles_list():
    articles: Article = Article.query.all()
    # call RPC method
    count_articles = requests.get('http://127.0.0.1:5001/api/articles/event_get_count/').json
    return render_template("articles/list.html", articles=articles, count_articles=count_articles['count'])


@articles_app.route("/create", methods=["GET"])
@login_required
def create_article_form():
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    return render_template("articles/create.html", form=form)



@articles_app.route("/create", methods=["POST"])
@login_required
def create_article():
    errors = []
    form = CreateArticleForm(request.form)
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if form.validate_on_submit():
        _article = Article(title=form.title.data.strip(), text=form.text.data)
        # db.session.add(_article)

        if request.method == "POST" and form.validate_on_submit():
            if form.tags.data:
                selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
                for tag in selected_tags:
                    _article.tags.append(tag)


        if not current_user.author:
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.commit()

        _article.author_id = current_user.author.id

        db.session.add(_article)
        db.session.commit()
        return redirect(url_for("articles_app.details", article_id=_article.id))


    return render_template('articles/create.html', form=form)


@articles_app.route('/<int:article_id>')
@login_required
def details(article_id: int):

    _article = Article.query.filter_by(id=article_id).options(joinedload(Article.tags)).one_or_none()


    if _article is None:
        raise NotFound(f"Article #{article_id} doesn't exist!")

    return render_template('articles/details.html', article=_article)

# @articles_app.route('/<int:pk>')
# def get_article(pk: int):
#     try:
#         article = ARTICLES[pk]
#     except KeyError:
#         raise NotFound(f'Article id {pk} not found')
#     return render_template('articles/details.html', article=article)
