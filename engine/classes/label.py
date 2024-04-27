import pygame

class Label():
    def __init__(self,
                 game,
                 scene,
                 x, y,
                 text='button',
                 font='Arial',
                 fontsize=40,
                 color=(0, 0, 0),
                 side="none", align="none"
                 ):
        
        self.game = game
        self.scene = scene
        self.screen = self.scene.screen
        
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.fontsize = fontsize
        self.color = color 
        self.side, self.align = side, align     
             
    
    def render(self):
        self.game.textManager.render(surface=self.screen,
                                    x=self.x, y=self.y,
                                    text=self.text,
                                    font=self.font,
                                    color=self.color,
                                    size=self.fontsize,
                                    side=self.side,
                                    align=self.align)