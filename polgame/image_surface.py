from .box_rect import Box, Surface
from pygame.image import load
from pygame import transform

class Image:
    def __init__(self, left: int, top: int, width: int, height: int, source: str):
        self.box = Box(left, top, width, height)
        self.image = load('assets/' + source)
        self.size = self.box.size
        self.source = source
        self.xoffset = 0
        self.yoffset = 0
        self.mask = False
        
    @property
    def size(self):
        return self.width, self.height
    
    @size.setter
    def size(self, new_size: tuple[int, int]):
        self.box.size = new_size
        self.image = transform.smoothscale(self.image, new_size)
        
    @property
    def width(self):
        return self.box.width
    
    @width.setter
    def width(self, new_width: int):
        self.size = (new_width, self.height)
        
    @property
    def height(self):
        return self.box.height
    
    @height.setter
    def height(self, new_height: int):
        self.size = (self.width, new_height)
        
    def get_surface(self):
        frame = Surface(self.size)
        frame.blit(self.image, self.offset, self.box if self.mask else None)
        return frame
        
    @property
    def offset(self):
        return (self.xoffset, self.yoffset)

    @offset.setter
    def offset(self, new_offset: tuple[int, int]):
        self.xoffset, self.yoffset = new_offset
        
    def __repr__(self):
        return f'Image({self.box.left}, {self.box.top}, {self.width}, {self.height}, {self.source})'