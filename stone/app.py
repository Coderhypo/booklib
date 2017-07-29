from sanic import Sanic

from stone.ext import jinja, session_interface
from stone.blueprints import book_blueprint, dashboard_blueprint, index_blueprint, user_blueprint


def create_app():
    app = Sanic("Stone")
    app.static("/static", "stone/static")

    # register blueprint
    app.blueprint(book_blueprint)
    app.blueprint(dashboard_blueprint)
    app.blueprint(index_blueprint)
    app.blueprint(user_blueprint)

    # init ext model
    jinja.init_app(app, pkg_name=__name__)

    # init middleware
    init_middleware(app)
    return app


def init_middleware(app):
    @app.middleware('request')
    async def add_session_to_request(request):
        await session_interface.open(request)

    @app.middleware('response')
    async def save_session(request, response):
        await session_interface.save(request, response)

