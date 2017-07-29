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
    is_deleted = Column(Boolean, default=False, index=True)

    @property
    def query(self):
        return db_session.query_property().filter_by(is_deleted=False)

    def delete(self):
        self.is_deleted = True


BaseModel = declarative_base(bind=engine, cls=Base)


async def init_db(drop=False):
    if drop:
        Base.metadata.drop_all()
    Base.metadata.create_all()
