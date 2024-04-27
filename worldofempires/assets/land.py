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
        
        self.surface = pygame.Surface((self.scene.land_cell_size, self.scene.land_cell_size))
        self.surface.set_alpha(128)
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = x, y
        
    def render(self):
        self.game.screen.blit(self.surface, self.rect)
    
    def __repr__(self):
        return f'Land of {self.country} (x={self.x} y={self.y})'