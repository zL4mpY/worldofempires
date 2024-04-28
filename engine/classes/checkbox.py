import pygame

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
                 color=(0, 0, 0),
                 multipress=False,
                 normalcolor='#ffffff',
                 normaltransparency=255,
                 hovercolor='#666666',
                 hovertransparency=255,
                 pressedcolor='#333333',
                 pressedtransparency=255
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
        self.color = color
        self.falsetext = falsetext
        self.truetext = truetext
        self.currenttext = self.truetext if defaultvalue else self.falsetext
        self.align = align
        
        self.fontname = font
        
        try:
            self.font = pygame.font.Font(self.fontname, fontsize)
        except Exception:
            self.font = pygame.font.SysFont(self.fontname, fontsize)

        self.fillColors = {
            'normal': normalcolor,
            'hover': hovercolor,
            'pressed': pressedcolor,
        }
        
        self.fillTransparencies = {
            'normal': normaltransparency,
            'hover': hovertransparency,
            'pressed': pressedtransparency,
        }
         
        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.devButtonSurface = pygame.Surface((self.width, self.height))
        self.devButtonSurface.set_alpha(64)
        self.devButtonSurface.fill((0, 0, 255))
        
        self.devButtonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        if self.align == "tl":
            self.align = "topleft"
            
        elif self.align == "tr":
            self.align = "topright"
            
        elif self.align == "br":
            self.align = "bottomright"
            
        elif self.align == "bl":
            self.align = "bottomleft"
            
        elif self.align == "l":
            self.align = "left"
            
        elif self.align == "r":
            self.align = "right"
            
        elif self.align == "t":
            self.align = "top"
            
        elif self.align == "b":
            self.align = "bottom"
            
        elif self.align == "c":
            self.align = "center"
        
        if self.align in ['left', 'right']:
            setattr(self.buttonRect, self.align, x)
            setattr(self.devButtonRect, self.align, x)
            
        elif self.align in ['top, bottom']:
            setattr(self.buttonRect, self.align, y)
            setattr(self.devButtonRect, self.align, y)
            
        elif self.align in ['center', 'topleft', 'topright', 'bottomleft', 'bottomright']:
            setattr(self.buttonRect, self.align, (x, y))
            setattr(self.devButtonRect, self.align, (x, y))
                
        self.buttonSurface.set_alpha(self.fillTransparencies['normal'])
        self.buttonSurf = self.font.render(self.currenttext, True, self.color)
        self.devButtonSurf = self.font.render(self.currenttext, True, self.color)
    
    def get_value(self):
        return self.value
    
    def change_state(self, state):
        if state == 'normal':
            self.buttonSurface.fill(self.fillColors['normal'])
            self.buttonSurface.set_alpha(self.fillTransparencies['normal'])
    
        elif state == 'hover':
            self.buttonSurface.fill(self.fillColors['hover'])
            self.buttonSurface.set_alpha(self.fillTransparencies['hover'])
        
        elif state == 'pressed':
            self.buttonSurface.fill(self.fillColors['pressed'])
            self.buttonSurface.set_alpha(self.fillTransparencies['pressed'])
    
    def handle_event(self):
        mousePos = pygame.mouse.get_pos()
        
        self.change_state('normal')
        
        if self.devButtonRect.collidepoint(mousePos):
            self.change_state('hover')
            
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.multipress:
                    self.change_state('pressed')
                    self.value = self.falsevalue if self.value == self.truevalue else self.truevalue
                    self.currenttext = self.falsetext if self.value != self.truevalue else self.truetext
                    self.buttonSurf = self.font.render(self.currenttext, True, self.color)
                    self.devButtonSurf = self.font.render(self.currenttext, True, self.color)
                
                elif not self.alreadyPressed:
                    self.change_state('pressed')
                    self.value = self.falsevalue if self.value == self.truevalue else self.truevalue
                    self.currenttext = self.falsetext if self.value != self.truevalue else self.truetext
                    self.buttonSurf = self.font.render(self.currenttext, True, self.color)
                    self.devButtonSurf = self.font.render(self.currenttext, True, self.color)
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
                
    
    def render(self):
        if self.is_visible:
            self.buttonSurface.blit(self.buttonSurf, [
                self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
                self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
            ])
            self.screen.blit(self.buttonSurface, self.buttonRect)
                
        if self.game.is_devmode:
            self.devButtonSurface.blit(self.devButtonSurf, [
                    self.devButtonRect.width/2 - self.devButtonSurf.get_rect().width/2,
                    self.devButtonRect.height/2 - self.devButtonSurf.get_rect().height/2
                ])
            self.screen.blit(self.devButtonSurface, self.devButtonRect)