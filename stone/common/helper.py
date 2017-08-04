from stone.models.library import Library


def str2bool(value, default=False):
    assert isinstance(default, bool), "{} is not a boolean".format(default)

    if value is None:
        return default
    assert isinstance(value, str), "{} is not a string".format(value)

    if value.lower() in ["t", "1", "true", "y", "yes"]:
        return True
    if value.lower() in ["f", "0", "false", "n", "no"]:
        return False
    return default


async def get_current_library():
    lib = Library.query.first()
    return lib

