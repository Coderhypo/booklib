from sqlalchemy import Column, String, ForeignKey, TEXT

from . import BaseModel


class Library(BaseModel):
    """
    图书馆表， 允许多个图书馆
    """
    __tablename__ = "libraries"
    name = Column(String(128), nullable=False, index=True)


class Member(BaseModel):
    """
    图书馆成员表
    """
    __tablename__ = "members"
    library_id = Column(String(128), ForeignKey("library.id"), index=True)
    user_id = Column(String(128), ForeignKey("user.id"), index=True)


class CollectionBook(BaseModel):
    """
    图书馆藏书表
    """
    __tablename__ = "collection_books"
    library_id = Column(String(128), ForeignKey("library.id"), index=True)
    book_id = Column(String(128), ForeignKey("book.id"))


class RecommendedBook(BaseModel):
    """
    用户推荐图书表
    """
    __tablename__ = "recommended_books"
    library_id = Column(String(128), ForeignKey("library.id"), index=True)
    user_id = Column(String(128), ForeignKey("user.id"), index=True)
    member_id = Column(String(128), ForeignKey("member.id"))
    book_id = Column(String(128), ForeignKey("book.id"))
    comment = Column(TEXT)


class PurchaseBook(BaseModel):
    """
    待采购图书表
    """
    __tablename__ = "purchase_books"
    library_id = Column(String(128), ForeignKey("library.id"), index=True)
    user_id = Column(String(128), ForeignKey("user.id"), index=True)
    member_id = Column(String(128), ForeignKey("member.id"))
    book_id = Column(String(128), ForeignKey("book.id"))


class BorrowRecord(BaseModel):
    """
    图书借阅记录表
    """
    __tablename__ = "borrow_records"
    library_id = Column(String(128), ForeignKey("library.id"), index=True)
    user_id = Column(String(128), ForeignKey("user.id"), index=True)
    member_id = Column(String(128), ForeignKey("member.id"))
    book_id = Column(String(128), ForeignKey("book.id"))

