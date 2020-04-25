import tkinter as tk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from gui.apps.temporal.results_wizard.window import TemporalResultsWizardWindow


class ResultsFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        replot_button = tk.Button(self, text="Change Variables", command=self.replot)
        replot_button.pack()

        exit_button = tk.Button(self, text="Exit", command=self.exit)
        exit_button.pack()

    def plot_results(self, results, xlbl, ylbl):
        self.ax.clear()
        # for each briber
        xs = results.get(xlbl)
        ys = results.get(ylbl)

        if not isinstance(xs[0], list) and not isinstance(ys[0], list):
            self.ax.plot(xs, ys)
        else:
            for b in range(0, len(self.controller.briber_names)):
                x_plot = [r[b] for r in xs] if isinstance(xs[0], list) else xs
                y_plot = [r[b] for r in ys] if isinstance(ys[0], list) else ys

                self.ax.plot(x_plot, y_plot, label=self.controller.briber_names[b])

            self.ax.legend()

        self.ax.set_xlabel(xlbl)
        self.ax.set_ylabel(ylbl)
        self.canvas.draw()

    def replot(self):
        results_wizard = TemporalResultsWizardWindow(self.controller, self.controller.results)
        results_wizard.lift()

    def exit(self):
        self.results = []
        self.controller.show_frame("GraphFrame")
