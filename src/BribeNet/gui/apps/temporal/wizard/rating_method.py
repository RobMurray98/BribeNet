import tkinter as tk

from BribeNet.graph.ratingMethod import RatingMethod
from BribeNet.gui.apps.temporal.wizard.rating_methods.median_p_rating import MedianPRating
from BribeNet.gui.apps.temporal.wizard.rating_methods.o_rating import ORating
from BribeNet.gui.apps.temporal.wizard.rating_methods.p_gamma_rating import PGammaRating
from BribeNet.gui.apps.temporal.wizard.rating_methods.p_rating import PRating
from BribeNet.gui.apps.temporal.wizard.rating_methods.weighted_median_p_rating import WeightedMedianPRating
from BribeNet.gui.apps.temporal.wizard.rating_methods.weighted_p_rating import WeightedPRating

METHOD_SUBFRAMES = (ORating, PRating, MedianPRating, PGammaRating, WeightedPRating, WeightedMedianPRating)
METHOD_DICT = {v: k for k, v in enumerate([a.name for a in METHOD_SUBFRAMES])}


class TemporalRatingMethod(tk.Frame):
    """
    Frame for pop-up wizard for adding a temporal briber
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.method_type = tk.StringVar(self)

        self.subframes = tuple(c(self) for c in METHOD_SUBFRAMES)
        self.options = tuple(f.get_name() for f in self.subframes)

        name_label = tk.Label(self, text="Rating Method")
        name_label.grid(row=0, column=0, pady=10)

        self.dropdown = tk.OptionMenu(self, self.method_type, *self.options)
        self.dropdown.grid(row=1, column=0, pady=10)

        self.method_type.set(self.options[0])
        for f in self.subframes:
            f.grid(row=2, column=0, sticky="nsew", pady=20)

        self.method_type.trace('w', self.switch_frame)

        self.show_subframe(1)  # (p-rating)

    def show_subframe(self, page_no):
        frame = self.subframes[page_no]
        frame.tkraise()

    # noinspection PyUnusedLocal
    def switch_frame(self, *args):
        self.show_subframe(METHOD_DICT[self.method_type.get()])

    def get_rating_method(self) -> RatingMethod:
        return self.subframes[METHOD_DICT[self.method_type.get()]].enum_value

    def get_args(self):
        return self.subframes[METHOD_DICT[self.method_type.get()]].get_args()
