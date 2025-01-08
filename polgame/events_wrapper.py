from pygame import event, QUIT
from typing import Self

EventCode = int | str

class Event:
    def __init__(self, type: EventCode, dict: dict):
        self.type = type
        self.dict = dict
        
    def get(self, key: EventCode):
        return self.dict.get(key)
    
    def has(self, key: EventCode):
        return key in self.dict
                
    def __getitem__(self, key: EventCode):
        return self.dict[key]
        
    def __contains__(self, key: EventCode):
        return key in self.dict

    def __eq__(self, other: Self | EventCode):
        if isinstance(other, Event):
            return self.type == other.type and self.dict == other.dict
        if isinstance(other, EventCode):
            return self.type == other
        raise ValueError(f'Comparisson between Event and {type(other)} is not supported.')
        
    def __repr__(self):
        return f"Event({self.type}, {self.dict})"
        
HOVER_BOX   = event.custom_type()
UNHOVER_BOX = event.custom_type()
CLICK_BOX   = event.custom_type()
RELEASE_BOX = event.custom_type()
DRAG_BOX    = event.custom_type()
KEYHOLD     = event.custom_type()
CLOSE = QUIT

NOT_IMPLEMENTED: list[int] = [
    UNHOVER_BOX,
    RELEASE_BOX
]

EVENT_NAME: dict[int, str] = {
    HOVER_BOX: 'HOVER_BOX',
    UNHOVER_BOX: 'UNHOVER_BOX',
    CLICK_BOX: 'CLICK_BOX',
    RELEASE_BOX: 'RELEASE_BOX',
    DRAG_BOX: 'DRAG_BOX',
    KEYHOLD: 'KEYHOLD'
}