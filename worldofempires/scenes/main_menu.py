from engine.managers.sceneManager import Scene
from engine.managers.imageManager import ImageManager
from ..custom_managers.terrainGenerator import TerrainGenerator, Terrain, layers, pilImageToSurface

from engine.classes.button import Button
from engine.classes.label import Label
from engine.classes.image import Image
from engine import get_base_dir

import pygame, random

class MenuScene(Scene):
    def __init__(self, game, name):
        super().__init__(game, name)
        
        self.terrainGenerator = TerrainGenerator(self.game, self)
        self.terrain = None
        
        self.draw_objects()
    
    def draw_objects(self):
        self.uiManager.add_element(element=Image(game=self.game,
                                         scene=self,
                                         x=self.game.width / 2, y=0+self.game.height / 5,
                                         image=get_base_dir() / "worldofempires" / "assets" / "logo.png",
                                         align='c'),
                                   id="game_logo")
        
        def onclick():
            self.sceneManager.get_scene("map_settings_menu").terrain = self.terrain
            self.sceneManager.switch_scene("map_settings_menu")
            
        # buttons
        
        # play_btn
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height / 2 + 20,
                        width=200, height=50,
                        text=f'{self.game.lang.get("play")}',
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False,
        )

        self.uiManager.add_element(button, 'play_button')

        del onclick
        del button
        
        def onclick():
            self.sceneManager.get_scene("game_settings_menu").terrain = self.terrain
            self.sceneManager.switch_scene('game_settings_menu')
        
        # test_btn
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height / 2 + 120,
                        width=200, height=50,
                        text=f'{self.game.lang.get("settings")}',
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False,
                        align='center')

        self.uiManager.add_element(button, 'settings_button')

        del onclick
        del button
        
        # labels
        
        # version_lbl
        label = Label(game=self.game,
                      scene=self,
                      x=10, y=self.game.height - 10,
                      text=f"v{self.game.get_version()}",
                      font="Arial",
                      fontsize=20,
                      color=(0, 0, 0),
                      side="lb",
                      align="left")

        self.uiManager.add_element(label, 'version_label')
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
        self.uiManager.update_ui()
    
    def handle_event(self, event):
        self.uiManager.handle_event(event)
    
    def render(self):
        self.screen.fill((150, 150, 150))
        
        if self.terrain:
            self.terrain.render()
        
        self.uiManager.render_ui()
        
        
        