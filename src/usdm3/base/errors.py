import traceback
from d4k_sel.errors import Errors as SelErrors
from d4k_sel.error_location import ErrorLocation as SelErrorLocation


class Errors:
    ERROR = SelErrors.ERROR
    WARNING = SelErrors.WARNING
    DEBUG = SelErrors.DEBUG
    INFO = SelErrors.INFO

    def __init__(self):
        self.errors = SelErrors()

    def exception(self, message: str, e: Exception, location: SelErrorLocation):
        message = f"Exception '{e}' raised. {message}"
        self.errors.add(message, location, self.errors.ERROR)
        message = f"Tracsback for the previous error:\n\n{traceback.format_exc()}"
        self.errors.add(message, location, self.errors.ERROR)
        print(self.dump())

    def error(self, message: str, location: SelErrorLocation):
        self.errors.add(message, location, self.errors.ERROR)

    def warning(self, message: str, location: SelErrorLocation):
        self.errors.add(message, location, self.errors.WARNING)

    def dump(self):
        return self.errors.dump(self.ERROR)
