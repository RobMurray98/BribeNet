import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import rgb2hex
from networkit.viztasks import drawGraph

from gui.apps.temporal.results_wizard.window import TemporalResultsWizardWindow


class GraphFrame(tk.Frame):
    """
    Frame for showing the current state and actions that can be taken for the temporal model being run
    """

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.parent = parent
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.grid_rowconfigure(1, weight=1)
        self.canvas.get_tk_widget().grid(row=1, column=0, rowspan=10)
        self.results = []

        step_button = tk.Button(self, text="Next Step", command=self.controller.next_step)
        step_button.grid(row=3, column=2)

        results_button = tk.Button(self, text="Results", command=self.show_results_wizard)
        results_button.grid(row=4, column=2)

        exit_button = tk.Button(self, text="Exit", command=self.return_to_wizard)
        exit_button.grid(row=7, column=2)

        steps_slide = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL)
        steps_slide.grid(row=6, column=2)
        n_steps_button = tk.Button(self, text="Perform n steps", command=lambda: self.n_steps(steps_slide.get()))
        n_steps_button.grid(row=5, column=2)

        self.info = tk.StringVar(parent)
        round_desc_canvas = tk.Canvas(self)
        round_desc_scroll = tk.Scrollbar(self, orient='vertical', command=round_desc_canvas.yview)
        round_desc_frame = tk.Frame(self)
        round_desc_frame.bind(
            "<Configure>",
            lambda e: round_desc_canvas.configure(
                scrollregion=round_desc_canvas.bbox("all")
            )
        )
        round_desc_canvas.create_window((0, 0), window=round_desc_frame, anchor="n")
        round_desc_canvas.config(yscrollcommand=round_desc_scroll.set)
        round_desc_label = tk.Label(round_desc_frame, textvariable=self.info)
        round_desc_label.pack(fill=tk.BOTH, expand=1)

        round_desc_canvas.grid(row=1, column=1, columnspan=2, pady=10, padx=10, sticky='nsew')
        round_desc_scroll.grid(row=1, column=2, pady=10, sticky='nse')
        self.info.set("--")

    def return_to_wizard(self):
        self.results = []
        self.info.set("--")
        self.controller.clear_graph()
        self.controller.show_frame("WizardFrame")

    def set_info(self, s):
        self.info.set(s)

    def set_pos(self, pos):
        self.pos = pos

    def n_steps(self, n):
        for i in range(0, n):
            self.controller.next_step()

    def add_briber_buttons(self, bribers):

        view_txt = tk.StringVar(self)
        lbl = tk.Label(self, textvariable=view_txt)
        lbl.grid(row=2, column=1)
        view_txt.set("View rating for briber")

        none_bt = tk.Button(self, text="none", command=lambda: self.draw_basic_graph(self.controller.g))
        none_bt.grid(row=3, column=1)

        for i, c in enumerate(self.controller.bribers):
            bribe_bt = tk.Button(self, text=self.controller.briber_names[i],
                                 command=lambda i=i: self.draw_briber_graph(self.controller.g, i))
            bribe_bt.grid(row=(i + 4), column=1)

        trust_but = tk.Button(self, text="Show Trust", command=lambda: self.show_trust(self.controller.g))
        trust_but.grid(row=len(self.controller.bribers) + 4, column=1)

    def show_results_wizard(self):
        results_wizard = TemporalResultsWizardWindow(self.controller, self.controller.results)
        results_wizard.lift()

    def draw_basic_graph(self, graph):
        colors = ["gray" for c in graph.get_customers()]  # nodes
        edge_colors = ["#000000" for e in graph.get_edges()]  # edges
        self._update_graph(graph, colors, edge_colors)
        self.canvas.draw()

    def draw_briber_graph(self, graph, b):

        # node colors
        cmap = plt.get_cmap("Purples")
        colors = []
        for c in graph.get_customers():
            if np.isnan(graph.get_vote(c)[b]):
                colors.append("gray")
            else:
                colors.append(rgb2hex(cmap(graph.get_vote(c)[b])[:3]))
        edge_colors = ["#000000" for e in graph.get_edges()]  # edges

        self._update_graph(graph, colors, edge_colors)
        self._add_annotations(graph, b)
        self.canvas.draw()

    def _update_graph(self, graph, colors, edge_colors):

        self.ax.clear()
        drawGraph(
            graph.graph(),
            node_size=400,
            node_color=colors,
            edge_color=edge_colors,
            ax=self.ax, pos=self.pos,
            with_labels=True
        )

    def _add_annotations(self, graph, b):
        for c in graph.get_customers():
            if np.isnan(graph.get_vote(c)[b]):
                rating = "None"
            else:
                rating = round(graph.get_vote(c)[b], 2)

            self.ax.annotate(
                str(c) + ":\n"
                + "Vote: " + str(rating) + "\n"
                + "PRating: " + str(round(graph.get_rating(c), 2)),
                xy=(self.pos[c][0], self.pos[c][1]),
                bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
            )

    def show_trust(self, graph):

        colors = ["gray" for c in graph.get_customers()]  # nodes
        cmap = plt.get_cmap("Greys")
        edge_colors = []
        for (u, v) in graph.get_edges():
            edge_colors.append(rgb2hex(cmap(graph.get_weight(u, v))[:3]))
        self._update_graph(graph, colors, edge_colors)
        self.canvas.draw()
