class BaseError(Exception):
    error_id = ""
    error_msg = ""

    def __repr__(self):
        return "<{err_id}>: {err_msg}".format(
            err_id=self.error_id,
            err_msg=self.error_msg,
        )

    def render(self):
        return dict(
            error_id=self.error_id,
            error_msg=self.error_msg,
        )


class ClientError(BaseError):
    error_id = "Third_Party_Dependent_Error"

    def __init__(self, error_msg):
        self.error_msg = error_msg


class BookNotFound(BaseError):
    error_id = "Book_Not_Found"

    def __init__(self, error_msg):
        self.error_msg = error_msg


class UserNotFound(BaseError):
    error_id = "User_Not_Found"

    def __init__(self, error_msg):
        self.error_msg = error_msg


class RecommendedNotFound(BaseError):
    error_id = "Recommended_Not_Found"

    def __init__(self, error_msg):
        self.error_msg = error_msg
