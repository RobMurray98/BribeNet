import abc
import os
import tkinter as tk

from PIL import ImageTk, Image

from BribeNet.gui.classes.tooltip import ToolTip


class ParamListFrame(tk.Frame, abc.ABC):
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

    def grid_params(self, show_name=True):
        offset = 0
        if show_name:
            name_label = tk.Label(self, text=self.name)
            name_label.grid(row=0, column=0, columnspan=3, pady=10)
            offset = 1
        for i, (name, var) in enumerate(self.params.items()):
            label = tk.Label(self, text=name)
            label.grid(row=i + offset, column=0)
            canvas_frame = tk.Frame(self)
            canvas = tk.Canvas(master=canvas_frame, width=16, height=16)
            self.tooltips.append(ToolTip(canvas_frame, self.descriptions[name]))
            canvas_frame.bind('<Enter>', self.tooltips[i].show_tip)
            canvas_frame.bind('<Leave>', self.tooltips[i].hide_tip)
            self.images.append(canvas.create_image(0, 0, anchor=tk.NW, image=self.info_img))
            entry = tk.Entry(self, textvariable=var)
            canvas.pack()
            canvas_frame.grid(row=i + offset, column=1, padx=30)
            entry.grid(row=i + offset, column=2)
