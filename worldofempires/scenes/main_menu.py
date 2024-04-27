from engine.managers.sceneManager import Scene
from engine.managers.imageManager import ImageManager
from ..custom_managers.terrainGenerator import TerrainGenerator, Terrain, layers, pilImageToSurface

from engine.classes.button import Button
from engine.classes.label import Label
from engine import get_base_dir

import pygame, random

class MenuScene(Scene):
    def __init__(self, game, name):
        super().__init__(game, name)
        
        self.objects = []
        self.buttons = []
        
        self.imageManager = self.game.imageManager
        self.terrainGenerator = TerrainGenerator(self.game, self)
        self.logo = pygame.image.load(get_base_dir() / "worldofempires" / "assets" / "logo.png", "")
        self.menu_bg = pygame.image.load(get_base_dir() / "worldofempires" / "assets" / "menu_bg.png", "")
        self.terrain = None
        
        self.draw_objects()
    
    def draw_objects(self):
        def onclick():
            self.game.sceneManager.get_scene("game_process_settings_menu").terrain = self.terrain
            self.game.sceneManager.switch_scene("game_process_settings_menu")
            
        # buttons
        
        # play_btn
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=350,
                        width=200, height=75,
                        text='Play',
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False,
                        normalimage=pygame.image.load(get_base_dir() / "worldofempires" / "assets" / "start_button.png", ""),
                        hoverimage=pygame.image.load(get_base_dir() / "worldofempires" / "assets" / "start_button_hovered.png", ""),
                        pressedimage=pygame.image.load(get_base_dir() / "worldofempires" / "assets" / "start_button_pressed.png", ""),
        )

        self.buttons.append(button)
        self.objects.append(button)

        del onclick
        
        # test_btn
        # button = Button(game=self.game,
        #                 scene=self,
        #                 x=540, y=400,
        #                 width=200, height=75,
        #                 text='Test Button',
        #                 font=self.game.settingsManager.settings.get('font'),
        #                 fontsize=25,
        #                 onclick=lambda: print("test button"),
        #                 multipress=False)
        
        # labels
        
        # version_lbl
        label = Label(game=self.game,
                      scene=self,
                      x=10, y=self.game.height - 10,
                      text="v0.0.5 ALPHA",
                      font="Arial",
                      fontsize=20,
                      color=(0, 0, 0),
                      side="lb",
                      align="left")

        self.objects.append(label)
        self.terrain = self.generate_terrain()
    
    def generate_terrain(self):
        # scale = random.randint(75, 100)
        scale = 100
        seed = 0
        sea_level = random.randint(110, 125)
        # persistence = random.randint(55, 100)
        persistence = 55
        lacunarity = 25
        octaves = 6
        
        noise_array = self.terrainGenerator.generate(scale=scale,
                                                      shape=(self.game.height, self.game.width),
                                                      octaves=octaves,
                                                      persistence=persistence,
                                                      lacunarity=lacunarity,
                                                      seed=seed)

        color_array = self.terrainGenerator.assign_colors(layers, noise_array, sea_level)
        image = self.terrainGenerator.color_array_to_image(color_array)
        landscape = pilImageToSurface(image)
        
        terrain = Terrain(game=self.game, scene=self, x=0, y=0, image=image, landscape=landscape, width=self.game.width, height=self.game.height)
        return terrain
        
    def start(self):
        pass
    
    def update(self):
        for button in self.buttons:
            button.handle_event()
    
    def handle_event(self, event):
        pass
    
    def render(self):
        self.screen.fill((150, 150, 150))
        
        if self.terrain:
            self.terrain.render()
        
        # self.imageManager.render(self.screen, self.menu_bg, 0, 0, 1, align="tl")
        self.imageManager.render(self.screen, self.logo, 150, 10, 1)
        
        for object in self.objects:
            object.render()
        
        
        