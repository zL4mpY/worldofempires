import pygame

class TextManager:
    def render(self, surface, x, y, text, font, color, size):
        try:
            font = pygame.font.Font(font, size)
        except Exception:
            font = pygame.font.SysFont(font, size)
        
        text = font.render(text, True, color)
        rect = text.get_rect()
        rect.topleft = (x, y)
        surface.blit(text, (rect.x, rect.y))