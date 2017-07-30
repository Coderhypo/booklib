class BaseError(Exception):
    error_id = ""
    error_msg = ""
    error_code = 500

    def __repr__(self):
        return "<{err_id} {err_code}>: {err_msg}".format(
            err_id=self.error_id,
            err_code=self.error_code,
            err_msg=self.error_msg,
        )

    def render(self):
        return dict(
            error_id=self.error_id,
            error_msg=self.error_msg,
        )


class ClientError(BaseError):

    def __init__(self, msg, error_code):
        self.error_id = "Third_Party_Dependent_Error"
        self.error_msg = msg
        self.error_code = error_code
