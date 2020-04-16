import abc
import tkinter as tk


class GeneratorAlgoFrame(tk.Frame, abc.ABC):
    name = "ABC"

    def __init__(self, parent):
        super().__init__(parent)
        self.params = {}
        self.descriptions = {}

    def get_args(self):
        return tuple(p.get() for p in self.params.values())

    def get_name(self):
        return self.name
