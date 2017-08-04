from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, TEXT, ForeignKey, DateTime

from . import BaseModel


class Library(BaseModel):
    """
    图书馆表
    """
    __tablename__ = "libraries"
    name = Column(String(128), nullable=False, index=True)
    member = relationship("Member")
    collection_book = relationship("CollectionBook")
    recommended_book = relationship("RecommendedBook")
    purchase_book = relationship("PurchaseBook")
    borrow_record = relationship("BorrowRecord")
    create_user = Column(String(128))

    def __init__(self, name):
        self.name = name


class Member(BaseModel):
    """
    图书馆成员表
    """
    __tablename__ = "members"
    library_id = Column(String(128), ForeignKey("libraries.id"))
    user_id = Column(String(128), index=True)

    def __init__(self, library_id, user_id):
        self.user_id = user_id
        self.library_id = library_id


class CollectionBook(BaseModel):
    """
    图书馆藏书表
    """
    __tablename__ = "collection_books"
    library_id = Column(String(128), ForeignKey("libraries.id"))
    book_id = Column(String(128), index=True)
    add_user = Column(String(128))

    def __init__(self, library_id, book_id):
        self.library_id = library_id
        self.book_id = book_id


class RecommendedBook(BaseModel):
    """
    用户推荐图书表
    """
    __tablename__ = "recommended_books"
    library_id = Column(String(128), ForeignKey("libraries.id"))
    user_id = Column(String(128), index=True)
    member_id = Column(String(128))
    book_id = Column(String(128))
    comment = Column(TEXT)

    def __init__(self, library_id, user_id, book_id):
        self.library_id = library_id
        self.user_id = user_id
        self.book_id = book_id


class PurchaseBook(BaseModel):
    """
    待采购图书表
    """
    __tablename__ = "purchase_books"
    library_id = Column(String(128), ForeignKey("libraries.id"))
    user_id = Column(String(128), index=True)
    member_id = Column(String(128))
    book_id = Column(String(128), index=True)

    def __init__(self, library_id, user_id, book_id):
        self.library_id = library_id
        self.user_id = user_id
        self.book_id = book_id


class BorrowRecord(BaseModel):
    """
    图书借阅记录表
    """
    __tablename__ = "borrow_records"
    library_id = Column(String(128), ForeignKey("libraries.id"))
    user_id = Column(String(128), index=True)
    member_id = Column(String(128))
    collection_book_id = Column(String(128), index=True)
    borrow_at = Column(DateTime, default=datetime.now())
    return_at = Column(DateTime, default=None)

    def __init__(self, library_id, user_id, collection_book_id):
        self.library_id = library_id
        self.user_id = user_id
        self.collection_book_id = collection_book_id

