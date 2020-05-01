from BribeNet.graph.ratingMethod import RatingMethod
from BribeNet.gui.apps.temporal.wizard.rating_methods.rating_method_frame import RatingMethodFrame


class WeightedPRating(RatingMethodFrame):
    enum_value = RatingMethod.WEIGHTED_P_RATING
    name = 'weighted_p_rating'
