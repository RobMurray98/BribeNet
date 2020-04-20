import abc
import os
import tkinter as tk

from PIL import ImageTk, Image

from gui.classes.tooltip import ToolTip


class StrategyFrame(tk.Frame, abc.ABC):
    name = "ABC"

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.params = {}
        self.descriptions = {}
        img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'info.png')
        self.info_img = ImageTk.PhotoImage(Image.open(img_path))
        self.tooltips = []
        self.images = []

    def get_args(self):
        return tuple(p.get() for p in self.params.values())

    def get_name(self):
        return self.name

    def grid_params(self):
        for i, (name, var) in enumerate(self.params.items()):
            label = tk.Label(self, text=name)
            label.grid(row=i, column=0)
            canvas_frame = tk.Frame(self)
            canvas = tk.Canvas(master=canvas_frame, width=16, height=16)
            self.tooltips.append(ToolTip(canvas_frame, self.descriptions[name]))
            canvas_frame.bind('<Enter>', self.tooltips[i].show_tip)
            canvas_frame.bind('<Leave>', self.tooltips[i].hide_tip)
            self.images.append(canvas.create_image(0, 0, anchor=tk.NW, image=self.info_img))
            entry = tk.Entry(self, textvariable=var)
            canvas.pack()
            canvas_frame.grid(row=i, column=1, padx=30)
            entry.grid(row=i, column=2)

