import string
import random
from passlib.hash import pbkdf2_sha256
from itsdangerous import URLSafeSerializer, BadData
from sqlalchemy import Column, String

from . import BaseModel
from stone.config import get_config_obj

SERIALIZE = URLSafeSerializer(get_config_obj().SECRET_KEY, salt=get_config_obj().COMMON_SALT)


class User(BaseModel):
    """
    注册用户表，注册用户默认不从属图书馆（不是 member）
    """
    __tablename__ = "users"

    username = Column(String(64))
    email = Column(String(128), index=True)
    password = Column(String(128))
    salt = Column(String(64))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.salt = "".join(random.sample(string.ascii_letters + string.digits, 60))
        self.password = self.__get_password(password, self.salt)

    @staticmethod
    def __get_password(password, salt):
        return pbkdf2_sha256.hash("{}+{}".format(password, salt))

    def check_password(self, password):
        return pbkdf2_sha256.verify("{}+{}".format(password, self.salt), self.password)

    def update_password(self, password):
        self.password = self.__get_password(password, self.salt)

    @property
    def token(self):
        data = {
            "user_id": self.id,
            "salt": "".join(random.sample(string.digits + string.ascii_letters, 10)),
        }
        return SERIALIZE.dumps(data)

    @classmethod
    def get_user_by_token(cls, token):
        try:
            payload = SERIALIZE.loads(token)
        except BadData:
            raise
        user_id = payload['user_id']
        user = cls.query.filter_by(id=user_id).first()
        return user

