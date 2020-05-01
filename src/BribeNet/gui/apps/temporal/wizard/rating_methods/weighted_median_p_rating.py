from BribeNet.graph.ratingMethod import RatingMethod
from BribeNet.gui.apps.temporal.wizard.rating_methods.rating_method_frame import RatingMethodFrame


class WeightedMedianPRating(RatingMethodFrame):
    enum_value = RatingMethod.WEIGHTED_MEDIAN_P_RATING
    name = 'weighted_median_p_rating'
