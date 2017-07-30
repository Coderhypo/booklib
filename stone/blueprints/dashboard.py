from sanic.blueprints import Blueprint

dashboard_blueprint = Blueprint("dashboard", url_prefix="/dashboard")


@dashboard_blueprint.route("/")
def dashboard():
    pass


@dashboard_blueprint.route("/book/history")
def book_history():
    pass


