import datetime

{%- if cookiecutter.db_driver == "sqlachemy(sync)" %}
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
Base = declarative_base()
{%- endif %}
{%- if cookiecutter.db_driver == "gino(async)" %}

from fastapi import FastAPI
from gino.ext.starlette import Gino
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text

from {{cookiecutter.project_slug}}.settings import DB

app = FastAPI()


db = Gino(
    app,
    # drivername=DB["dialect"],
    host=DB["host"],
    port=DB["port"],
    user=DB["username"],
    password=DB["password"],
    database=DB["db_name"],
    echo=True,
)
Base = db.Model


async def setup_db():
    await db.set_bind("postgresql://docker:docker@postgres/{{cookiecutter.project_slug}}")
    await db.gino.create_all()
    await db.pop_bind().close()
{%- endif %}


class TimeStampedModelMixin:
    """
     An Mixin base class model that provides self-updating
    ``created_at`` and ``modified_at`` fields.
    """

    created_at = Column(DateTime, default=datetime.datetime.now)
    modified_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )


class AuthorModel(TimeStampedModelMixin, Base):
    __tablename__ = "author"

    id = Column(Integer, primary_key=True)
    name = Column(Text(), unique=True)


class QuoteModel(TimeStampedModelMixin, Base):
    __tablename__ = "quote"

    id = Column(Integer, primary_key=True)
    content = Column(Text())
    author_id = Column(Integer, ForeignKey("author.id"))
    {%- if cookiecutter.db_driver == "sqlachemy(sync)" %}
    author = relationship("AuthorModel")
    {%- endif %}
