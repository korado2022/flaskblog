from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

articles_app = Blueprint("articles_app", __name__, url_prefix='/articles', static_folder='../static')

ARTICLES = {
    1: {
        'title': 'title_1',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
                'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
                'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
                'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
                'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
                'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
                'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
                'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
                'metus consequat. In congue sodales condimentum.',
        'author': {
            'name': 'Aleks',
            'id': 1,
        },
    },
    2: {
        'title': 'title_2',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
                'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
                'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
                'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
                'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
                'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
                'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
                'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
                'metus consequat. In congue sodales condimentum.',
        'author': {
            'name': 'Jon',
            'id': 2,
        },
    },
    3: {
        'title': 'title_3',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
                'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
                'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
                'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
                'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
                'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
                'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
                'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
                'metus consequat. In congue sodales condimentum.',
        'author': {
            'name': 'Ivan',
            'id': 3,
        },
    },
    4: {
        'title': 'title_4',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
                'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
                'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
                'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
                'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
                'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
                'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
                'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
                'metus consequat. In congue sodales condimentum.',
        'author': {
            'name': 'Aleks',
            'id': 1,
        },
    },
    5: {
        'title': 'title_5',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
                'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
                'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
                'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
                'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
                'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
                'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
                'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
                'metus consequat. In congue sodales condimentum.',
        'author': {
            'name': 'Jon',
            'id': 2,
        },
    },
    6: {
        'title': 'title_6',
        'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus laoreet dapibus ipsum, '
                'fringilla pharetra ante condimentum sed. Mauris quis mi eu est rhoncus ornare vitae vel lacus. '
                'Praesent id scelerisque neque. Quisque sed augue vitae urna finibus volutpat eget nec nisl. '
                'Proin nisi mauris, faucibus eget eros convallis, congue tempus mi. Integer facilisis feugiat lacus, '
                'sit amet porta sapien tempus ac. Fusce tincidunt rhoncus ipsum, at tempor urna viverra varius. '
                'Duis a erat dictum, molestie erat eget, pellentesque nisl. Mauris fringilla in urna ac luctus. '
                'Interdum et malesuada fames ac ante ipsum primis in faucibus. Praesent mi purus, tincidunt '
                'non condimentum eu, aliquam nec augue. Suspendisse finibus purus quis leo tincidunt, eget tincidunt '
                'metus consequat. In congue sodales condimentum.',
        'author': {
            'name': 'Ivan',
            'id': 3,
        },
    }
}


@articles_app.route("/")
def articles_list():
    return render_template("articles/list.html", articles=ARTICLES)

@articles_app.route('/<int:pk>')
def get_article(pk: int):
    try:
        article = ARTICLES[pk]
    except KeyError:
        raise NotFound(f'Article id {pk} not found')
    return render_template('articles/details.html', article=article)
