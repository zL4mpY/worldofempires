import pygame

class ImageManager:
    def render(self, surface, image, x, y, scale):
        width = image.get_width()
        height = image.get_height()
        image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        rect = image.get_rect
        rect.topleft = (x, y)

        surface.blit(image, (rect.x, rect.y))