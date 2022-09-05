import os

from sqlalchemy import (Boolean, Column, DateTime, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

DB_ENGINE = os.getenv('DB_ENGINE')
DB_NAME = os.getenv('DB_NAME')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


# testing_engine = create_engine('sqlite:///test.db', future=True)
engine = create_engine(
    '{}://{}:{}@{}:{}/{}'.format(
        DB_ENGINE, POSTGRES_USER,
        POSTGRES_PASSWORD, DB_HOST,
        DB_PORT, DB_NAME
    )
)


Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    tg_id = Column(Integer, unique=True)


class Statistics(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user.id'))
    website = Column(String)
    date = Column(DateTime)
    success = Column(Boolean)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    instance = model(**kwargs)
    session.add(instance)
    session.commit()
    return instance


Base.metadata.create_all(engine)
