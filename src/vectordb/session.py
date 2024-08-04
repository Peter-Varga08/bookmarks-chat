from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from vectordb.config import DB_CONNECTION


def create_session():
    engine = create_engine(DB_CONNECTION)
    Session = sessionmaker(bind=engine)
    return Session()
