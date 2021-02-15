# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
{%- if cookiecutter.db_driver == "gino(async)" %}
import asyncio
{% endif %}
{%- if cookiecutter.db_driver == "sqlachemy(sync)" %}
from {{cookiecutter.project_slug}}.models.sessions import session
{% endif %}
from {{cookiecutter.project_slug}}.models.models import AuthorModel, QuoteModel, db, setup_db


{%- if cookiecutter.db_driver == "sqlachemy(sync)" %}
class DBPipeline:
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
{% endif %}
{%- if cookiecutter.db_driver == "gino(async)" %}


async def main():
    await setup_db()
    await db.set_bind("postgresql://docker:docker@postgres/{{cookiecutter.project_slug}}")


class DBPipeline:
    def open_spider(self, spider):
        asyncio.get_event_loop().run_until_complete(main())

    async def process_item(self, item, spider):
        author = await AuthorModel.query.where(
            AuthorModel.name == item.get("author", "")
        ).gino.first()
        if not author:
            author = await AuthorModel.create(name=item.get("author", ""))
        else:
            author = await author.update(name=item.get("author", "")).apply()
        await QuoteModel.create(author_id=author.id, content=item.get("content"))
        return item

    async def close_spider(self, spider):
        await db.pop_bind().close()
{% endif %}