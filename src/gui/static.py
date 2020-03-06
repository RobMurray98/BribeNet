import tkinter as tk

import networkit as nk

from bribery.static.oneMoveInfluentialNodeBriber import OneMoveInfluentialNodeBriber
from bribery.static.oneMoveRandomBriber import OneMoveRandomBriber
from graph.static.ratingGraph import StaticRatingGraph
from graph.generation.algo.compositeGenerator import CompositeGenerator

from gui.frames.static.wizard import WizardFrame
from gui.frames.static.graph import GraphFrame
from gui.frames.static.result import ResultsFrame

from helpers.override import override


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


class StaticGUI(tk.Tk):
    def __init__(self, controller, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in [WizardFrame, GraphFrame, ResultsFrame]:
            page_name = F.__name__
            frame = F(parent=self, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WizardFrame")

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()

    def generate_graph(self, gtype, btype):
        briber = switch_briber(btype)()

        ba_gen = nk.generators.BarabasiAlbertGenerator(5, 30, 0, True)
        comp_gen = CompositeGenerator(50, 5, 2, 0.1, 3, 0.05)

        print(gtype)

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
