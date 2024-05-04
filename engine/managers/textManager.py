import pygame

class TextManager:
    def __init__(self, game):
        self.game = game
        self.game.loggingManager.log(f'TextManager initialized!', 'INFO')
        
    def render(self, surface, x, y, text, font, color, size, side='none', align='none'):
        try:
            font = pygame.font.Font(font, size)
        except Exception:
            font = pygame.font.SysFont(font, size)
        
        text = font.render(text, True, color)
        rect = text.get_rect()
        rect.center = (x, y)
        
        devSurface = pygame.Surface((rect.width, rect.height))
        devSurface.set_alpha(64)
        devSurface.fill((0, 0, 255))
        devRect = pygame.Rect(x, y, rect.width, rect.height)
        
        if align in ['left', 'l']:
            rect.left = x
            devRect.left = x
        elif align in ['center', 'c']:
            rect.center = (x, y)
            devRect.center = (x, y)
        elif align in ['right', 'r']:
            rect.right = x
            devRect.right = x
        
        match side:
            case 'lb':
                rect.bottom = y
                devRect.bottom = y
            
            case 'lt':
                rect.top = y
                devRect.top = y
            
            case 'rb':
                rect.bottom = y
                devRect.bottom = y
            
            case 'rt':
                rect.top = y
                devRect.top = y
            
            case 'cb':
                rect.center = (x, y)
                rect.bottom = y
                devRect.center = (x, y)
                devRect.bottom = y
            
            case 'ct':
                rect.center = (x, y)
                rect.top = y
                devRect.center = (x, y)
                devRect.top = y
            
        surface.blit(text, (rect.x, rect.y))
        
        if self.game.is_devmode:
            surface.blit(devSurface, (devRect.x, devRect.y))