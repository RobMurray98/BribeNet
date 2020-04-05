import tkinter as tk


class GeneratorAlgoFrame(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.name = "UNDEFINED"
        self.params = {}
        self.descriptions = {}
