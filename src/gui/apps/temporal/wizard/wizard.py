import tkinter as tk

from gui.apps.temporal.wizard.bribers import TemporalBribers
from gui.apps.temporal.wizard.generation import TemporalGeneration
from gui.apps.temporal.wizard.settings import TemporalSettings

SUBFRAME_CLASSES = (TemporalSettings, TemporalBribers, TemporalGeneration)
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

        self.subframes[TemporalSettings.__name__].grid(row=0, column=0, sticky="nsew")
        self.subframes[TemporalBribers.__name__].grid(row=0, column=1, sticky="nsew")
        self.subframes[TemporalGeneration.__name__].grid(row=1, column=0, sticky="nsew")

        run_button = tk.Button(self, text="Run", command=lambda: self.on_button())
        run_button.grid(row=1, column=1)

    def add_briber(self, b_type, u0):
        self.controller.add_briber(b_type, u0)
        txt = self.subframes[TemporalBribers.__name__].bribers_txt.get()
        txt += f"\n{b_type}: u0={u0}"
        self.subframes[TemporalBribers.__name__].bribers_txt.set(txt)

    def on_button(self):
        gtype = self.subframes[TemporalGeneration.__name__].get_graph_type()
        args = self.subframes[TemporalGeneration.__name__].get_args()
        # check some bribers on graph
        if self.subframes[TemporalBribers.__name__].bribers_txt.get() == "":
            tk.messagebox.showerror(message="Graph needs one or more bribers")
            return

        params = self.subframes[TemporalSettings.__name__].get_graph_params()

        self.controller.add_graph(gtype, args, params)
        self.controller.show_frame("GraphFrame")
