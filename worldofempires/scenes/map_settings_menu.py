from engine.managers.sceneManager import Scene
from engine.managers.imageManager import ImageManager

from engine.classes.button import Button
from engine.classes.label import Label
from engine.classes.image import Image
from engine.classes.textinput import TextInputBox
from engine import get_base_dir

import pygame

class MapSettingsMenuScene(Scene):
    def __init__(self, game, name):
        super().__init__(game, name)
        
        self.terrain = None
        
        self.draw_objects()
    
    def draw_objects(self):
        self.uiManager.add_element(element=Image(game=self.game,
                                         scene=self,
                                         x=self.game.width / 2, y=0+self.game.height / 5,
                                         image=get_base_dir() / "worldofempires" / "assets" / "logo.png",
                                         align='c'),
                                   id="game_logo")
        
        # text and text inputs:
        
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 - 150, y= self.game.height / 2 - 80,
                      text=f"{self.game.lang.get('min_countries_label')}:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="right")
        
        self.uiManager.add_element(label, 'map_min_countries_label')
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 - 145, y = self.game.height / 2 - 98,
                                    width = 30, height = 25,
                                    defaulttext='2', textcolor=(0, 0, 0), textlimit=3,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='topleft', allowedchars='0123456789')

        self.uiManager.add_element(textinputbox, 'map_min_countries_textinputbox')
        del textinputbox
    
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 - 150, y= self.game.height / 2 - 30,
                      text=f"{self.game.lang.get('max_countries_label')}:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="right")
        
        self.uiManager.add_element(label, 'map_max_countries_label')
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 - 145, y = self.game.height / 2 - 48,
                                    width = 30, height = 25,
                                    defaulttext='5', textcolor=(0, 0, 0), textlimit=3,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='topleft', allowedchars='0123456789')
        
        self.uiManager.add_element(textinputbox, 'map_max_countries_textinputbox')
        del textinputbox

        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 - 150, y= self.game.height / 2 + 20,
                      text=f"{self.game.lang.get('map_width_label')}:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="right")
        
        self.uiManager.add_element(label, 'map_width_label')
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 - 145, y = self.game.height / 2 + 3,
                                    width = 30, height = 25,
                                    defaulttext=str(self.game.width * 2), textcolor=(0, 0, 0), textlimit=4,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='topleft', allowedchars='0123456789')
        
        self.uiManager.add_element(textinputbox, 'map_width_textinputbox')
        del textinputbox
        
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 - 150, y= self.game.height / 2 + 70,
                      text=f"{self.game.lang.get('map_height_label')}:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="right")
        
        self.uiManager.add_element(label, 'map_height_label')
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 - 145, y = self.game.height / 2 + 53,
                                    width = 30, height = 25,
                                    defaulttext=str(self.game.height * 2), textcolor=(0, 0, 0), textlimit=4,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='topleft', allowedchars='0123456789')
        
        self.uiManager.add_element(textinputbox, 'map_height_textinputbox')
        del textinputbox
            
        # buttons
        
        def onclick():
            def start_game():
                self.game.sceneManager.get_scene('game_process').settings = {'countries': {'min_value': int(self.uiManager.get_element('map_min_countries_textinputbox').get_value()),
                                                                                           'max_value': int(self.uiManager.get_element('map_max_countries_textinputbox').get_value())},
                                                                             'map': {'width': int(self.uiManager.get_element('map_width_textinputbox').get_value()),
                                                                                     'height': int(self.uiManager.get_element('map_height_textinputbox').get_value()),
                                                                                     'sea_level': int(self.uiManager.get_element('map_sea_level_textinputbox').get_value()),
                                                                                     'zoom': int(self.uiManager.get_element('map_zoom_textinputbox').get_value()),
                                                                                     'seed': int(self.uiManager.get_element('map_seed_textinputbox').get_value())}}
                self.game.sceneManager.switch_scene("game_process")
            
            self.game.sceneManager.get_scene('loading_screen').custom_action = start_game
            self.game.sceneManager.switch_scene('loading_screen')
        
        # play_btn
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height-180,
                        width=200, height=50,
                        text=f'{self.game.lang.get("start")}',
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False
        )
        
        self.uiManager.add_element(button, 'start_button')
        del button
        del onclick
        
        def onclick():
            self.game.sceneManager.switch_scene("menu")
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height-100,
                        width=200, height=50,
                        text=f"{self.game.lang.get('menu')}",
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False
        )

        self.uiManager.add_element(button, 'menu_button')
        del button
        del onclick
        
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
        del label
        
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 + 190, y= self.game.height / 2 - 80,
                      text=f"{self.game.lang.get('sea_level_label')}:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="right")
        
        self.uiManager.add_element(label, 'map_sea_level_label')
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 + 195, y = self.game.height / 2 - 97,
                                    width = 30, height = 25,
                                    defaulttext='100', textcolor=(0, 0, 0), textlimit=3,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='topleft', allowedchars='0123456789')
        
        self.uiManager.add_element(textinputbox, 'map_sea_level_textinputbox')
        del textinputbox
        
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 + 190, y= self.game.height / 2 - 30,
                      text=f"{self.game.lang.get('zoom_label')}:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="right")
        
        self.uiManager.add_element(label, 'map_zoom_label')
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 + 195, y = self.game.height / 2 - 47,
                                    width = 30, height = 25,
                                    defaulttext='100', textcolor=(0, 0, 0), textlimit=3,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='topleft', allowedchars='0123456789')
        
        self.uiManager.add_element(textinputbox, 'map_zoom_textinputbox')
        del textinputbox
        
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 + 190, y= self.game.height / 2 + 20,
                      text=f"{self.game.lang.get('seed_label')}:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="right")
        
        self.uiManager.add_element(label, 'map_seed_label')
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 + 195, y = self.game.height / 2 + 3,
                                    width = 30, height = 25,
                                    defaulttext='0', textcolor=(0, 0, 0), textlimit=7,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='topleft', allowedchars='-0123456789')
        
        self.uiManager.add_element(textinputbox, 'map_seed_textinputbox')
        del textinputbox
        
    
    def start(self):
        pass
    
    def update(self):
        self.uiManager.update_ui()
    
    def handle_event(self, event):
        self.uiManager.handle_event(event)
    
    def render(self):
        self.screen.fill((150, 150, 150))
        self.terrain.render()
        
        self.uiManager.render_ui()
        
        
        
        