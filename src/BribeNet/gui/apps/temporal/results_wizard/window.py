import tkinter as tk

from BribeNet.gui.apps.temporal.results_wizard.frame import TemporalResultsWizardFrame


class TemporalResultsWizardWindow(tk.Toplevel):
    """
    Window for pop-up wizard for selecting results displayed
    """

    def __init__(self, controller, results):
        super().__init__(controller)
        self.title("Results Wizard")
        self.controller = controller
        self.frame = TemporalResultsWizardFrame(self, results)
        self.frame.pack(pady=10, padx=10)
