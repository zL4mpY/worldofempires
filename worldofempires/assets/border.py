import pygame

class Border:
    def __init__(self, game, scene, country, x1, y1, x2, y2):
        self.game = game
        self.scene = scene
        
        self.country = country
        self.color = self.country.territory_color
        self.border_thickness = 2
        
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.size = (x2 - x1, y2 - y1)
        
        self.surface = self.create_border_surface(*self.size)
        
        self.neighbors = []
    
    def create_border_surface(self, width, height):
        border_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        border_surface.fill((0, 0, 0, 0))  # Transparent center
        pygame.draw.rect(border_surface, self.color, pygame.Rect(self.border_thickness, self.border_thickness, width - self.border_thickness * 2, height - self.border_thickness * 2), 0, self.border_thickness)
        return border_surface

    def connect(self, other_border):
        if self.can_connect(other_border):
            self.neighbors.append(other_border)
            other_border.neighbors.append(self)

    def can_connect(self, other_border):
        if self.neighbors:
            return False

        dx, dy = self.x2 - self.x1, self.y2 - self.y1
        ox, oy = other_border.x2 - other_border.x1, other_border.y2 - other_border.y1

        if abs(dx) == abs(oy) and abs(ox) == abs(dy):
            if (dx * oy < 0 and dy * ox > 0) or (dx * oy > 0 and dy * ox < 0):
                return True

        return False
        
    def render(self):
        pygame.draw.rect(self.surface, self.color, pygame.Rect(self.border_thickness, self.border_thickness, self.surface.get_size()[0] - self.border_thickness * 2, self.surface.get_size()[1] - self.border_thickness * 2), self.border_thickness)