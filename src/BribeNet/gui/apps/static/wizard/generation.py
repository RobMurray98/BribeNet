import tkinter as tk

from BribeNet.gui.apps.static.wizard.algos.barabasi_albert import BarabasiAlbert
from BribeNet.gui.apps.static.wizard.algos.composite import Composite
from BribeNet.gui.apps.static.wizard.algos.watts_strogatz import WattsStrogatz

ALGO_SUBFRAMES = (BarabasiAlbert, Composite, WattsStrogatz)
ALGO_DICT = {v: k for k, v in enumerate([a.name for a in ALGO_SUBFRAMES])}


class StaticGeneration(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.graph_type = tk.StringVar(self)

        title_label = tk.Label(self, text='Graph Generation Algorithm')
        title_label.grid(row=0, column=0, pady=10)

        self.subframes = tuple(c(self) for c in ALGO_SUBFRAMES)
        self.options = tuple(f.get_name() for f in self.subframes)

        self.dropdown = tk.OptionMenu(self, self.graph_type, *self.options)
        self.dropdown.grid(row=1, column=0, pady=10, sticky='nsew')

        self.graph_type.set(self.options[0])
        for f in self.subframes:
            f.grid(row=2, column=0, sticky="nsew")

        self.graph_type.trace('w', self.switch_frame)

        self.show_subframe(0)

    def show_subframe(self, page_no):
        frame = self.subframes[page_no]
        frame.tkraise()

    def switch_frame(self, *args):
        self.show_subframe(ALGO_DICT[self.graph_type.get()])

    def get_args(self):
        return self.subframes[ALGO_DICT[self.graph_type.get()]].get_args()

    def get_graph_type(self):
        return self.graph_type.get()
