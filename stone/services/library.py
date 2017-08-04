from stone.models import db_session
from stone.models.user import User
from stone.models.book import Book
from stone.models.library import Library, Member, CollectionBook, \
    RecommendedBook, PurchaseBook, BorrowRecord
from stone.common.helper import get_current_library
from stone.common.errors import BookNotFound, UserNotFound, RecommendedNotFound


async def create_library(library_name, user_id):
    lib = Library(library_name)
    lib.create_user = user_id
    db_session.add(lib)
    db_session.commit()
    return lib


async def add_member(user_id):
    lib = await get_current_library()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise UserNotFound("Can't get user by id: {}".format(user_id))
    member = Member(lib.id, user_id)
    db_session.add(member)
    db_session.commit()
    return member


async def remove_member(member_id):
    member = Member.query.filter_by(id=member_id).first()
    if not member:
        raise UserNotFound("Can't get member info by id: {}".format(member_id))
    db_session.delete(member)
    db_session.commit()


async def add_collection_book(book_id, user_id):
    lib = await get_current_library()
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        raise BookNotFound("Can't get book info by id: {}".format(book_id))
    cb = CollectionBook(lib.id, book_id)
    cb.add_user = user_id
    pb = PurchaseBook.query.filter_by(book_id=book_id).first()
    if pb:
        db_session.delete(pb)
    db_session.add(cb)
    db_session.commit()
    return cb


async def add_recommended(book_id, user_id, comment):
    lib = await get_current_library()
    cb = CollectionBook.query.filter_by(book_id=book_id).first()
    if not cb:
        raise BookNotFound("The not a collection book")
    rb = RecommendedBook(lib.id, user_id, book_id)
    rb.comment = comment
    db_session.add(rb)
    db_session.commit()
    return rb


async def remove_recommended(recommended_id):
    rb = RecommendedBook.query.filter_by(id=recommended_id).first()
    if not rb:
        raise RecommendedNotFound("Can't get recommended info by id: {}"
                                  .format(recommended_id))
    db_session.delete(rb)
    db_session.commit()


async def add_purchase_book(book_id, user_id):
    lib = await get_current_library()
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        raise BookNotFound("Can't get book info by id: {}".format(book_id))
    cb = CollectionBook.query.filter_by(book_id=book_id).first()
    if cb:
        raise BookNotFound("The collection book is exited")
    pb = PurchaseBook.query.filter_by(book_id=book_id).first()
    if pb:
        return pb
    pb = PurchaseBook(lib.id, user_id, book_id)
    db_session.add(pb)
    db_session.commit()
    return pb


async def borrow_books(user_id, book_id):
    lib = await get_current_library()
    user = User.query.filter_by(id=user_id).first()
    if not user:
        raise UserNotFound("Can't get user by id: {}".format(user_id))
    book = CollectionBook.query.filter_by(book_id=book_id).first()
    if not book:
        raise BookNotFound("Can't get collection book by id: {}".format(book_id))
    br = BorrowRecord(lib.id, user_id, book.id)
    db_session.add(br)
    db_session.commit()
    return br


async def back_book(book_id):
    book = CollectionBook.query.filter_by(book_id=book_id).first()
    if not book:
        raise BookNotFound("Can't get collection book by id: {}".format(book_id))
    br = BorrowRecord.query.filter_by(collection_book_id=book.id).first()
    if not br:
        return
    db_session.delete(br)
    db_session.commit()
