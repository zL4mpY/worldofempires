import pygame

class ImageManager:
    def __init__(self, game):
        self.game = game
    
    def get_surface(self, image, x, y, scale, align="topleft"):
        width = image.get_width()
        height = image.get_height()
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        rect = image.get_rect()
        
        devSurface = pygame.Surface((rect.width, rect.height))
        devSurface.set_alpha(64)
        devSurface.fill((0, 0, 255))
        devRect = pygame.Rect(x, y, rect.width, rect.height)
        
        if align == "tl":
            align = "topleft"
            
        elif align == "tr":
            align = "topright"
            
        elif align == "br":
            align = "bottomright"
            
        elif align == "bl":
            align = "bottomleft"
            
        elif align == "l":
            align = "left"
            
        elif align == "r":
            align = "right"
            
        elif align == "t":
            align = "top"
            
        elif align == "b":
            align = "bottom"
            
        elif align == "c":
            align = "center"
        
        if align in ['left', 'right']:
            setattr(rect, align, x)
            setattr(devRect, align, x)
        elif align in ['top, bottom']:
            setattr(rect, align, y)
            setattr(devRect, align, y)
        elif align in ['center', 'topleft', 'topright', 'bottomleft', 'bottomright']:
            setattr(rect, align, (x, y))
            setattr(devRect, align, (x, y))
        
        return ((rect.width, rect.height))
    
    def render(self, surface, image, x, y, scale, align="topleft"):
        width = image.get_width()
        height = image.get_height()
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        rect = image.get_rect()
        rect.topleft = (x, y)
        
        devSurface = pygame.Surface((rect.width, rect.height))
        devSurface.set_alpha(64)
        devSurface.fill((0, 0, 255))
        devRect = pygame.Rect(x, y, rect.width, rect.height)
        devRect.topleft = (x, y)
        
        if align == "tl":
            align = "topleft"
            
        elif align == "tr":
            align = "topright"
            
        elif align == "br":
            align = "bottomright"
            
        elif align == "bl":
            align = "bottomleft"
            
        elif align == "l":
            align = "left"
            
        elif align == "r":
            align = "right"
            
        elif align == "t":
            align = "top"
            
        elif align == "b":
            align = "bottom"
            
        elif align == "c":
            align = "center"
        
        if align in ['left', 'right']:
            setattr(rect, align, x)
            setattr(devRect, align, x)
        elif align in ['top, bottom']:
            setattr(rect, align, y)
            setattr(devRect, align, y)
        elif align in ['center', 'topleft', 'topright', 'bottomleft', 'bottomright']:
            setattr(rect, align, (x, y))
            setattr(devRect, align, (x, y))

        surface.blit(image, (rect.x, rect.y))
        
        if self.game.is_devmode:
            surface.blit(devSurface, (devRect.x, devRect.y))