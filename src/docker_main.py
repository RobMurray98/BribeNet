from gui.main import GUI
from sys import exit

"""
Due to a bug where app.mainloop() will not exit on closing of the root Tk instance if a Toplevel was at any stage
instantiated, we use sys.exit(0) to 'hard exit' such that the Docker container does not hang after closing.
"""


def hard_exit(tk_app):
    tk_app.destroy()
    exit(0)


if __name__ == "__main__":
    app = GUI()
    app.protocol("WM_DELETE_WINDOW", lambda: hard_exit(app))
    app.mainloop()
