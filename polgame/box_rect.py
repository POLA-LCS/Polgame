from pygame import Rect, Surface, font
from .types import *

BoxFormat = tuple[float, float, float, float, Color]

class Box(Rect):
    DEFAULT_COLOR: Color = (0, 127, 255)
    
    class Border:
        DEFAULT_COLOR = (0, 0, 0)
        def __init__(self, width: int = 0, color: Color = None, radius: int | tuple[int, ...] | None = None):
            self.width  = width
            self.color  = color if color is not None else Box.Border.DEFAULT_COLOR
            self.radius = radius

    def from_rect(rect: Rect):
        return Box(rect.left, rect.top, rect.width, rect.height)

    # Constructor
    def __init__(self, left: float = 0, top: float = 0, width: float = 0, height: float = 0, color: Color = None, center = False):
        super().__init__(left, top, width, height)
        if center:
            self.centerx, self.centery = left, top
        self.color = color if color is not None else Box.DEFAULT_COLOR
        self.border = Box.Border()

    @property
    def size(self):
        return self.width, self.height

    @size.setter
    def size(self, size: tuple[float, float]):
        self.width, self.height = size

    def set_color(self, new_color: Color):
        self.color = new_color
        return self

    def set_size(self, new_size: tuple[int, int]):
        self.size = new_size
        return self

    def get_surface(self):
        return Surface(self.size, masks=self.color)

    def __repr__(self):
        return f"Box({self.left}, {self.top}, {self.width}, {self.height}, {self.color})"

    def __str__(self):
        return self.__repr__()