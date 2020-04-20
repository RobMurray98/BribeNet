import tkinter as tk

from gui.apps.temporal.briber_wizard.frame import TemporalBriberWizardFrame
from helpers.override import override


class TemporalBriberWizardWindow(tk.Toplevel):
    """
    Window for pop-up wizard for adding a temporal briber
    """

    def __init__(self, controller):
        super().__init__(controller)
        self.title("Briber Wizard")
        self.controller = controller
        self.frame = TemporalBriberWizardFrame(self)
        self.frame.pack(pady=10, padx=10)

    @override
    def destroy(self):
        self.controller.briber_wizard = None
        super().destroy()
