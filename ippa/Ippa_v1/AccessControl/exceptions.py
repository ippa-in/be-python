class ACCOUNT_ALREADY_EXISTS(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)

class ACTION_NOT_ALLOWED(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)

class EMAIL_ALREADY_VERIFIED(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)