#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk

import matplotlib.pyplot as plt
import networkit as nk
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.colors import rgb2hex
from networkit.nxadapter import nk2nx
from networkit.viztasks import drawGraph
from networkx import spring_layout

# Import Bribing Agents
from bribery.temporal.oneMoveInfluentialNodeBriber import OneMoveInfluentialNodeBriber
from bribery.temporal.oneMoveRandomBriber import OneMoveRandomBriber
from bribery.temporal.nonBriber import NonBriber
from graph.temporal.thresholdGraph import ThresholdGraph


def switch_briber(argument):
    switcher = {
        "random": OneMoveRandomBriber(10),
        "influential": OneMoveInfluentialNodeBriber(10),
        "non": NonBriber(10)
    }
    return switcher.get(argument)


# outer layer of application
# links start page with graph page
class GUI(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # application window
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # frame for each displayed page
        self.frames = {}
        for F in [StartPage, GraphFrame, ResultsFrame]:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
        self.bribers = []
        self.results = []

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def add_briber(self, b):
        self.bribers.append(switch_briber(b))

    def add_graph(self, gtype):

        if self.bribers == []:
            raise RuntimeError("No Bribers added to graph") # @TODO replace with better error

        ba_gen = nk.generators.BarabasiAlbertGenerator(5, 30, 0, True)

        self.g = ThresholdGraph(tuple(self.bribers)) if gtype == "ws" else ThresholdGraph(tuple(self.bribers), generator=ba_gen)
        for b in self.bribers:
            print(b.get_graph())

        self.frames["GraphFrame"].set_pos(spring_layout(nk2nx(self.g.graph())))
        self.results.append(self.g.eval_graph())

        print(self.g.eval_graph())
        for i in range(0, 10):
            print(f"{i}: -->{self.g.get_vote(i)}")

        self.frames["GraphFrame"].add_briber_buttons(self.bribers)
        self.frames["GraphFrame"].draw_graph(self.g)

    def plot_results(self, results):
        self.frames["ResultsFrame"].plot_results(results)

    def next_step(self):

        self.g.step()

        info = ""
        if self.g.get_time_step() % 2 == 1:
            info = "Bribes\n"
            for brbr, brb in self.g.get_last_bribery_action().bribes.items():
                for c, n in brb.items():
                    info += f"Briber {brbr + 1}: {c} --> {n}\n"
        else:
            info = self.g.get_last_customer_action()

        self.frames["GraphFrame"].draw_graph(self.g)
        self.frames["GraphFrame"].set_info(info)


# page for selection of graph and bribery method
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        gtype = tk.StringVar()
        gtype.set("L")
        btype = tk.StringVar()
        btype.set("L")

        rb1 = tk.Radiobutton(self, variable=gtype, value="ws", text="Watts-Strogatz")
        rb2 = tk.Radiobutton(self, variable=gtype, value="ba", text="Barabási–Albert")
        rb1.grid(row=0, column=0)
        rb2.grid(row=1, column=0)

        self.bribe_ns = {
            "random": tk.IntVar(),
            "influential": tk.IntVar(),
            "non": tk.IntVar()
        }
        for n, (b, v) in enumerate(self.bribe_ns.items()):

            txt = tk.StringVar()
            lbl = tk.Label(self, textvariable=txt)
            lbl.grid(row=n, column=3)
            txt.set(b)

            var_entry = tk.Entry(self, text=b, textvariable=v)
            var_entry.grid(row=n, column=5)

        b = tk.Button(self, text="Graph + Test", command=lambda: self.on_button(gtype.get()))
        b.grid(row=len(self.bribe_ns), column=2)

    def on_button(self, gtype):
        #check some bribers on graph
        if sum([v.get() for _, v in self.bribe_ns.items()]) <= 0:
            tk.messagebox.showerror(messgae="Graph needs one or more bribers")
            return
        # add bribers
        for b, v in self.bribe_ns.items():
            for i in range(0, v.get()):
                self.controller.add_briber(b)

        self.controller.add_graph(gtype)
        self.controller.show_frame("GraphFrame")



# page for displaying and running graph
class GraphFrame(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(row=1, column=0)
        self.results = []



        button3 = tk.Button(self, text="Next Step", command=lambda: self.controller.next_step())
        button3.grid(row=3, column=2)

        button4 = tk.Button(self, text="Results", command=lambda: self.to_results())
        button4.grid(row=4, column=2)

        button1 = tk.Button(self, text="Exit", command=lambda: self.controller.show_frame("StartPage"))
        button1.grid(row=5, column=2)

        self.info = tk.StringVar()
        lbl = tk.Label(self, textvariable=self.info)
        lbl.grid(row=1, column=1, columnspan=2)
        self.info.set("--")

    def set_info(self, s):
        self.info.set(s)

    def set_pos(self, pos):
        self.pos = pos

    def add_briber_buttons(self, bribers):

        view_txt = tk.StringVar()
        lbl = tk.Label(self, textvariable=view_txt)
        lbl.grid(row=2, column=1)
        view_txt.set("View rating for briber")

        none_bt = tk.Button(self, text="none", command=lambda: self.draw_graph(self.controller.g))
        none_bt.grid(row=3, column=1)

        for i, c in enumerate(self.controller.bribers):

            bribe_bt = tk.Button(self, text=str(i+1), command=lambda i=i: self.draw_graph(self.controller.g, briber=i))
            bribe_bt.grid(row=(i+4), column=1)


    def to_results(self):
        self.controller.plot_results(self.results)
        self.results = []
        self.controller.show_frame("ResultsFrame")

    def draw_graph(self, graph, **kwargs):

        colors = ["gray" for c in graph.get_customers()]
        if "briber" in kwargs:
            b = kwargs["briber"]

            # set clolours for nodes
            cmap = plt.get_cmap("Purples")
            colors = []
            for c in graph.get_customers():
                if np.isnan(graph.get_vote(c)[b]):
                    colors.append("gray")
                else:
                    colors.append(rgb2hex(cmap(graph.get_vote(c)[b])[:3]))

        #default edges black
        edge_colors = ["#000000" for e in graph.get_edges()]

        # set colours for edges proportional to trust
        cmap2 = plt.get_cmap("Greys")
        if "trust" in kwargs and kwargs["trust"]:
            edge_colors = []
            for (u, v) in graph.get_edges():
                edge_colors.append(rgb2hex(cmap2(graph.get_weight(u, v))[:3]))

        self.ax.clear()

        drawGraph(graph.graph(),
            node_size=400,
            node_color=colors,
            edge_color=edge_colors,
            ax=self.ax, pos=self.pos
        )

        if "briber" in kwargs:

            b = kwargs["briber"]

            # annotate votes on graph
            for c in graph.get_customers():
                if np.isnan(graph.get_vote(c)[b]):
                    rating = "None"
                else:
                    rating = round(graph.get_vote(c)[b], 2)

                self.ax.annotate(
                    str(c) + ":\n" +
                    "Rating: " + str(rating) + "\n" +
                    "PRating: " + str(round(graph.get_rating(c), 2)),
                    xy=(self.pos[c][0], self.pos[c][1]),
                    bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
                )

        # Show last bribe for bribers
        if "last" in kwargs:

            for n, c in zip(kwargs["last"], bribe_colors):
                self.ax.add_artist(plt.Circle(
                    (self.pos[n][0], self.pos[n][1]), 0.1,
                    color=c,
                    fill=False,
                    linewidth=3.0
                ))

        self.canvas.draw()

        # avp = str(round(graph.eval_graph(), 2))
        # if last < 0:
        #     self.txt.set("Average P-Rating: " + avp + " \nLast Bribed: --")
        # else:
        #     self.txt.set("Average P-Rating: " + avp + " \nLast Bribed: " + str(last))

    # def next_bribe(self):
    #     c = self.briber.next_bribe()
    #     self.display_graph(last=c)
    #     avp = self.graph.eval_graph()
    #     self.results.append(avp)
    #     self.canvas.draw()

    # def show_influential(self):
    #     cmap = plt.get_cmap("Purples")
    #     colors = []
    #
    #     for c in self.graph.get_customers():
    #         if self.graph.is_influential(c, charge_briber=False):
    #             colors.append("yellow")
    #         elif np.isnan(self.graph.get_vote(c)):
    #             colors.append("gray")
    #         else:
    #             colors.append(rgb2hex(cmap(self.graph.get_vote(c)[0])[:3]))
    #     self.ax.clear()
    #
    #     for c in self.graph.get_customers():
    #         rating = ""
    #         if np.isnan(self.graph.get_vote(c)):
    #             rating = "None"
    #         else:
    #             rating = round(self.graph.get_vote(c)[0], 2)
    #
    #         self.ax.annotate(
    #             str(c) + ":\n" +
    #             "Rating: " + str(rating) + "\n" +
    #             "PRating: " + str(round(self.graph.get_rating(c), 2)),
    #             xy=(self.pos[c][0], self.pos[c][1]),
    #             bbox=dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
    #         )
    #     drawGraph(self.graph.graph(), node_size=500, node_color=colors, ax=self.ax, pos=self.pos)
    #     self.canvas.draw()


class ResultsFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        button1 = tk.Button(self, text="Exit", command=lambda: self.exit())
        button1.pack()

    def plot_results(self, results):
        xs = [i for i in range(0, len(results))]
        self.ax.clear()
        self.ax.plot(xs, results)
        self.ax.set_xlabel("Moves over time")
        self.ax.set_ylabel("Average P-rating")
        self.canvas.draw()

    def exit(self):
        self.results = []
        self.controller.show_frame("StartPage")


if __name__ == '__main__':
    app = GUI()
    app.mainloop()
