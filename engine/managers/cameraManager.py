import pygame

class CameraManager():
    def __init__(self, game, scene, x, y, width, height, align='c'):
        self.width, self.height = width, height
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(x, y, self.width, self.height)
        
        from engine import get_align
        self.align = get_align(align)
        
        from engine import set_align
        set_align(self.align, self.rect, x, y)
    
    def set_position(self, x, y, align):
        from engine import get_align
        self.align = get_align(align)
        
        from engine import set_align
        set_align(self.align, self.rect, x, y)
    
    def get_position(self) -> tuple:
        return self.rect.center
        
        
        
        