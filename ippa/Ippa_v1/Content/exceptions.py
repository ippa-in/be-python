class TxnCreationFailed(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)

class RewardRedeemed(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)

class NotEnoughPoints(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)

class TournamentCreationFailed(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)

class PromotionsExist(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)

class PromotionsDoesNotExist(Exception):
    def __init__(self, message, *args, **kwargs):
        Exception.__init__(self, message, *args, **kwargs)
        