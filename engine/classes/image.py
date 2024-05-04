from .. import get_align, set_align
import pygame

class Image():
    def __init__(self,
                 game,
                 scene,
                 x, y,
                 image,
                 scale_width=1, scale_height=1,
                 align='topleft'):
    
        self.game, self.scene = game, scene
        
        self.screen = self.scene.screen
        
        self.surface = image if isinstance(image, pygame.Surface) else pygame.image.load(image, "")
        self.width = self.surface.get_width()
        self.height = self.surface.get_height()
        
        self.surface = pygame.transform.scale(self.surface, (int(self.width * scale_width), int(self.height * scale_height)))
        self.rect = self.surface.get_rect()
        self.align = get_align(align)
        
        self.rect.x, self.rect.y = set_align(self.align, self.rect, x, y)
        
        self.hitboxSurface = pygame.Surface((self.rect.width, self.rect.height))
        self.hitboxSurface.set_alpha(64)
        self.hitboxSurface.fill((0, 0, 255))
        
        self.hitboxRect = pygame.Rect(x, y, self.rect.width, self.rect.height)
        self.hitboxRect.x, self.hitboxRect.y = set_align(self.align, self.hitboxRect, x, y)
    
    def update(self):
        pass
    
    def handle_event(self, event):
        pass
    
    def render(self):
        self.screen.blit(self.surface, (self.rect.x, self.rect.y))
        
        if self.game.is_devmode:
            self.screen.blit(self.hitboxSurface, (self.hitboxRect.x, self.hitboxRect.y))
        
        
            