from graph.ratingMethod import RatingMethod
from gui.apps.temporal.wizard.rating_methods.rating_method_frame import RatingMethodFrame


class PRating(RatingMethodFrame):
    enum_value = RatingMethod.P_RATING
    name = 'p_rating'
