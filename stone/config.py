import os

from stone.common.helper import str2bool


class BaseConfig(object):
    DATABASE_PATH = "sqlite:///stone.db"


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

