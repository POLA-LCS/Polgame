from pygame import Rect
from .types import *

class Box(Rect):
    class Border:
        def __init__(self, width: int = 0, color: Color = (0, 0, 0), radius: int | tuple[int, ...] | None = None):
            self.width  = width
            self.color  = color
            self.radius = radius

    DEFAULT_COLOR: Color = (0, 127, 255)

    def __init__(self, left: float = 0, top: float = 0, width: float = 0, height: float = 0, color: Color = DEFAULT_COLOR):
        super().__init__(left, top, width, height)
        self.color: Color = color
        self.border = Box.Border()

    @property
    def size(self):
        return self.width, self.height

    @size.setter
    def size(self, size: tuple[float, float]):
        self.width, self.height = size

    def __repr__(self):
        return f"Box({self.left}, {self.top}, {self.width}, {self.height}, {self.color})"

    def __str__(self):
        return self.__repr__()