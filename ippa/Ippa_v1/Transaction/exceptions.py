class BANK_ACC_NOT_EXIST(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)

class LESS_POINTS(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)
        