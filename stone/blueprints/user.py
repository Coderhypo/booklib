from sanic.blueprints import Blueprint


user_blueprint = Blueprint("user", url_prefix="/user")
