import tkinter as tk

from BribeNet.graph.ratingMethod import RatingMethod
from BribeNet.gui.apps.temporal.wizard.rating_methods.rating_method_frame import RatingMethodFrame


class PGammaRating(RatingMethodFrame):
    enum_value = RatingMethod.P_GAMMA_RATING
    name = 'p_gamma_rating'

    def __init__(self, parent):
        super().__init__(parent)

        self.params = {
            'gamma': tk.DoubleVar(self, value=0.05)
        }

        self.descriptions = {
            'gamma': 'dampening factor that defines the effect of nodes based on their distance'
        }

        self.grid_params(show_name=False)
