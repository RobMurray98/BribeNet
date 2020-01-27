import enum


@enum.unique
class RatingMethod(enum.Enum):
    O_RATING = 0
    P_RATING = 1
    MEDIAN_P_RATING = 2
    SAMPLE_P_RATING = 3
    PK_RATING = 4

