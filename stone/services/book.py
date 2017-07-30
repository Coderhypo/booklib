from stone.models.book import Book
from stone.models import db_session


async def create_book_by_isbn(isbn):
    book = await Book.create_by_isbn(isbn)
    db_session.add(book)
    db_session.commit()
    return book


async def create_book_by_dou_id(dou_id):
    book = await Book.create_by_dou_id(dou_id)
    db_session.add(book)
    db_session.commit()
    return book


async def update_book_info(book: Book):
    await book.update_book_info()
    db_session.add(book)
    db_session.commit()
    return book

