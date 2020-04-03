import tkinter as tk


class Main(tk.Frame):
    """
    Frame for the main menu of the GUI
    """

    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master=master, *args, **kwargs)
        title_text = tk.Label(self, text="Bribery Networks", font=("Calibri", 16, "bold"), pady=20)
        title_text.pack()
        static_button = tk.Button(self, text="Static Model", command=self.master.show_static_gui, pady=10)
        static_button.pack(pady=10)
        temporal_button = tk.Button(self, text="Temporal Model", command=self.master.show_temporal_gui, pady=10)
        temporal_button.pack()
