from BribeNet.helpers.bribeNetException import BribeNetException


class BribeMustBeGreaterThanZeroException(BribeNetException):
    pass


class NodeDoesNotExistException(BribeNetException):
    pass


class BriberDoesNotExistException(BribeNetException):
    pass


class BriberyActionExceedsAvailableUtilityException(BribeNetException):
    pass
