# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from {{cookiecutter.project_slug}}.models.models import AuthorModel, QuoteModel
from {{cookiecutter.project_slug}}.models.sessions import session


class SQLAlchemyPipeline(object):
    """Pipeline to save uniq authors (consider name is unique key), save all quotes (dupls allowed)"""

    def close_spider(self, spider):
        session.close()

    def process_item(self, item, spider):
        author = (
            session.query(AuthorModel).filter_by(name=item.get("author")).one_or_none()
        )
        if not author:
            author = AuthorModel()
            author.name = item.get("author")
            session.add(author)
        quote = QuoteModel()
        quote.author = author
        quote.content = item.get("content")
        session.add(quote)
        session.commit()
        return item
