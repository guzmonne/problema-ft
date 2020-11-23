class CustomException(Exception):
    """Base class for custom exceptions"""
    def __init__(self, *args, **kwargs):
        self.message = self.init(*args, **kwargs)
        if self.message is not None:
            super().__init__(self.message)

    def init(self):
        pass