import pygame
import noise
from PIL.Image import fromarray
import numpy
import random
from tkinter.filedialog import asksaveasfilename

# Initialize pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
clock = pygame.time.Clock()
pygame.display.set_caption("Landscape Generator")

hard_to_walk = [(50, 89, 38), (80, 143, 61), (22, 156, 233), (45, 166, 235)]

class Human:
    def __init__(self, screen, terrain, pos):
        self.screen = screen
        self.terrain = terrain
        self.image = pygame.Surface((5, 5))  # Create a 2x2 pixel image
        self.image.fill((0, 0, 0))  # Set the color to red
        self.rect = self.image.get_rect()  # Get the rectangle for collision detection 
        self.rect.x, self.rect.y = pos
        self.speed = 2  # Set the initial speed
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def update(self):
        terrain_color = self.terrain.get_at((self.rect.x, self.rect.y))
        if terrain_color in hard_to_walk:
            self.speed = 1
        else:
            self.speed = 2

        direction = random.choice(self.directions)
        new_x, new_y = direction[0] * self.speed, direction[1] * self.speed
        new_pos = self.rect.move(new_x, new_y)  # Calculate the new position
        if self.can_move(new_pos):  # Check if the new position is valid
            self.rect = new_pos  # Update the position

    def can_move(self, pos):
        if pos.x < 0 or pos.x + self.rect.width > self.screen.get_width():
            return False  # Check if the position is outside the screen
        if pos.y < 0 or pos.y + self.rect.height > self.screen.get_height():
            return False  # Check if the position is outside the screen
        terrain_color = self.terrain.get_at((pos.x, pos.y))  # Get the terrain color at the new position
        if terrain_color == (68, 176, 238):
            return False  # Check if the new position is on water
        if terrain_color == (58, 29, 19) or terrain_color == (92, 61, 61) or terrain_color == (245, 240, 240):
            return False # Check if the new position is on mountains
        
        return True

    def render(self):
        self.screen.blit(self.image, self.rect)

    
class Generator:
    def __init__(self):
        pass

    def get_random_noise(self, scale, shape, octaves, persistence, lacunarity, seed=False):
        scale = shape[1] * (scale / 100)
        persistence /= 100
        lacunarity /= 10
        world = numpy.zeros(shape)
        if seed == False or seed <= 0: seed = numpy.random.randint(1,100)
        for i in range(shape[0]):
            for j in range(shape[1]):
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

# Update the display
pygame.display.flip()

font = pygame.font.SysFont('Arial', 16)

generator = Generator()
events = ["start"]
humans = []

class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.is_hidden = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
    
    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    self.onclickFunction()
                elif not self.alreadyPressed:
                    self.onclickFunction()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
        
        if not self.is_hidden:
            self.buttonSurface.blit(self.buttonSurf, [
                self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
            ])
            screen.blit(self.buttonSurface, self.buttonRect)

def save(image):
    dir = asksaveasfilename(
            title="Save your terrain"
        )
    if dir:
        image.save(dir+".png")

# Generate the landscape
octaves = 6
seed = 0 # [0, 0, 100]
sea_level = 125 # [120, 1, 200]
scale = 50 # [45, 1, 100]
persistence = 55 # [55, 1, 100]
lacunarity = 20 # [20, 1, 100]

def pilImageToSurface(pilImage):
    return pygame.image.fromstring(
        pilImage.tobytes(), pilImage.size, pilImage.mode).convert()

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

noise_array = None
color_array = None
image = None
landscape = None

def generate():
    global noise_array, color_array, image, landscape
    
    noise_array = generator.get_random_noise(scale=scale,
                                       shape=(HEIGHT, WIDTH),
                                       octaves=octaves,
                                       persistence=persistence,
                                       lacunarity=lacunarity,
                                       seed=seed)

    color_array = generator.assign_colors(layers, noise_array, sea_level)
    image = generator.color_array_to_image(color_array)
    landscape = pilImageToSurface(image)
    
    for human in humans:
        human.terrain = landscape

generate()

def spawn_human():
    spawn_successful = False
    while not spawn_successful:
        x = random.randint(0, WIDTH - 2)
        y = random.randint(0, HEIGHT - 2)
        terrain_color = landscape.get_at((x, y))
        if terrain_color != (22, 156, 233) and terrain_color != (45, 166, 235) and terrain_color != (68, 176, 238) and terrain_color != (58, 29, 19) and terrain_color != (92, 61, 61) and terrain_color != (245, 240, 240):
            humans.append(Human(screen, landscape, (x, y)))
            spawn_successful = True

buttons = []

generate_btn = Button(WIDTH-100, 0, 100, 50, 'Generate', generate)
spawn_human_btn = Button(WIDTH-100, 100, 100, 50, 'Spawn Human', spawn_human)
save_btn = Button(WIDTH-100, 50, 100, 50, 'Save', lambda: save(image))

buttons.append(generate_btn)
buttons.append(save_btn)
buttons.append(spawn_human_btn)

# Run the game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                for button in buttons:
                    button.is_hidden = not button.is_hidden

    screen.blit(landscape, landscape.get_rect())
    for button in buttons:
        button.process()
    
    for human in humans:
        human.update()
        human.render()
    
    pygame.display.flip()
    clock.tick(15)

pygame.quit()