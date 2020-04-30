import tkinter as tk

from gui.apps.main import Main
from gui.apps.static.static import StaticGUI
from gui.apps.temporal.main import TemporalGUI
from helpers.override import override


class GUI(tk.Tk):
    """
    Main menu window for the GUI
    Self-withdraws when model wizard opened, and deiconifies when wizard closed
    """

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Bribery Networks")
        self.main_frame = Main(self)
        self.main_frame.grid(row=1, column=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.minsize(400, 400)
        self.static_gui = None
        self.temporal_gui = None

    def show_static_gui(self):
        if (self.static_gui is None) and (self.temporal_gui is None):
            self.static_gui = StaticGUI(self)
            self.withdraw()

    def show_temporal_gui(self):
        if (self.static_gui is None) and (self.temporal_gui is None):
            self.temporal_gui = TemporalGUI(self)
            self.withdraw()

    def show_main(self):
        self.static_gui = None
        self.temporal_gui = None
        self.deiconify()

    @override
    def destroy(self):
        if self.static_gui is not None:
            self.static_gui.destroy()
        if self.temporal_gui is not None:
            self.temporal_gui.destroy()
        super().destroy()


if __name__ == "__main__":
    app = GUI()
    app.mainloop()
