import os
import uuid
from datetime import datetime
from sqlalchemy import Table, ForeignKey, or_
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, TEXT, Float, DateTime

from . import BaseModel
from stone.common.clients import DouClient
from stone.config import get_config_obj

config_obj = get_config_obj()
IMAGE_PATH = os.path.join(config_obj.DATA_PATH, "images")

tag_relationship = Table(
    'tag_relationship', BaseModel.metadata,
    Column('tag_id', String(64), ForeignKey('tags.id')),
    Column('book_id', String(64), ForeignKey('books.id')),
    Column('bind_at', DateTime, default=datetime.now),
)


class Book(BaseModel):
    """
    图书表， 通过豆瓣 api 获得图书信息
    图书表只记录图书的信息，不记录关系（图书馆藏书，用户借阅等）
    """
    __tablename__ = "books"

    title = Column(String(256))
    dou_id = Column(String(64))
    rating = Column(Float)
    author = Column(String(256))
    origin_title = Column(String(256))
    translator = Column(String(256))
    douban_link = Column(String(128))
    publisher = Column(String(128))
    isbn10 = Column(String(32), index=True)
    isbn13 = Column(String(32), index=True)
    summary = Column(TEXT)
    tags = relationship(
        "Tag",
        secondary=tag_relationship,
        back_populates="books")

    def __init__(self):
        self.id = str(uuid.uuid4())

    @classmethod
    async def create_by_isbn(cls, isbn):
        book = cls.query.filter(or_(
            cls.isbn13 == isbn,
            cls.isbn10 == isbn,
        )).first()
        if book:
            return book
        book = cls()
        client = DouClient()
        info = client.get_book_info_by_isnb(isnb=isbn)
        await book.__put_info_from_dou(info)
        return book

    @classmethod
    async def create_by_dou_id(cls, dou_id):
        book = cls.query.filter_by(dou_id=dou_id).first()
        if book:
            return book
        book = cls()
        client = DouClient()
        info = client.get_book_info_by_dou_id(dou_id)
        await book.__put_info_from_dou(info)
        return book

    async def __put_info_from_dou(self, info):
        self.title = info['title']
        self.dou_id = info['dou_id']
        self.rating = info['rating']
        self.author = info['author']
        self.origin_title = info['origin_title']
        self.translator = info['translator']
        self.douban_link = info['douban_link']
        self.publisher = info['publisher']
        self.isbn10 = info['isbn10']
        self.isbn13 = info['isbn13']
        self.summary = info['summary']

        await self.bind_tag(info['tags'])
        await self.save_images(info['images'])

    async def update_book_info(self):
        client = DouClient()
        info = client.get_book_info_by_dou_id(self.dou_id)
        await self.__put_info_from_dou(info)

    async def save_images(self, images):
        client = DouClient()
        small = images.get("small")
        sm = client.get_file(small)
        with open(self.get_image_path("small"), "wb") as file:
            file.write(sm)

        large = images.get("large")
        lm = client.get_file(large)
        with open(self.get_image_path("large"), "wb") as file:
            file.write(lm)

        medium = images.get("medium")
        mm = client.get_file(medium)
        with open(self.get_image_path("medium"), "wb") as file:
            file.write(mm)

    def get_image_path(self, image_type="small"):
        path = os.path.join(
            IMAGE_PATH,
            "{}-{}.jpg".format(self.id, image_type),
        )
        return path

    async def bind_tag(self, tags):
        tag_list = []
        for t in tags:
            title = t.get("title")
            name = t.get("name")
            tag = Tag.get_tag_by_title(title)
            if not tag:
                tag = Tag(name, title)
            tag_list.append(tag)
        self.tags = tag_list


class Tag(BaseModel):
    """
    图书标签表
    """
    __tablename__ = "tags"

    name = Column(String(128))
    title = Column(String(128), index=True, unique=True)
    books = relationship(
        "Book",
        secondary=tag_relationship,
        back_populates="tags")

    def __init__(self, name, title):
        self.name = name
        self.title = title

    @classmethod
    def get_tag_by_title(cls, title):
        tag = cls.query.filter_by(title=title).first()
        return tag
