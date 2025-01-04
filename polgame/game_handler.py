import pygame as pg
from .box_rect import *
from .events_wrapper import *

class Game:
    
    DEFAULT_COLOR: Color = (18, 18, 18)
    
    def __init__(self, title: str, width: int, height: int, background_color: Color = DEFAULT_COLOR, framerate: int = 60):
        class Mouse:
            def __init__(self):
                self.pressed  = tuple[bool, bool, bool]()
                self.relative = tuple[int, int]()
                self.position = tuple[int, int]()
            
            def update(self):
                self.pressed  = pg.mouse.get_pressed()
                self.relative = pg.mouse.get_rel()
                self.position = pg.mouse.get_pos()
            
            @property
            def left(self):
                return self.pressed[0]
            
            @property
            def middle(self):
                return self.pressed[1]

            @property
            def right(self):
                return self.pressed[2]
            
            @property
            def x(self):
                return self.position[0]
            
            @property
            def y(self):
                return self.position[1]
            
            @property
            def xrel(self):
                return self.relative[0]
            
            @property
            def yrel(self):
                return self.relative[1]
        # Pygame
        pg.init()
        self.screen = pg.display.set_mode((width, height))
        pg.display.set_caption(title)

        self._title = title
        self.background_color = background_color
        
        self.running = True

        # Boxes
        self.boxes: list[Box] = []
        self.draw_list: list[Box] = []

        # Events
        self.events: list[Event] = []
        self.event_listeners: dict[int, list[tuple[callable, tuple]]] = {}
        self.clock = pg.time.Clock()
        self.framerate = framerate

        # Mouse
        self.mouse = Mouse()
        
        # Keyboard
        self.active_keys = set[str]()
        
    def load(self, *boxes: Box):
        self.boxes.extend([*boxes])
        if len(boxes) == 1:
            return boxes[0]
        return boxes
        
    def draw(self, *boxes: Box):
        self.draw_list.extend([*boxes])
    
    def close(self):
        self.running = False
        
    def listen(self, type: int, callback: callable, *args):
        self.event_listeners.setdefault(type, []).append((callback, args))
        
    def listen_events(self):
        if not self.running:
            return
        
        # Mouse properties
        self.mouse.update()
        
        self.events = []
        for event in pg.event.get():
            # KEY DOWN
            if event.type == pg.KEYDOWN:
                self.active_keys.add(event.unicode)

            # KEY UP
            if event.type == pg.KEYUP:
                if event.unicode in self.active_keys:
                    self.active_keys.remove(event.unicode)
            
            self.events.append(Event(event.type, event.dict))            
            
            # KEY HOLD
            for key in self.active_keys:
                self.events.append(Event(KEYHOLD, {'key': key}))
            
        for box in self.boxes:
            # HOVER, CLICK AND DRAG
            if box.collidepoint(self.mouse.position):
                # HOVER
                self.events.append(Event(HOVER_BOX, {'box': box, 'pos': self.mouse.position}))
                # CLICK
                if any(self.mouse.pressed):
                    self.events.append(Event(CLICK_BOX, {'box': box, 'pos': self.mouse.position, 'click': self.mouse.pressed}))
                    # DRAG
                    if self.mouse.relative != (0, 0):
                        self.events.append(Event(DRAG_BOX, {'box': box, 'pos': self.mouse.position, 'move': self.mouse.relative, 'click': self.mouse.pressed}))
        
    def update(self):
        if not self.running:
            return
        
        for event in self.events:
            for call_args in self.event_listeners.get(event.type, []):
                call, args = call_args
                call(event, *args)
        
        self.screen.fill(self.background_color)
        
        for box in self.draw_list:
            radius = [-1, -1, -1, -1]
            if box.border.radius is not None:
                if isinstance(box.border.radius, (int, float)):
                    radius = [int(box.border.radius)]*4
                elif isinstance(box.border.radius, tuple):
                    if len(box.border.radius) == 2:
                        radius[0] = radius[3] = box.border.radius[0]
                        radius[1] = radius[2] = box.border.radius[1]
                    elif len(box.border.radius) == 3:
                        radius[0] = box.border.radius[0]
                        radius[1], radius[2] = box.border.radius[1:]
                    elif len(box.border.radius) == 4:
                        radius = box.border.radius
            if box.border.width > 0:
                border = box.border.width / 2
                pg.draw.rect(self.screen, box.border.color, (box.left - border, box.top - border, box.width + box.border.width, box.height + box.border.width), box.border.width, -1, *radius)
            pg.draw.rect(self.screen, box.color, box, 0, 0, *radius)
        self.draw_list = []
        
        pg.display.update()
        self.clock.tick(self.framerate)
        
        
    @property
    def title(self) -> str:
        return self._title
    
    @title.setter
    def title(self, title: str):
        self._title = title
        pg.display.set_caption(title)
        
    def set_title(self, new_title: str):
        self.title = new_title
        
    @property
    def width(self):
        return self.screen.get_width()
    
    @width.setter
    def width(self, width: int):
        self.screen = pg.display.set_mode((width, self.height))
        
    @property
    def height(self):
        return self.screen.get_height()
    
    @height.setter
    def height(self, height: int):
        self.screen = pg.display.set_mode((self.width, height))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print(f"[EXCEPTION]: {exc_type} -> {exc_value}")
        if traceback:
            print(f"[Traceback]: {traceback}")
        pg.quit()