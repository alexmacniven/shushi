from click import ClickException


class ShushiException(ClickException):
    """Base exception."""
    def __init__(self, message=None, **kwargs):
        if not message:
            message = "Shushi encountered a problem."
        ClickException.__init__(self, message)


class IncorrectPassword(ShushiException):
    """Supplied password was incorrect."""
