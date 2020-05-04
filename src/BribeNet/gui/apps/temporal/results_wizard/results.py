class ResultsStore:
    """
    Class for storing results during runs, identified by keys, seperated to xs and ys
    """

    def __init__(self, xs, ys):
        self.xs = xs
        self.ys = ys
        self.data = {k: [] for k in (xs + ys)}

    def add(self, k, v):
        self.data[k].append(v)

    def get(self, k):
        return self.data[k]

    def get_x_options(self):
        return self.xs

    def get_y_options(self):
        return self.ys
