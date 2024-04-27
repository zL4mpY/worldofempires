from engine.managers.textManager import TextManager

import engine
import pygame
import random

class City(engine.BaseObject):
    def __init__(self, game, scene, x, y, country, isCapital = False):
        super().__init__(game, scene, x, y)
        
        self.country = country

        self.name = self.game.lang['cityRenderMessage'] if isCapital == False else self.country.name

        # self.name = self.country.name if isCapital else game.lang['cityRenderMessage']
        
        self.color = self.country.color
        # self.text_color = self.color
        self.text_color = (255, 255, 255)
        self.size = self.scene.cell_size
        self.isCapital = isCapital
        self.textManager = self.game.textManager
        self.hp = 250
        self.max_hp = 250
        self.human_spawn_boost = 0
        self.regen_size = {'min': round(random.uniform(0.05, 2), 2), 'max': round(random.uniform(2, 10), 2)}
        
        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = x,y
    
    def set_screen(self, screen):
        super().set_screen(screen)
    
    def render(self):
        super().render()
        pygame.draw.rect(self.screen, self.color, (self.rect.x, self.rect.y, self.size, self.size))
        self.textManager.render(self.screen, self.rect.x, self.rect.y - 15, self.name, 'arialblack', self.text_color, 10, align='center')
    
    def act(self):
        if self.game.settingsManager.settings.get('auto_spawn').get('humans').get('enabled'):
            if random.uniform(0, 1) < (self.game.settingsManager.get('auto_spawn').get('humans').get('spawn_chance') + self.human_spawn_boost) / 12500:
                self.spawn_human()
                pass
        
        if self.country.states['in_war'] == False:
            if self.hp <= self.max_hp:
                self.hp += round(random.uniform(self.regen_size['min'], self.regen_size['max']), 2)

                if self.hp >= self.max_hp:
                    self.hp = self.max_hp

    
    def spawn_human(self):
        from .human import Human
        self.country.humans.append(Human(self.game, self.scene, self.x, self.y, self.country, self))
    
    def __repr__(self):
        return f'City of {self.country} at {self.x=} {self.y=}'