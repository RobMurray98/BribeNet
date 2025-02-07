import tkinter as tk

from BribeNet.bribery.static.oneMoveInfluentialNodeBriber import OneMoveInfluentialNodeBriber
from BribeNet.bribery.static.oneMoveRandomBriber import OneMoveRandomBriber
from BribeNet.graph.generation import GraphGeneratorAlgo
from BribeNet.graph.generation.flatWeightGenerator import FlatWeightedGraphGenerator
from BribeNet.graph.static.ratingGraph import StaticRatingGraph
from BribeNet.gui.apps.static.graph import GraphFrame
from BribeNet.gui.apps.static.result import ResultsFrame
from BribeNet.gui.apps.static.wizard.wizard import WizardFrame
from BribeNet.helpers.override import override

FRAMES_CLASSES = [WizardFrame,
                  GraphFrame,
                  ResultsFrame]
FRAMES_DICT = {i: c.__class__.__name__ for (i, c) in enumerate(FRAMES_CLASSES)}


def switch_briber(argument):
    switcher = {
        "r": lambda: OneMoveRandomBriber(10),
        "i": lambda: OneMoveInfluentialNodeBriber(10)
    }
    return switcher.get(argument)


class StaticGUI(tk.Toplevel):
    """
    Window for the static wizard and running environment
    """

    def __init__(self, controller, *args, **kwargs):
        super().__init__(controller, *args, **kwargs)
        self.title("Static Model")
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in FRAMES_CLASSES:
            page_name = F.__name__
            frame = F(parent=self, controller=controller)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WizardFrame")

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def generate_graph(self, gtype, btype):
        briber = switch_briber(btype)()

        ba_gen = FlatWeightedGraphGenerator(GraphGeneratorAlgo.BARABASI_ALBERT, 5, 30, 0, True)
        comp_gen = FlatWeightedGraphGenerator(GraphGeneratorAlgo.COMPOSITE, 50, 5, 2, 0.1, 3, 0.05)

        if gtype == "ba":
            rg = StaticRatingGraph(briber, generator=ba_gen)
        elif gtype == "cg":
            rg = StaticRatingGraph(briber, generator=comp_gen)
        else:
            rg = StaticRatingGraph(briber)
        self.frames["GraphFrame"].set_graph(rg, briber)

    def plot_results(self, results):
        self.frames["ResultsFrame"].plot_results(results)

    @override
    def destroy(self):
        if self.controller is not None:
            self.controller.show_main()
        super().destroy()


if __name__ == '__main__':
    app = StaticGUI(None)
    app.mainloop()
