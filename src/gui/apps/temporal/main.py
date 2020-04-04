import tkinter as tk

from networkit.nxadapter import nk2nx
from networkx import spring_layout

from bribery.temporal.mostInfluentialNodeBriber import MostInfluentialNodeBriber
from bribery.temporal.oneMoveRandomBriber import OneMoveRandomBriber
from bribery.temporal.oneMoveEvenBriber import OneMoveEvenBriber
from bribery.temporal.nonBriber import NonBriber
from graph.temporal.thresholdGraph import ThresholdGraph

from graph.generation import GraphGeneratorAlgo
from graph.generation.flatWeightGenerator import FlatWeightedGraphGenerator

from graph.temporal.action.actionType import ActionType
from gui.apps.temporal.result import ResultsFrame

from gui.apps.temporal.wizard.wizard import WizardFrame
from gui.apps.temporal.graph import GraphFrame

from helpers.override import override

FRAMES_CLASSES = (WizardFrame, GraphFrame, ResultsFrame)

FRAMES_DICT = {i: c.__class__.__name__ for (i, c) in enumerate(FRAMES_CLASSES)}


def switch_briber(argument, u0=10):
    switcher = {
        "random": OneMoveRandomBriber(u0),
        "influential": MostInfluentialNodeBriber(u0),
        "non": NonBriber(u0),
        "even": OneMoveEvenBriber(u0)
    }
    return switcher.get(argument)


class TemporalGUI(tk.Tk):
    """
    Window for the temporal wizard and running environment
    """

    def __init__(self, controller, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.controller = controller

        # application window
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # frame for each displayed page
        self.frames = {}
        for F in FRAMES_CLASSES:
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(WizardFrame.__name__)
        self.bribers = []
        self.results = []
        self.briber_names = []
        self.g = None

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def add_briber(self, b, u0):
        self.bribers.append(switch_briber(b, u0=u0))
        self.briber_names.append(f"Briber{len(self.bribers)}: {b}: u0={u0}")

    def add_graph(self, gtype, args, params):
        if not self.bribers:
            raise RuntimeError("No Bribers added to graph")  # TODO replace with better error

        if gtype == "ba":
            gen = FlatWeightedGraphGenerator(
                GraphGeneratorAlgo.BARABASI_ALBERT,
                args[0], args[1], args[2])
        elif gtype == "cg":
            gen = FlatWeightedGraphGenerator(
                GraphGeneratorAlgo.COMPOSITE,
                args[0], args[1], args[2], args[3], args[4], args[5])
        else:
            gen = FlatWeightedGraphGenerator(
                GraphGeneratorAlgo.WATTS_STROGATZ,
                args[0], args[1], args[2])

        self.g = ThresholdGraph(
            tuple(self.bribers),
            generator=gen,
            threshold=params[0],
            d=params[1],
            q=params[2],
            apathy=params[3]
        )

        self.frames["GraphFrame"].set_pos(spring_layout(nk2nx(self.g.graph())))
        self.results.append([self.g.eval_graph(briber_id=b) for b in range(0, len(self.bribers))])

        for i in range(0, 10):
            print(f"{i}: --> {self.g.get_vote(i)}")

        self.frames["GraphFrame"].add_briber_buttons(self.bribers)
        self.frames["GraphFrame"].draw_graph(self.g)

    def plot_results(self):
        self.frames["ResultsFrame"].plot_results(self.results)
        self.results = []

    def next_step(self):

        self.g.step()
        self.results.append([self.g.eval_graph(briber_id=b) for b in range(0, len(self.bribers))])

        if self.g.get_time_step() % self.g.get_d() == self.g.get_d() - 1:
            info = "BRIBES\n"
            for bribers, bribe in self.g.get_last_bribery_action().get_bribes().items():
                for c, n in bribe.items():
                    info += f"Briber {bribers + 1}: {c} --> {n}\n"
        else:
            info = "CUSTOMERS\n"
            for c, a in self.g.get_last_customer_action().actions.items():
                if a[0] == ActionType.NONE:
                    info += f"Customer {c}: No Action\n"
                elif a[0] == ActionType.BRIBED:
                    info += f"Customer {c}: Bribed to {a[1]}\n"
                elif a[0] == ActionType.SELECT:
                    info += f"Customer {c}: Going to {a[1]}\n"
        self.frames["GraphFrame"].draw_graph(self.g)
        self.frames["GraphFrame"].set_info(info)

    @override
    def destroy(self):
        if self.controller is not None:
            self.controller.show_main()
        super().destroy()


if __name__ == '__main__':
    app = TemporalGUI(None)
    app.mainloop()
