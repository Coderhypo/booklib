from sanic.blueprints import Blueprint

from stone.ext import jinja
from stone.froms.front import LoginForm, RegisterForm

index_blueprint = Blueprint("index")


@index_blueprint.route("/")
async def home(request):
    return jinja.render("index/index.html", request)


@index_blueprint.route("/random")
async def random(request):
    return jinja.render("index/books.html", request)


@index_blueprint.route("/faq")
async def faq(request):
    return jinja.render("index/faq.html", request)


@index_blueprint.route("/login", methods=["GET", "POST"])
async def login(request):
    form = LoginForm()
    if form.validate_on_submit():
        pass
    return jinja.render("index/login.html", request, form=form)


@index_blueprint.route("/register", methods=["GET", "POST"])
async def register(request):
    form = RegisterForm()
    if form.validate_on_submit():
        pass
    return jinja.render("index/register.html", request, form=form)

