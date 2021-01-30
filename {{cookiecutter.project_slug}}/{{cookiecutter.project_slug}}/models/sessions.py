import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from {{cookiecutter.project_slug}}.models.models import Base
from {{cookiecutter.project_slug}}.settings import DB


def get_session():
    engine_url = sqlalchemy.engine.url.URL(
        drivername=DB["dialect"],
        host=DB["host"],
        port=DB["port"],
        username=DB["username"],
        password=DB["password"],
        database=DB["db_name"],
        # query={'charset': 'utf8mb4'}
    )

    db_engine = create_engine(
        engine_url, encoding="utf-8", echo=False, pool_recycle=3600
    )

    Session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = scoped_session(Session)
    return db_engine, session


db_engine, session = get_session()
Base.metadata.create_all(db_engine)
