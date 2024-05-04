import pygame
from engine import get_align, set_align, set_align_add

class CheckBox():
    def __init__(self,
                 game,
                 scene,
                 x, y,
                 width,
                 height,
                 align="center",
                 defaultvalue=False,
                 falsevalue=False,
                 truevalue=True,
                 falsetext='off',
                 truetext='on',
                 font='Arial',
                 fontsize=20,
                 textcolor=(0, 0, 0),
                 multipress=False,
                 boxcolor='#ffffff',
                 outlinecolor=(225, 225, 225),
                 outlinewidth=2
                 ):
        
        self.game = game
        self.scene = scene
        self.screen = self.game.screen
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.multipress = multipress
        self.alreadyPressed = False
        
        self.value = defaultvalue
        self.falsevalue = falsevalue
        self.truevalue = truevalue

        self.is_visible = True
        self.textcolor = textcolor
        self.falsetext = falsetext
        self.truetext = truetext
        self.currenttext = self.truetext if defaultvalue else self.falsetext
        self.align = align
        self.outlinewidth = outlinewidth
        
        self.fontname = font
        self.fontsize = fontsize
        
        try:
            self.font = pygame.font.Font(self.fontname, fontsize)
        except Exception:
            self.font = pygame.font.SysFont(self.fontname, fontsize)
        
        self.boxcolor = boxcolor
        self.outlinecolor = outlinecolor
         
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.surface.fill(self.boxcolor)
        
        self.bgSurface = pygame.Surface((self.width+(self.outlinewidth*2), self.height+(self.outlinewidth*2)))
        self.bgRect = pygame.Rect(x-(self.outlinewidth*2), y-(self.outlinewidth*2), self.width-(self.outlinewidth*2), self.height-(self.outlinewidth*2))
        self.bgSurface.fill(self.outlinecolor)
        
        self.devSurface = pygame.Surface((self.width+(self.outlinewidth*2), self.height+(self.outlinewidth*2)))
        self.devSurface.set_alpha(64)
        self.devSurface.fill((0, 0, 255))
        
        self.devRect = pygame.Rect(self.x, self.y, self.width+self.outlinewidth*2, self.height+self.outlinewidth*2)
        
        self.align = get_align(self.align)
        
        self.rect.x, self.rect.y = set_align(self.align, self.rect, self.x, self.y)
        self.bgRect.x, self.bgRect.y = set_align_add(self.align, self.bgRect, self.outlinewidth, self.outlinewidth, self.x, self.y)
        self.devRect.x, self.devRect.y = set_align_add(self.align, self.devRect, self.outlinewidth, self.outlinewidth, self.x, self.y)
                
        self.surf = self.font.render(self.currenttext, True, self.textcolor)
        self.devSurf = self.font.render(self.currenttext, True, self.textcolor)
    
    def get_value(self):
        return self.value
    
    def update(self):
        # mousePos = pygame.mouse.get_pos()
        
        # if self.devRect.collidepoint(mousePos):
            
        #     if pygame.mouse.get_pressed(num_buttons=3)[0]:
        #         if self.multipress:
        #             self.value = self.falsevalue if self.value == self.truevalue else self.truevalue
        #             self.currenttext = self.falsetext if self.value != self.truevalue else self.truetext
        #             self.surf = self.font.render(self.currenttext, True, self.textcolor)
        #             self.devSurf = self.font.render(self.currenttext, True, self.textcolor)
                
        #         elif not self.alreadyPressed:
        #             self.value = self.falsevalue if self.value == self.truevalue else self.truevalue
        #             self.currenttext = self.falsetext if self.value != self.truevalue else self.truetext
        #             self.surf = self.font.render(self.currenttext, True, self.textcolor)
        #             self.devSurf = self.font.render(self.currenttext, True, self.textcolor)
        #             self.alreadyPressed = True
        #     else:
        #         self.alreadyPressed = False
        mousePos = pygame.mouse.get_pos()
        
        if self.devRect.collidepoint(mousePos):
            
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.multipress:
                    self.value = self.falsevalue if self.value == self.truevalue else self.truevalue
                    self.currenttext = self.falsetext if self.value != self.truevalue else self.truetext
                    self.surf = self.font.render(self.currenttext, True, self.textcolor)
                
                elif not self.alreadyPressed:
                    self.value = self.falsevalue if self.value == self.truevalue else self.truevalue
                    self.currenttext = self.falsetext if self.value != self.truevalue else self.truetext
                    self.surf = self.font.render(self.currenttext, True, self.textcolor)
                    
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
    
    def handle_event(self, event):
        pass
    
    def render(self):
        if self.is_visible:
            
            
            self.bgSurface.fill(self.outlinecolor)
            self.screen.blit(self.bgSurface, self.bgRect)
            
            self.surface.fill(self.boxcolor)
            self.surface.blit(self.surf, [
                (self.rect.width - self.surf.get_rect().width ) /2,
                (self.rect.height - self.surf.get_rect().height) /2
            ])
            self.screen.blit(self.surface, self.rect)
                
        if self.game.is_devmode:
            self.screen.blit(self.devSurface, self.devRect)