from PIL.Image import fromarray
import pygame
import numpy
import noise

layers = numpy.array(object=[
    ["water1", (22, 156, 233), -10],
    ["water2", (45, 166, 235), -5],
    ["water3", (68, 176, 238), 0],
    ["sand", (244, 218, 138), 3],
    ["land0", (181, 202, 116), 6],
    ["land1", (116, 186, 94), 25],
    ["land2", (80, 143, 61), 35],
    ["land3", (50, 89, 38), 42],
    ["mountain1", (58, 29, 19), 46],
    ["mountain2", (92, 61, 61), 52],
    ["mountain_snow", (245, 240, 240), 255]
    ], dtype="object")

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

class Terrain():
    def __init__(self, game, scene, x, y, image, landscape, width, height):
        self.game = game
        self.scene = scene
        self.screen = self.game.screen
        
        self.image = image
        self.landscape = landscape
        self.rect = self.screen.get_rect()
        self.rect.topleft = (x, y)
        self.width, self.height = width, height
    
    def render(self):
        # self.screen.blit(self.landscape, self.rect)
        self.screen.blit(self.landscape, self.rect)
    
    def get_at(self, coordinates: tuple):
        if coordinates[0] > self.width or coordinates[0] < 0:
            return None
        
        if coordinates[1] > self.height or coordinates[0] < 0:
            return None
        
        return self.landscape.get_at(coordinates)

class TerrainGenerator:
    def __init__(self, game, scene):
        self.game = game
        self.scene = scene

    def generate(self, scale, shape, octaves, persistence, lacunarity, seed=False):
        shape = (shape[0] + 1, shape[1] + 1)
        
        scale = shape[1] * (scale / 100)
        persistence /= 100
        lacunarity /= 10
        world = numpy.zeros(shape)
        
        if seed == False or seed <= 0: seed = numpy.random.randint(1,100)
        for i in range(shape[0]):
            for j in range(shape[1] ):
                world[i][j] = noise.pnoise2(i / scale, j / scale,
                                            octaves=octaves,
                                            persistence=persistence,
                                            lacunarity=lacunarity,
                                            base=seed)
        return ((world + 1) * 128).astype(numpy.uint8)

    def assign_colors(self, layers, noise_array, sea_level):
        altitudes = (layers[:, 2] + sea_level).astype(int)
        colors = numpy.array([numpy.array([*color], dtype=numpy.uint8) for color in layers[:, 1]])
        color_indices = numpy.digitize(noise_array, altitudes)
        color_array = numpy.array([colors[ind] for ind in color_indices])
        return color_array

    def noise_array_to_image(self,noise_world):
        return fromarray(noise_world, mode="L")

    def color_array_to_image(self,color_world):
        return fromarray(color_world, mode="RGB")