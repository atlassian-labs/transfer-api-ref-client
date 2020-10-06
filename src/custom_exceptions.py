class AuthException(Exception):
    def __init__(self, error_message):
        self.message = error_message

    def __str__(self):
        return self.message
