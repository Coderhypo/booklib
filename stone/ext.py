from sanic_jinja2 import SanicJinja2
from sanic_session import InMemorySessionInterface


jinja = SanicJinja2()
session_interface = InMemorySessionInterface(cookie_name="stone", prefix="stone")
