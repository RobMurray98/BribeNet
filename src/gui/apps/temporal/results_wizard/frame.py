import tkinter as tk


class TemporalResultsWizardFrame(tk.Frame):
    """
    Frame for pop-up wizard for selecting results displayed
    """

    def __init__(self, parent, results):
        super().__init__(parent)
        self.parent = parent

        self.x_string_var = tk.StringVar(self)
        self.y_string_var = tk.StringVar(self)

        self.title_text = tk.Label(self, text="Select Values", font=("Calibri", 16, "bold"), pady=20)
        self.title_text.grid(row=0, column=0, columnspan=2)

        self.x_text = tk.Label(self, text="X-axis", padx=20, pady=10)
        self.x_text.grid(row=1, column=0)

        self.y_text = tk.Label(self, text="Y-axis", padx=20, pady=10)
        self.y_text.grid(row=2, column=0)

        x_options = results.get_x_options()
        self.x_string_var.set(x_options[0])
        self.drop_xs = tk.OptionMenu(self, self.x_string_var, *x_options)
        self.drop_xs.grid(row=1, column=1, sticky='ew')

        y_options = results.get_y_options()
        self.y_string_var.set(y_options[0])
        self.drop_ys = tk.OptionMenu(self, self.y_string_var, *y_options)
        self.drop_ys.grid(row=2, column=1, sticky='ew')

        self.submit_button = tk.Button(self, text="Submit", command=self.submit)
        self.submit_button.grid(row=3, column=0, columnspan=2, pady=20, sticky='nsew')

    def submit(self):
        self.parent.controller.plot_results(self.x_string_var.get(), self.y_string_var.get())
        self.parent.destroy()
