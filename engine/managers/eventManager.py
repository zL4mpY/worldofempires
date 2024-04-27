import time
import pygame
from typing import Callable

keys = {
    '1': pygame.K_1,
    '2': pygame.K_2,
    '3': pygame.K_3,
    '4': pygame.K_4,
    '5': pygame.K_5,
    '6': pygame.K_6,
    '7': pygame.K_7,
    '8': pygame.K_8,
    '9': pygame.K_9,
    '0': pygame.K_0,
    'a': pygame.K_a,
    'b': pygame.K_b,
    'c': pygame.K_c,
    'd': pygame.K_d,
    'e': pygame.K_e,
    'f': pygame.K_f,
    'g': pygame.K_g,
    'h': pygame.K_h,
    'i': pygame.K_i,
    'j': pygame.K_j,
    'k': pygame.K_k,
    'l': pygame.K_l,
    'm': pygame.K_m,
    'n': pygame.K_n,
    'o': pygame.K_o,
    'p': pygame.K_p,
    'q': pygame.K_q,
    'r': pygame.K_r,
    's': pygame.K_s,
    't': pygame.K_t,
    'u': pygame.K_u,
    'v': pygame.K_v,
    'w': pygame.K_w,
    'x': pygame.K_x,
    'y': pygame.K_y,
    'z': pygame.K_z,
    'F1': pygame.K_F1,
    'F2': pygame.K_F2,
    'F3': pygame.K_F3,
    'F4': pygame.K_F4,
    'F5': pygame.K_F5,
    'F6': pygame.K_F6,
    'F7': pygame.K_F7,
    'F8': pygame.K_F8,
    'F9': pygame.K_F9,
    'F10': pygame.K_F10,
    'F11': pygame.K_F11,
    'F12': pygame.K_F12,
    'F13': pygame.K_F13,
    'F14': pygame.K_F14,
    'F15': pygame.K_F15
    }

def get_pygame_key(key):
    return keys[key]

class Event():
    """
    
        A basic event that can be used in event manager.
    
    """
    def __init__(self, action, time):
        self.action = action
        self.time = pygame.time.get_ticks() + time * 1000
    
    def run(self):
        self.action()
        del self

class KeyboardEvent():
    """
    
        This is a keyboard event.
    
    """
    def __init__(self, key: str, event: Callable):
        self.key = key
        self.event = event
    
    def run(self) -> None:
        """
        
            Runs the keyboard event.
        
        """
        self.event()

class EventManager():
    
    """
    
        This is an event manager. It can be used to create events that will be
        executed in some time or use useful time variables.
    
    """
    
    def __init__(self):
        self.game_start_time = None
        self.game_end_time = None
        self.scene_start_time = {}
        self._events = []
        self._keyboard_events = []
    
    def get_events(self) -> dict:
        return self._events
    
    def set_start_time(self, time: float | int) -> None:
        """
        
            Sets the start time of your program which can be used for something.
            In Lumix it is already executed at start by default.
        
        """
        self.start_time = time
    
    def get_start_time(self) -> float | int:
        """
        
            This method returns a start time of your program which can be used for something.
            In Lumix the start time is already set at start by default.
        
        """
        return self.start_time
        
    def create_event(self, event: Event | str) -> None:
        """
        
            Use it to create an event that will execute after any time you want.
            Event is a event you want to execute and time is a time after which your
            event will be executed (in seconds).
        
        """
        
        self._events.append(event)
    
    def remove_event(self, event: Event | str) -> None:
        """
        
            Use it to remove the event if it was executed or for any other reasons.
            Event can be Event type or a string (depends on the type of its key value).
        
        """
        self._events.remove(event)
    
    def add_keyboard_event(self, key: str, event: Callable):
        event = KeyboardEvent(key=key, event=event)
        self._keyboard_events.append(event)
    
    def remove_keyboard_event(self, event: int | Callable):
        if isinstance(event, int):
            event = self._keyboard_events.pop(event)
            return event
        
        event = self._keyboard_events.remove(event)
        return event

    def get_keyboard_events(self) -> list:
        return self._keyboard_events

    def run_events(self):
        for event in self._events:
            time = pygame.time.get_ticks()
            if event.time <= time:
                event.run()
                self._events.remove(event)