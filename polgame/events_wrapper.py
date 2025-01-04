from pygame import event

class Event:
    def __init__(self, type: int | str, dict: dict):
        self.type = type
        self.dict = dict
        
    def __repr__(self):
        return f"Event({self.type}, {self.dict})"
        
    def __getitem__(self, key: str):
        return self.dict[key]
        
    def get(self, key: str):
        return self.dict.get(key)

    def __eq__(self, other):
        if isinstance(other, Event):
            return self.type == other.type and self.dict == other.dict
        if isinstance(other, int):
            return self.type == other
        if isinstance(other, str):
            return self.type == other
        
HOVER_BOX   = event.custom_type()
UNHOVER_BOX = event.custom_type()
CLICK_BOX   = event.custom_type()
RELEASE_BOX = event.custom_type()
DRAG_BOX    = event.custom_type()
KEYHOLD     = event.custom_type()