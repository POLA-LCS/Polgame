from pygame import Rect, Surface
from .types import *
from typing import Self

class Box(Rect):
    # BORDER INNER CLASS
    # TODO: Make the border to be another Box and add Box.radius
    class Border:
        DEFAULT_COLOR = (0, 0, 0)
        def __init__(self, width: int = 0, color: Color = None, radius: int | tuple[int, ...] | None = None):
            self.width  = width
            self.color  = color if color is not None else Box.Border.DEFAULT_COLOR
            self.radius = radius

    # BOX CLASS
    DEFAULT_COLOR: Color = (0, 127, 255)
    def __init__(self, left: float = 0, top: float = 0, width: float = 0, height: float = 0, color: Color = None, center = False):
        super().__init__(left, top, width, height)
        if center:
            self.centerx, self.centery = left, top
        self.color = color if color is not None else Box.DEFAULT_COLOR
        self.border = Box.Border()

    def set_color(self, new_color: Color):
        self.color = new_color

    def move_to(self, left: int, top: int):
        self.left = left
        self.top = top

    @property
    def size(self):
        return (self.width, self.height)

    @size.setter
    def size(self, size: tuple[float, float]):
        self.width, self.height = size

    def get_format(self):
        return (self.left, self.top, self.width, self.height)

    def copy(self, center = False):
        return Box(self.left, self.top, self.width, self.height, self.color, center)

    def change(self, attr: str, value) -> Self:
        if not attr in self.__dict__:
            raise AttributeError(f'Box has no attribute {attr}')
        self.__dict__[attr] = value
        return self

    def __repr__(self):
        return f"Box({self.left}, {self.top}, {self.width}, {self.height}, {self.color})"

    def __str__(self):
        return self.__repr__()