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

