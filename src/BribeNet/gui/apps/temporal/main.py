import tkinter as tk
import os

from networkit.nxadapter import nk2nx
from networkx import spring_layout

from BribeNet.bribery.temporal.budgetNodeBriber import BudgetNodeBriber
from BribeNet.bribery.temporal.influentialNodeBriber import InfluentialNodeBriber
from BribeNet.bribery.temporal.mostInfluentialNodeBriber import MostInfluentialNodeBriber
from BribeNet.bribery.temporal.nonBriber import NonBriber
from BribeNet.bribery.temporal.oneMoveEvenBriber import OneMoveEvenBriber
from BribeNet.bribery.temporal.oneMoveRandomBriber import OneMoveRandomBriber
from BribeNet.bribery.temporal.pGreedyBriber import PGreedyBriber
from BribeNet.graph.generation import GraphGeneratorAlgo
from BribeNet.graph.generation.flatWeightGenerator import FlatWeightedGraphGenerator
from BribeNet.graph.temporal.action.actionType import ActionType
from BribeNet.graph.temporal.thresholdGraph import ThresholdGraph
from BribeNet.gui.apps.static.wizard.algos.barabasi_albert import BarabasiAlbert
from BribeNet.gui.apps.static.wizard.algos.composite import Composite
from BribeNet.gui.apps.temporal.briber_wizard.strategies.budget import BudgetFrame
from BribeNet.gui.apps.temporal.briber_wizard.strategies.even import EvenFrame
from BribeNet.gui.apps.temporal.briber_wizard.strategies.influential import InfluentialFrame
from BribeNet.gui.apps.temporal.briber_wizard.strategies.most_influential import MostInfluentialFrame
from BribeNet.gui.apps.temporal.briber_wizard.strategies.non import NonFrame
from BribeNet.gui.apps.temporal.briber_wizard.strategies.p_greedy import PGreedyFrame
from BribeNet.gui.apps.temporal.briber_wizard.strategies.random import RandomFrame
from BribeNet.gui.apps.temporal.graph import GraphFrame
from BribeNet.gui.apps.temporal.result import ResultsFrame
from BribeNet.gui.apps.temporal.results_wizard.results import ResultsStore
from BribeNet.gui.apps.temporal.wizard.wizard import WizardFrame
from BribeNet.helpers.override import override

FRAMES_CLASSES = (WizardFrame, GraphFrame, ResultsFrame)

FRAMES_DICT = {i: c.__class__.__name__ for (i, c) in enumerate(FRAMES_CLASSES)}

X_AXIS_OPTIONS = ("Time", "Utility Spent")
Y_AXIS_OPTIONS = ("Average Rating", "Total Utility", "Average Trust")


def switch_briber(strategy_type, *args):
    switcher = {
        RandomFrame.name: OneMoveRandomBriber,
        InfluentialFrame.name: InfluentialNodeBriber,
        MostInfluentialFrame.name: MostInfluentialNodeBriber,
        NonFrame.name: NonBriber,
        EvenFrame.name: OneMoveEvenBriber,
        BudgetFrame.name: BudgetNodeBriber,
        PGreedyFrame.name: PGreedyBriber
    }
    return switcher.get(strategy_type)(*args)


class TemporalGUI(tk.Toplevel):
    """
    Window for the temporal wizard and running environment
    """

    def __init__(self, controller, *args, **kwargs):
        super().__init__(controller, *args, **kwargs)
        self.title("Temporal Model")
        self.controller = controller

        # application window
        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky='nsew')
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
        self.bribers_spent = []
        self.results = ResultsStore(X_AXIS_OPTIONS, Y_AXIS_OPTIONS)
        self.briber_names = []
        self.g = None

    def clear_graph(self):
        self.bribers = []
        self.bribers_spent = []
        self.results = ResultsStore(X_AXIS_OPTIONS, Y_AXIS_OPTIONS)
        self.briber_names = []
        self.g = None

    def show_frame(self, page):
        self.frames[page].tkraise()

    def add_briber(self, b, *args):
        self.bribers.append(switch_briber(b, *args))
        self.bribers_spent.append(0)
        self.briber_names.append(f"Briber{len(self.bribers)}: {b}: u0={args[0]}")

    def add_graph(self, gtype, args, params):
        if not self.bribers:
            raise RuntimeError("No Bribers added to graph")

        if gtype == BarabasiAlbert.name:
            gen = FlatWeightedGraphGenerator(GraphGeneratorAlgo.BARABASI_ALBERT, *args)
        elif gtype == Composite.name:
            gen = FlatWeightedGraphGenerator(GraphGeneratorAlgo.COMPOSITE, *args)
        else:
            gen = FlatWeightedGraphGenerator(GraphGeneratorAlgo.WATTS_STROGATZ, *args)

        self.g = ThresholdGraph(
            tuple(self.bribers),
            generator=gen,
            non_voter_proportion=params[0],
            threshold=params[1],
            d=params[2],
            q=params[3],
            pay=params[4],
            apathy=params[5],
            learning_rate=params[6],
            true_averages=params[7],
            true_std_devs=params[8]
        )

        self.frames[GraphFrame.__name__].set_pos(spring_layout(nk2nx(self.g.get_graph())))

        self.frames[GraphFrame.__name__].add_briber_dropdown()
        self.frames[GraphFrame.__name__].draw_basic_graph(self.g)

    def update_results(self):

        self.results.add("Average Rating", [self.g.average_rating(briber_id=b) for b in range(0, len(self.bribers))])
        self.results.add("Total Utility", [b.get_resources() for b in self.bribers])
        self.results.add("Average Trust", self.g.average_trust())
        self.results.add("Utility Spent", [self.bribers_spent[b] for b in range(0, len(self.bribers))])
        self.results.add("Time", self.g.get_time_step())

    def plot_results(self, x_label, y_label):
        self.frames[ResultsFrame.__name__].plot_results(self.results, x_label, y_label)
        self.show_frame(ResultsFrame.__name__)

    def next_step(self):

        last_round_was_bribery = self.g.is_bribery_round()
        self.g.step()

        if last_round_was_bribery:
            for bribers, bribe in self.g.get_last_bribery_actions()[-1].get_bribes().items():
                self.bribers_spent[bribers] += sum(bribe.values())

        self.update_results()

        if last_round_was_bribery:
            info = "BRIBES\n"
            for bribers, bribe in self.g.get_last_bribery_actions()[-1].get_bribes().items():
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

        self.frames[GraphFrame.__name__].draw_basic_graph(self.g)
        self.frames[GraphFrame.__name__].set_info(info)

    @override
    def destroy(self):
        if self.controller is not None:
            self.controller.show_main()
        super().destroy()


if __name__ == '__main__':
    app = TemporalGUI(None)
    app.mainloop()
