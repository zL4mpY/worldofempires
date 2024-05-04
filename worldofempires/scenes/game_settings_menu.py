from engine.managers.sceneManager import Scene
from engine.managers.imageManager import ImageManager

from engine.classes.button import Button
from engine.classes.label import Label
from engine.classes.textinput import TextInputBox
from engine.classes.checkbox import CheckBox
from engine.classes.image import Image
from engine import get_base_dir

import pygame

class GameSettingsMenuScene(Scene):
    def __init__(self, game, name):
        super().__init__(game, name)
        
        self.terrain = None
        
        self.draw_objects()
    
    def draw_objects(self):
        # text and text inputs:
        width, height = self.settingsManager.get_resolution()
        
        self.uiManager.add_element(element=Image(game=self.game,
                                         scene=self,
                                         x=self.game.width / 2, y=0+self.game.height / 5,
                                         image=get_base_dir() / "worldofempires" / "assets" / "logo.png",
                                         align='c'),
                                   id="game_logo")
        
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2, y= self.game.height / 2 - 80,
                      text=f"{self.game.lang.get('screen_width_label')}:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="right")
        
        self.uiManager.add_element(label, 'screen_width_label')
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 + 4, y = self.game.height / 2 - 84,
                                    width = 30, height = 25,
                                    defaulttext=str(width), textcolor=(0, 0, 0), textlimit=4,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='centerleft', allowedchars='0123456789')
        
        self.uiManager.add_element(textinputbox, 'screen_width_textinputbox')
        del textinputbox
    
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2, y= self.game.height / 2 - 30,
                      text=f"{self.game.lang.get('screen_height_label')}:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="right")
        
        self.uiManager.add_element(label, 'screen_height_label')
        del label
        
        textinputbox = TextInputBox(game=self.game,
                                    scene=self,
                                    x=self.game.width / 2 + 4, y = self.game.height / 2 - 34,
                                    width = 30, height = 25,
                                    defaulttext=str(height), textcolor=(0, 0, 0), textlimit=4,
                                    font='Arial', fontsize=24,
                                    boxcolor=(235, 235, 235),
                                    activecolor=(255, 255, 255),
                                    align='centerleft', allowedchars='0123456789')
        
        self.uiManager.add_element(textinputbox, 'screen_height_textinputbox')
        del textinputbox
        
        label = Label(game=self.game,
                      scene=self,
                      x=self.game.width / 2, y= self.game.height / 2 + 20,
                      text=f"{self.game.lang.get('fullscreen_label')}:",
                      font="Arial", fontsize=24,
                      color=(0, 0, 0),
                      align="right")
        
        self.uiManager.add_element(label, 'fullscreen_state_label')
        del label
        
        checkbox = CheckBox(game=self.game,
                            scene=self,
                            x=self.game.width / 2 + 10, y= self.game.height / 2 + 20,
                            width=55, height=30,
                            align='centerleft',
                            defaultvalue=self.settingsManager.get("fullscreen"),
                            falsevalue=False,
                            truevalue=True,
                            falsetext=f"{self.game.lang.get('off')}",
                            truetext=f"{self.game.lang.get('on')}")
        
        self.uiManager.add_element(checkbox, 'fullscreen_state_checkbox')
        del checkbox
            
        # buttons
        
        def onclick():
            self.settingsManager.set("resolution", str(self.uiManager.get_element('screen_width_textinputbox').get_value() + 'x' + self.uiManager.get_element('screen_height_textinputbox').get_value()))
            self.settingsManager.set("fullscreen", self.uiManager.get_element('fullscreen_state_checkbox').get_value())
            self.settingsManager.save_settings()
            self.game.restart()
        
        # play_btn
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height-120,
                        width=200, height=50,
                        text=f'{self.game.lang.get("apply")}',
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False,
                        )

        self.uiManager.add_element(button, 'apply_button')

        del onclick
        del button
        
        def onclick():
            self.game.sceneManager.switch_scene("menu")
        
        # play_btn
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height-60,
                        width=200, height=50,
                        text=f"{self.game.lang.get('menu')}",
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False,
                        )

        self.uiManager.add_element(button, 'menu_button')

        del onclick
        del button
        
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
                      x=self.game.width / 2, y=self.game.height - 300,
                      text=f"{self.game.lang.get('language_label')}",
                      font="Arial",
                      fontsize=20,
                      color=(0, 0, 0),
                      align="center")

        self.uiManager.add_element(label, 'version_label')
        del label
        
        def onclick():
            self.settingsManager.set('language', 'en_US')
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height-210,
                        width=100, height=40,
                        text=f"English",
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False,
                        )

        self.uiManager.add_element(button, 'en_lang_btn')
        del onclick
        del button
        
        def onclick():
            self.settingsManager.set('language', 'ru_RU')
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width / 2, y=self.game.height-260,
                        width=100, height=40,
                        text=f"Русский",
                        scale=1,
                        align="center",
                        font=self.game.settingsManager.settings.get('font'),
                        fontsize=25,
                        onclick=onclick,
                        multipress=False,
                        )

        self.uiManager.add_element(button, 'ru_lang_btn')
        del onclick
        del button
        
        
    
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
        
        
        