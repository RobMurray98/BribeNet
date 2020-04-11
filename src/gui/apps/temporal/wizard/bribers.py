import tkinter as tk

from gui.apps.temporal.briber_wizard.window import TemporalBriberWizardWindow
from helpers.override import override


class TemporalBribers(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.briber_wizard = None
        self.bribers_list = []

        bribers_title_label = tk.Label(self, text="Bribers")
        bribers_title_label.grid(row=1, column=1)

        self.bribers_listbox = tk.Listbox(self)
        self.bribers_listbox.grid(row=2, column=1, rowspan=3)

        self.add_briber_button = tk.Button(self, text="Add", command=self.open_briber_wizard)
        self.add_briber_button.grid(row=2, column=2)

        self.delete_briber_button = tk.Button(self, text="Delete", command=self.delete_selected_briber)
        self.delete_briber_button.grid(row=3, column=2)

    def open_briber_wizard(self):
        if self.briber_wizard is None:
            self.briber_wizard = TemporalBriberWizardWindow(self)
        else:
            self.briber_wizard.lift()

    def delete_selected_briber(self):
        cur_sel = self.bribers_listbox.curselection()
        if not cur_sel:
            return
        self.bribers_listbox.delete(cur_sel[0])
        del self.bribers_list[cur_sel[0]]

    def add_briber(self, strat_type, *args):
        self.bribers_list.append((strat_type, *args))
        self.bribers_listbox.insert(tk.END, strat_type)

    def get_all_bribers(self):
        return self.bribers_list

    @override
    def destroy(self):
        if self.briber_wizard is not None:
            self.briber_wizard.destroy()
        super().destroy()
