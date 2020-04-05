import tkinter as tk

from gui.apps.static.wizard.algos.barabasi_albert import BarabasiAlbert
from gui.apps.static.wizard.algos.composite import Composite
from gui.apps.static.wizard.algos.watts_strogatz import WattsStrogatz

ALGO_SUBFRAMES = (BarabasiAlbert, Composite, WattsStrogatz)


class StaticGeneration(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.gtype = tk.StringVar(self)

        self.subframes = tuple(c(self) for c in ALGO_SUBFRAMES)
        self.options = tuple(f.name for f in self.subframes)

        self.dropdown = tk.OptionMenu(self, self.gtype, *self.options)
        self.dropdown.pack()

        self.gtype.set(self.options[0])
        self.subframes[0].pack()


