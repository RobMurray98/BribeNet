import enum


@enum.unique
class RatingMethod(enum.Enum):
    O_RATING = 0
    P_RATING = 1
    MEDIAN_P_RATING = 2
    SAMPLE_P_RATING = 3
    P_GAMMA_RATING = 4
    WEIGHTED_P_RATING = 5
    WEIGHTED_MEDIAN_P_RATING = 6
