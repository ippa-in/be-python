class TxnCreationFailed(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)

class RewardRedeemed(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)

class NotEnoughPoints(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)
        