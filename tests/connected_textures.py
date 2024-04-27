import pygame

pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("Connected Textures")

class Tile():
    size = 25
    border_size = 2  # Ширина границы

    def __init__(self, x, y):
        self.surface = pygame.Surface((Tile.size, Tile.size), pygame.SRCALPHA)  # Используем SRCALPHA для прозрачности
        self.surface.fill((0, 0, 0, 128))  # Задаем прозрачный цвет (0, 0, 0, 0)

        # Рисуем границу
        pygame.draw.rect(self.surface, (0, 0, 0), (0, 0, Tile.size, Tile.size), Tile.border_size)

        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = x, y

    def render(self):
        screen.blit(self.surface, self.rect)
        # pygame.draw.rect(self.surface, (0, 0, 0), self.rect, 15)

tiles = []

tile1 = Tile(100, 100)
tile2 = Tile(100 + Tile.size - Tile.border_size, 100)

tiles.append(tile1)
tiles.append(tile2)

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill((255, 255, 255))
    
    for tile in tiles:
        tile.render()
    
    pygame.display.flip()
    clock.tick(15)

pygame.quit()