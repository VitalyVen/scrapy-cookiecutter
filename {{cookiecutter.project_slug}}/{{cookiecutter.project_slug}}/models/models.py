import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


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
    author = relationship("AuthorModel")
