from engine.managers.sceneManager import Scene
from engine.managers.imageManager import ImageManager

from engine.classes.button import Button
from engine.classes.label import Label
from engine.classes.textinput import TextInputBox
from engine.classes.checkbox import CheckBox
from engine import get_base_dir

import pygame

class GameSettingsMenuScene(Scene):
    def __init__(self, game, name):
        super().__init__(game, name)
        
        self.objects = []
        self.buttons = []
        self.labels = []
        self.textinputboxes = []
        self.checkboxes = []
        
        self.imageManager = self.game.imageManager
        self.logo = pygame.image.load(get_base_dir() / "worldofempires" / "assets" / "logo.png", "")
        self.menu_bg = pygame.image.load(get_base_dir() / "worldofempires" / "assets" / "menu_bg.png", "")
        self.terrain = None
        
        self.draw_objects()
    
    def draw_objects(self):
        # text and text inputs:
        width, height = self.settingsManager.get_resolution()
        
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 - 50, y= self.game.height / 2 - 80,
                      text="Screen width:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="c")
        
        self.labels.append(label)
        self.objects.append(label)
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 + 50, y = self.game.height / 2 - 84,
                                    width = 30, height = 25,
                                    defaulttext=str(width), textcolor=(0, 0, 0), textlimit=4,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='c', allowedchars='0123456789')
        
        self.textinputboxes.append(textinputbox)
        self.objects.append(textinputbox)
        del textinputbox
    
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 - 50, y= self.game.height / 2 - 30,
                      text="Screen height:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="c")
        
        self.labels.append(label)
        self.objects.append(label)
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 + 50, y = self.game.height / 2 - 34,
                                    width = 30, height = 25,
                                    defaulttext=str(height), textcolor=(0, 0, 0), textlimit=4,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='c', allowedchars='0123456789')
        
        self.textinputboxes.append(textinputbox)
        self.objects.append(textinputbox)
        del textinputbox
        
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2 - 50, y= self.game.height / 2 + 20,
                      text="Fullscreen:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="c")
        
        self.labels.append(label)
        self.objects.append(label)
        del label
        
        checkbox = CheckBox(game=self.game,
                            scene=self,
                            x=self.game.width / 2 + 30, y= self.game.height / 2 + 20,
                            width=35, height=30,
                            align='center',
                            defaultvalue=self.settingsManager.get("fullscreen"),
                            falsevalue=False,
                            truevalue=True,
                            falsetext="off",
                            truetext="on")
        
        self.checkboxes.append(checkbox)
        self.objects.append(checkbox)
        del checkbox
            
        # buttons
        
        def onclick():
            self.settingsManager.set("resolution", str(self.textinputboxes[0].get_value() + 'x' + self.textinputboxes[1].get_value()))
            self.settingsManager.set("fullscreen", self.checkboxes[0].get_value())
            self.settingsManager.save_settings()
            self.game.restart()
        
        # play_btn
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height-170,
                        width=200, height=50,
                        text='Apply',
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False,
                        )

        self.buttons.append(button)
        self.objects.append(button)

        del onclick
        
        def onclick():
            self.game.sceneManager.switch_scene("menu")
        
        # play_btn
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height-110,
                        width=200, height=50,
                        text='Menu',
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False,
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
        
        for checkbox in self.checkboxes:
            checkbox.handle_event()
        
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
        
        
        