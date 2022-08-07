import os

from sqlalchemy import Boolean, Column, Date, Integer, String, create_engine
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


class Statistics(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    website = Column(String)
    date = Column(Date)
    success = Column(Boolean)


Base.metadata.create_all(engine)
