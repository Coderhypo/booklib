from sanic import Sanic

from stone.config import get_config_obj
from stone.ext import jinja, session_interface
from stone.blueprints import book_blueprint, dashboard_blueprint, index_blueprint, user_blueprint


def create_app():
    app = Sanic("Stone")
    app.static("/static", "stone/static")
    config_obj = get_config_obj()
    app.config.from_object(config_obj)

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
        from stone.models.user import User
        session = await session_interface.open(request)
        user_id = session.get("user_id")
        user = User.query.filter_by(id=user_id).first()
        if user:
            request['current_user'] = user

    @app.middleware('response')
    async def save_session(request, response):
        await session_interface.save(request, response)

