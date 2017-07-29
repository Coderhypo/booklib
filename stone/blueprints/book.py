from sanic.blueprints import Blueprint


book_blueprint = Blueprint("book", url_prefix="/book")
