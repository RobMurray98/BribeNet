import enum


@enum.unique
class ActionType(enum.Enum):
    NONE = 0
    BRIBED = 1
    SELECT = 2
