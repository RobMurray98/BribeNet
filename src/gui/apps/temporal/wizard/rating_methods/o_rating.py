from graph.ratingMethod import RatingMethod
from gui.apps.temporal.wizard.rating_methods.rating_method_frame import RatingMethodFrame


class ORating(RatingMethodFrame):
    enum_value = RatingMethod.O_RATING
    name = 'o_rating'
