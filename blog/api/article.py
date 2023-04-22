from combojsonapi.event.resource import EventsResource
from flask_combo_jsonapi import ResourceDetail, ResourceList
from blog.schemas import ArticleSchema
from blog.extensions import db
from blog.models import Article


class ArticleCountEvent(EventsResource):
    def event_get_count(self):
        return {'count': Article.query.count()}

class AuthorDetailEvent(EventsResource):
    def event_get_articles_count(self, **kwargs):
        return {'count': Article.query.filter(Article.author_id == kwargs['id']).count()}

class ArticleList(ResourceList):
    events = ArticleCountEvent
    schema = ArticleSchema
    data_layer = {
        'session': db.session,
        'model': Article,
    }
class ArticleDetail(ResourceDetail):
    events = AuthorDetailEvent
    schema = ArticleSchema
    data_layer = {
        'session': db.session,
        'model': Article,
    }

