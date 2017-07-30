import os

from stone.common.helper import str2bool


class BaseConfig(object):
    DATABASE_PATH = "sqlite:///data/db/stone.db"
    DOU_API_KEY = None
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(os.path.dirname(PROJECT_PATH), "data")
    SECRET_KEY = "THIS_A_KEY"
    COMMON_SALT = "SALT"
    WTF_CSRF_SECRET_KEY = SECRET_KEY + COMMON_SALT + ".WTF"


class DevConfig(BaseConfig):
    DEBUG = True


class ProConfig(BaseConfig):
    DEBUG = str2bool(os.getenv("DEBUG"))


def get_config_obj():
    runtime = os.getenv("RUNTIME", "DEFAULT")
    return app_config[runtime]


app_config = {
    "DEVELOPMENT": DevConfig,
    "PRODUCTION": ProConfig,
    "DEFAULT": ProConfig,
}

