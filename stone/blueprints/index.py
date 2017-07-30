from sanic.blueprints import Blueprint
from sanic.response import redirect

from stone.ext import jinja
from stone.froms.front import LoginForm, RegisterForm
from stone.services.user import create_user, get_username_by_email
from stone.models.user import User

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
    form = LoginForm(request)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        request['session'].update(dict(user_id=user.id))
        return redirect("/dashboard")
    return jinja.render("index/login.html", request, form=form)


@index_blueprint.route("/register", methods=["GET", "POST"])
async def register(request):
    form = RegisterForm(request)
    if form.validate_on_submit():
        user = await create_user(
            get_username_by_email(form.email.data),
            form.email.data,
            form.password.data
        )
        request['session'].update(dict(user_id=user.id))
        return redirect("/dashboard")
    return jinja.render("index/register.html", request, form=form)
