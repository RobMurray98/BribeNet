import abc
from typing import Optional

from graph.ratingMethod import RatingMethod
from gui.classes.param_list_frame import ParamListFrame


class RatingMethodFrame(ParamListFrame, abc.ABC):
    enum_value: Optional[RatingMethod] = None

    def __init__(self, parent):
        super().__init__(parent)
