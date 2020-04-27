import tkinter as tk

from graph.ratingMethod import RatingMethod
from gui.apps.temporal.wizard.bribers import TemporalBribers
from gui.apps.temporal.wizard.generation import TemporalGeneration
from gui.apps.temporal.wizard.rating_method import TemporalRatingMethod
from gui.apps.temporal.wizard.settings import TemporalSettings

SUBFRAME_CLASSES = (TemporalSettings, TemporalBribers, TemporalGeneration, TemporalRatingMethod)
SUBFRAME_DICT = {i: c.__class__.__name__ for (i, c) in enumerate(SUBFRAME_CLASSES)}


class WizardFrame(tk.Frame):
    """
    Frame for the wizard to construct a temporal model run
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        self.subframes = {}

        for c in SUBFRAME_CLASSES:
            page_name = c.__name__
            frame = c(self)
            self.subframes[page_name] = frame

        self.subframes[TemporalSettings.__name__].grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.subframes[TemporalBribers.__name__].grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        self.subframes[TemporalGeneration.__name__].grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self.subframes[TemporalRatingMethod.__name__].grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        run_button = tk.Button(self, text="Run", command=self.on_button)
        run_button.grid(row=2, column=1, pady=20, sticky='se')

    def add_briber(self, b_type, u0):
        self.controller.add_briber(b_type, u0)

    def on_button(self):
        graph_type = self.subframes[TemporalGeneration.__name__].get_graph_type()
        graph_args = self.subframes[TemporalGeneration.__name__].get_args()
        bribers = self.subframes[TemporalBribers.__name__].get_all_bribers()
        rating_method = self.subframes[TemporalRatingMethod.__name__].get_rating_method()
        rating_method_args = self.subframes[TemporalRatingMethod.__name__].get_args()

        if not bribers:
            # noinspection PyUnresolvedReferences
            tk.messagebox.showerror(message="Graph needs one or more bribers")
            return

        try:
            for briber in bribers:
                strat_type = briber[0]
                briber_args = briber[1:]
                self.controller.add_briber(strat_type, *briber_args)
            params = self.subframes[TemporalSettings.__name__].get_args()
            self.controller.add_graph(graph_type, graph_args, params)
            self.controller.g.set_rating_method(rating_method)
            if rating_method == RatingMethod.P_GAMMA_RATING:
                self.controller.g.set_gamma(rating_method_args[0])
            self.controller.update_results()
        except Exception as e:
            # noinspection PyUnresolvedReferences
            tk.messagebox.showerror(message=f"{e.__class__.__name__}: {str(e)}")
            self.controller.clear_graph()
            return

        self.controller.show_frame("GraphFrame")
