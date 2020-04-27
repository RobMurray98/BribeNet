from graph.ratingMethod import RatingMethod
from gui.apps.temporal.wizard.rating_methods.rating_method_frame import RatingMethodFrame


class MedianPRating(RatingMethodFrame):
    enum_value = RatingMethod.MEDIAN_P_RATING
    name = 'median_p_rating'
