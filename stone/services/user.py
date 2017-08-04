from stone.models import db_session as session
from stone.models.user import User


async def create_user(username, email, password):
    user = User(username, email, password)
    session.add(user)
    session.commit()
    return user


def gen_username_by_email(email):
    username, domain = email.split('@')
    username = (" ".join([w.capitalize() for w in username.split(".")]))
    return username


