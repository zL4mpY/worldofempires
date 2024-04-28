from engine.managers.sceneManager import Scene
from engine.managers.imageManager import ImageManager

from engine.classes.button import Button
from engine.classes.label import Label
from engine.classes.textinput import TextInputBox
from engine import get_base_dir

import pygame

class MapSettingsMenuScene(Scene):
    def __init__(self, game, name):
        super().__init__(game, name)
        
        self.objects = []
        self.buttons = []
        self.labels = []
        self.textinputboxes = []
        
        self.imageManager = self.game.imageManager
        self.logo = pygame.image.load(get_base_dir() / "worldofempires" / "assets" / "logo.png", "")
        self.menu_bg = pygame.image.load(get_base_dir() / "worldofempires" / "assets" / "menu_bg.png", "")
        self.terrain = None
        
        self.draw_objects()
    
    def draw_objects(self):
        # text and text inputs:
        
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 - 100, y= self.game.height / 2 - 80,
                      text="Minimal countries amount:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="c")
        
        self.labels.append(label)
        self.objects.append(label)
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 + 60, y = self.game.height / 2 - 84,
                                    width = 30, height = 25,
                                    defaulttext='2', textcolor=(0, 0, 0), textlimit=3,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='c', allowedchars='0123456789')
        
        self.textinputboxes.append(textinputbox)
        self.objects.append(textinputbox)
        del textinputbox
    
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 - 100, y= self.game.height / 2 - 30,
                      text="Maximal countries amount:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="c")
        
        self.labels.append(label)
        self.objects.append(label)
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 + 60, y = self.game.height / 2 - 34,
                                    width = 30, height = 25,
                                    defaulttext='5', textcolor=(0, 0, 0), textlimit=3,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='c', allowedchars='0123456789')
        
        self.textinputboxes.append(textinputbox)
        self.objects.append(textinputbox)
        del textinputbox

        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 - 100, y= self.game.height / 2 + 20,
                      text="Map width:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="c")
        
        self.labels.append(label)
        self.objects.append(label)
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 - 25, y = self.game.height / 2 + 15,
                                    width = 30, height = 25,
                                    defaulttext=str(self.game.width * 2), textcolor=(0, 0, 0), textlimit=4,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='c', allowedchars='0123456789')
        
        self.textinputboxes.append(textinputbox)
        self.objects.append(textinputbox)
        del textinputbox
        
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 - 100, y= self.game.height / 2 + 70,
                      text="Map height:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="c")
        
        self.labels.append(label)
        self.objects.append(label)
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 - 20, y = self.game.height / 2 + 66,
                                    width = 30, height = 25,
                                    defaulttext=str(self.game.height * 2), textcolor=(0, 0, 0), textlimit=4,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='c', allowedchars='0123456789')
        
        self.textinputboxes.append(textinputbox)
        self.objects.append(textinputbox)
        del textinputbox
            
        # buttons
        
        def onclick():
            def start_game():
                self.game.sceneManager.get_scene('game_process').settings = {'countries': {'min_value': int(self.textinputboxes[0].get_value()),
                                                                                           'max_value': int(self.textinputboxes[1].get_value())},
                                                                             'map': {'width': int(self.textinputboxes[2].get_value()),
                                                                                     'height': int(self.textinputboxes[3].get_value())}}
                self.game.sceneManager.switch_scene("game_process")
            
            self.game.sceneManager.get_scene('loading_screen').custom_action = start_game
            self.game.sceneManager.switch_scene('loading_screen')
        
        # play_btn
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height-180,
                        width=200, height=50,
                        text='Start',
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False
        )
        
        self.buttons.append(button)
        self.objects.append(button)

        del onclick
        
        def onclick():
            self.game.sceneManager.switch_scene("menu")
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height-100,
                        width=200, height=50,
                        text='Menu',
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False
        )

        self.buttons.append(button)
        self.objects.append(button)

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

        self.objects.append(label)
        
    
    def start(self):
        pass
    
    def update(self):
        for button in self.buttons:
            button.handle_event()
        
        for textinputbox in self.textinputboxes:
            textinputbox.update()
    
    def handle_event(self, event):
        for textinputbox in self.textinputboxes:
            textinputbox.handle_event(event)
    
    def render(self):
        self.screen.fill((150, 150, 150))
        self.terrain.render()
        self.imageManager.render(self.screen, self.logo, 150, 10, 1)
        
        for object in self.objects:
            object.render()
        
        
        