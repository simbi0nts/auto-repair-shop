
class MethodNotFound(Exception):
    def __init__(self, request_method: str):
        message = f"Method process_{request_method.lower()} not found in context processor"
        super().__init__(message)


class WrongArgumentsHasBeenPassed(Exception):
    pass


class ProcessorNotFound(Exception):
    pass
