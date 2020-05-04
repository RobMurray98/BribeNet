import tkinter as tk

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import rgb2hex
from networkit.viztasks import drawGraph

from BribeNet.gui.apps.temporal.results_wizard.window import TemporalResultsWizardWindow


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
        self.pos = None
        self.gamma = None
        self.briber_buttons = None
        self.briber_name_to_index = None
        self.rating_string_var = None

        step_button = tk.Button(self, text="Next Step", command=self.controller.next_step)
        step_button.grid(row=3, column=2, sticky='nsew')

        results_button = tk.Button(self, text="Results", command=self.show_results_wizard)
        results_button.grid(row=4, column=2, sticky='nsew')

        exit_button = tk.Button(self, text="Exit", command=self.return_to_wizard)
        exit_button.grid(row=7, column=2, sticky='nsew')

        steps_slide = tk.Scale(self, from_=1, to=100, orient=tk.HORIZONTAL)
        steps_slide.grid(row=6, column=2, sticky='nsew')
        n_steps_button = tk.Button(self, text="Perform n steps", command=lambda: self.n_steps(steps_slide.get()))
        n_steps_button.grid(row=5, column=2, sticky='nsew')

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

    def add_briber_dropdown(self):

        view_title_label = tk.Label(self, text="View rating for briber")
        view_title_label.grid(row=3, column=1)

        rating_choices = ['None'] + self.controller.briber_names

        self.briber_name_to_index = {v: k for k, v in enumerate(self.controller.briber_names)}
        self.rating_string_var = tk.StringVar(self)
        self.rating_string_var.set('None')

        rating_dropdown = tk.OptionMenu(self, self.rating_string_var, *rating_choices)

        # noinspection PyUnusedLocal
        def change_dropdown(*args):
            var_val = self.rating_string_var.get()
            if var_val == 'None':
                self.draw_basic_graph(self.controller.g)
            else:
                self.draw_briber_graph(self.briber_name_to_index[var_val])

        self.rating_string_var.trace('w', change_dropdown)

        rating_dropdown.grid(row=4, column=1, sticky='nsew')

        trust_button = tk.Button(self, text="Show Trust", command=lambda: self.show_trust(self.controller.g))
        trust_button.grid(row=6, column=1, sticky='nsew')

    def show_results_wizard(self):
        results_wizard = TemporalResultsWizardWindow(self.controller, self.controller.results)
        results_wizard.lift()

    def draw_basic_graph(self, graph):
        colours = ["gray" for _ in graph.get_customers()]  # nodes
        edge_colours = ["#000000" for _ in graph.get_edges()]  # edges
        self._update_graph(graph, colours, edge_colours)
        self.canvas.draw()

    def draw_briber_graph(self, b):

        # node colours
        graph = self.controller.g

        colour_map = plt.get_cmap("Purples")
        colours = []
        for c in graph.get_customers():
            if np.isnan(graph.get_vote(c)[b]):
                colours.append("gray")
            else:
                colours.append(rgb2hex(colour_map(graph.get_vote(c)[b])[:3]))
        edge_colours = ["#000000" for _ in graph.get_edges()]  # edges

        self._update_graph(graph, colours, edge_colours)
        self._add_annotations(b)
        self.canvas.draw()

    def _update_graph(self, graph, colours, edge_colours):

        self.ax.clear()
        drawGraph(
            graph.get_graph(),
            node_size=400,
            node_color=colours,
            edge_color=edge_colours,
            ax=self.ax, pos=self.pos,
            with_labels=True
        )

    def _add_annotations(self, b):
        graph = self.controller.g
        for c in graph.get_customers():
            if np.isnan(graph.get_vote(c)[b]):
                rating = "None"
            else:
                rating = round(graph.get_vote(c)[b], 2)

            self.ax.annotate(
                str(c) + ":\n"
                + "Vote: " + str(rating) + "\n"
                + "Rating: " + str(round(graph.get_rating(c), 2)),
                xy=(self.pos[c][0], self.pos[c][1]),
                bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
            )

    def show_trust(self, graph):

        colours = ["gray" for _ in graph.get_customers()]  # nodes
        colour_map = plt.get_cmap("Greys")
        edge_colours = []
        for (u, v) in graph.get_edges():
            edge_colours.append(rgb2hex(colour_map(graph.get_weight(u, v))[:3]))
        self._update_graph(graph, colours, edge_colours)
        self.canvas.draw()
