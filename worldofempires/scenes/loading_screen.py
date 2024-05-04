from engine.managers.sceneManager import Scene
from engine.managers.eventManager import Event

from engine.classes.label import Label
from engine import get_base_dir

import pygame
import time

class LoadingScene(Scene):
    def __init__(self, game, name, custom_action=None):
        super().__init__(game, name)
        
        self.objects = []
        self.custom_action = custom_action
        self.eventManager = self.game.eventManager
        
        self.draw_objects()
    
    def draw_objects(self):
        # labels
        
        # loading_lbl
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width - 6, y=self.game.height - 6,
                      text=f"{self.game.lang.get('loading_label')}",
                      font="Arial",
                      fontsize=20,
                      color=(255, 255, 255),
                      side="rb",
                      align="right")

        self.objects.append(label)
        
    
    def start(self):
        def custom_action():
            self.custom_action()
            self.custom_action = None
            
        self.eventManager.create_event(Event(custom_action, 1))
    
    def update(self):
        self.eventManager.run_events()
    
    def handle_event(self, event):
        pass
    
    def render(self):
        self.screen.fill((0, 0, 0))
        
        for object in self.objects:
            object.render()