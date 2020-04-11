import tkinter as tk

from gui.apps.temporal.briber_wizard.strategies.budget import BudgetFrame
from gui.apps.temporal.briber_wizard.strategies.even import EvenFrame
from gui.apps.temporal.briber_wizard.strategies.influential import InfluentialFrame
from gui.apps.temporal.briber_wizard.strategies.non import NonFrame
from gui.apps.temporal.briber_wizard.strategies.random import RandomFrame

STRAT_SUBFRAMES = (NonFrame, RandomFrame, InfluentialFrame, EvenFrame, BudgetFrame)
STRAT_DICT = {v: k for k, v in enumerate([a.name for a in STRAT_SUBFRAMES])}


class TemporalBriberWizardFrame(tk.Frame):
    """
    Frame for pop-up wizard for adding a temporal briber
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.strat_type = tk.StringVar(self)

        self.subframes = tuple(c(self) for c in STRAT_SUBFRAMES)
        self.options = tuple(f.get_name() for f in self.subframes)

        self.dropdown = tk.OptionMenu(self, self.strat_type, *self.options)
        self.dropdown.grid(row=0, column=0)

        self.strat_type.set(self.options[0])
        for f in self.subframes:
            f.grid(row=1, column=0, sticky="nsew")

        self.strat_type.trace('w', self.switch_frame)

        self.show_subframe(0)

        self.submit_button = tk.Button(self, text="Submit", command=self.add_briber)
        self.submit_button.grid(row=2, column=0)

    def show_subframe(self, page_no):
        frame = self.subframes[page_no]
        frame.tkraise()

    # noinspection PyUnusedLocal
    def switch_frame(self, *args):
        self.show_subframe(STRAT_DICT[self.strat_type.get()])

    def get_args(self):
        return self.subframes[STRAT_DICT[self.strat_type.get()]].get_args()

    def get_graph_type(self):
        return self.strat_type.get()

    def add_briber(self):
        self.parent.controller.add_briber(self.get_graph_type(), *(self.get_args()))
        self.parent.destroy()
