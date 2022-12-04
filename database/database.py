from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def make_engine(path):
    engine = create_engine(f'sqlite:///{path}')
    return engine


def create_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


Base = declarative_base()
