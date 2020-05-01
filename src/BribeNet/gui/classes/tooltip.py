import tkinter as tk


# noinspection PyUnusedLocal
class ToolTip(object):
    """
    Show a tooltip
    from https://stackoverflow.com/a/56749167/5539184
    """

    def __init__(self, widget, text):
        self.widget = widget
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.text = text

    def show_tip(self, *args):
        if self.tip_window is not None or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() + 27
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(tw, text=self.text, wraplength=400, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "10", "normal"))
        label.pack(ipadx=1)

    def hide_tip(self, *args):
        if self.tip_window is not None:
            self.tip_window.destroy()
            self.tip_window = None
