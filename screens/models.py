from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('sqlite:///test.db', future=True)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class Statistics(Base):
    __tablename__ = 'statistics'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    website = Column(String)


Base.metadata.create_all(engine)
