from engine.managers.textManager import TextManager
from .place import Place

import random
import pygame

class Battle:
    def __init__(self, game, scene, war, city):
        self.game = game
        self.scene = scene
        
        self.war = war
        self.participants = self.war.participants
        
        self.city = city
        self.country = city.country
        self.place = city
        self.size = 1

        self.render_message = self.game.lang['battleRenderMessage']
        self.render_text_color = self.city.country.color
        
        self.textRenderer = self.game.textManager
    
    def get_place(self):
        x = random.randint(self.city.x - random.randrange(0, 20, 5), self.city.x + random.randrange(0, 20, 5))
        y = random.randint(self.city.y - random.randrange(0, 20, 5), self.city.y + random.randrange(0, 20, 5))

        self.place = Place(x, y)

    def end(self):
        self.war.battles.remove(self)        
        del self

    def render(self):
        self.textRenderer.render(self.game.screen, self.place.x + 5, self.place.y - 5, self.render_message, 'arialblack', self.render_text_color, 9)
    
    def __repr__(self):
        return f'Battle of {", ".join([participant.name for participant in self.participants])}'