import pygame as pg
from .box_rect import *
from .image_surface import *
from .events_wrapper import *
from typing import Any

Entity = Box | Image | Surface
Entity_Pos = tuple[Entity, tuple[int, int]]
Drawable = Entity | Entity_Pos

class Game:
    DEFAULT_COLOR: Color = (18, 18, 18)
    def __init__(self, width: int, height: int, title: str = 'Polgame', background_color: Color = DEFAULT_COLOR, framerate: int = 60):
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
            def left_click(self):
                return self.pressed[0]

            @property
            def wheel_click(self):
                return self.pressed[1]

            @property
            def right_click(self):
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
        self.entities = list[Entity]()
        self.draw_list = list[Drawable]()

        # Events
        self.events = list[Event]()
        self.handlers = dict[EventCode, list[EventHandler]]()

        # Frames
        self.clock = pg.time.Clock()
        self.framerate = framerate
        self.frame = 1
        self.cycle = 1

        # Mouse
        self.mouse = Mouse()

        # Keyboard
        self.active_keys = set[str]()

    def throw(self, type: int, props: dict):
        self.events.append(Event(type, props))

    def catch(self, type: int, many: int):
        events = list[Event]()
        i = many
        for event in self.events[::-1]:
            if event.type == type:
                if many == 1:
                    return [event]

                if i == 0:
                    break

                events.append(event)
                i -= 1
        return events

    def expose(self, *objects: Entity):
        for o in objects:
            if not isinstance(o, Entity):
                raise TypeError(f'Object of type {type(o)} is not considered an Entity.')
            self.entities.append(o)
        if len(objects) == 1:
            return self.entities[-1]
        return objects

    def draw(self, *drawables: Drawable):
        self.draw_list.extend([*drawables])

    def close(self, _: Event | None = None):
        self.running = False

    def listen(self, type: int, callback: HandlerType, *args: Any):
        if not isinstance(callback, Callable):
            raise TypeError('Callback must be a callable object.')
        if type in NOT_IMPLEMENTED:
            raise NotImplementedError(f'Event with type ({type}: {EVENT_NAME[type]}) is not implemented yet.')
        self.handlers.setdefault(type, []).append(EventHandler(callback, *args))

    def load(self):
        if not self.running:
            return False

        # Mouse properties
        self.mouse.update()

        self.events = []
        for event in pg.event.get():
            # KEY DOWN
            if event.type == pg.KEYDOWN:
                event.dict['key'] = event.key
                self.active_keys.add(event.key)
                if event.unicode:
                    self.active_keys.add(event.unicode)
                    event.dict['code'] = event.unicode

            # KEY UP
            if event.type == pg.KEYUP:
                event.dict['key'] = event.unicode
                self.active_keys.remove(event.key)
                if event.unicode:
                    self.active_keys.remove(event.unicode)
                    event.dict['code'] = event.unicode

            self.throw(event.type, event.dict)

        # KEY HOLD
        for key in self.active_keys:
            self.throw(KEYHOLD, {'key': key})

        for box in self.entities:
            # HOVER, CLICK AND DRAG
            if box.collidepoint(self.mouse.position):
                # HOVER
                self.throw(HOVER_BOX, {'box': box, 'pos': self.mouse.position})
                # CLICK
                if any(self.mouse.pressed):
                    self.throw(CLICK_BOX, {'box': box, 'pos': self.mouse.position, 'click': self.mouse.pressed})
                    # DRAG
                    if self.mouse.relative != (0, 0):
                        self.throw(DRAG_BOX, {'box': box, 'pos': self.mouse.position, 'move': self.mouse.relative, 'click': self.mouse.pressed})
        return True

    def update(self):
        if not self.running:
            return False

        for event in self.events:
            for handle in self.handlers.get(event.type, []):
                handle.call(event)

        self.screen.fill(self.background_color)

        # Inner function
        def draw(object: Drawable):
            if isinstance(object, tuple):
                instance, topleft = object
                
                if isinstance(instance, Surface):
                    self.screen.blit(instance, topleft)
                    return
                
                copy = instance.copy()
                if isinstance(copy, Box):
                    copy.border = instance.border
                copy.top, copy.left = topleft
                draw(copy)

            elif isinstance(object, Image):
                self.screen.blit(object.get_surface(), object.box.topleft, object.box if object.mask else None)

            elif isinstance(object, Box):
                radius = [-1, -1, -1, -1]
                # If there's a radius
                if object.border.radius is not None:
                    if isinstance(object.border.radius, (int, float)):
                        radius = [int(object.border.radius)]*4
                        
                    elif isinstance(object.border.radius, tuple | list):
                        if len(object.border.radius) == 2:
                            radius[0] = radius[3] = object.border.radius[0]
                            radius[1] = radius[2] = object.border.radius[1]

                        elif len(object.border.radius) == 3:
                            radius[0] = object.border.radius[0]
                            radius[1], radius[2] = object.border.radius[1:]

                        elif len(object.border.radius) == 4:
                            radius = object.border.radius
                    else:
                        raise TypeError(f'Border of {object} is not a tuple or list.')

                    # IF BOX HAS BORDER
                    if object.border.width > 0:
                        border = object.border.width / 2
                        
                        pg.draw.rect(self.screen,
                            object.border.color,
                            (
                                object.left   - border,
                                object.top    - border,
                                object.width  + object.border.width,
                                object.height + object.border.width),
                            object.border.width, -1, *radius
                        )

                # FINAL DRAW
                pg.draw.rect(self.screen, object.color, object, 0, 0, *radius)
                
            elif isinstance(object, Surface):
                self.screen.blit(object, (0, 0))
                
            else:
                raise ValueError(f'Object of type {type(object)} is not a Drawable.')

        for box in self.draw_list:
            draw(box)

        self.draw_list = []

        pg.display.update()
        self.clock.tick(self.framerate)
        self.frame += 1
        if self.frame % self.framerate == 0:
            self.frame = 0
            self.cycle += 1
        return True

    def every(self, frames: int, cycles: int, id: EventCode | None = None):
        result = self.frame % frames == 0 and self.cycle % cycles == 0
        if result and id is not None:
            self.throw(UPDATE, {'id': id, 'frame': self.frame, 'cycle': self.cycle})
        return 

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