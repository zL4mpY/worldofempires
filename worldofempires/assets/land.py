import engine
import pygame

class Land():
    def __init__(self, game, scene, x, y, country):
        self.game = game
        self.scene = scene
        self.screen = self.game.screen
        
        self.country = country
        self.color = country.territory_color
        self.size = self.scene.land_cell_size
        
        self.surface = pygame.Surface((self.scene.land_cell_size, self.scene.land_cell_size), flags=pygame.SRCALPHA)
        self.surface.set_alpha(128)
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = x, y
        self.camerarect = self.surface.get_rect()
        self.camerarect.x, self.camerarect.y = x, y
        
    def render(self, add_x=0, add_y=0):
        if add_x != 0 or add_y != 0:
            self.surface.fill((0, 0, 0))
            self.surface.set_alpha(255)
            self.screen.blit(self.surface, self.rect, special_flags=(pygame.BLEND_RGBA_ADD))
            
            self.surface.set_alpha(128)
            self.surface.fill(self.color)
        
        self.screen.blit(self.surface, (self.rect.x + add_x, self.rect.y + add_y))
        self.camerarect.x = self.rect.x + add_x
        self.camerarect.y = self.rect.y + add_y
    
    def __repr__(self):
        return f'Land of {self.country} (x={self.x} y={self.y})'