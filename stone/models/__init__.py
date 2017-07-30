import uuid
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, DateTime, Boolean, String

from stone.config import get_config_obj

config_obj = get_config_obj()

engine = create_engine(config_obj.DATABASE_PATH, convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


class Base(object):
    id = Column(String, default=lambda: str(uuid.uuid4()), primary_key=True)
    create_at = Column(DateTime, default=datetime.now)
    update_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)


BaseModel = declarative_base(bind=engine, cls=Base)
BaseModel.query = db_session.query_property()


def init_db(drop=False):
    from .user import User
    from .book import tag_relationship, Book, Tag
    if drop:
        BaseModel.metadata.drop_all()
    BaseModel.metadata.create_all()
