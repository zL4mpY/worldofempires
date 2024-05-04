import pygame
from engine import get_align, set_align, set_align_add

class Button():
    def __init__(self,
                 game,
                 scene,
                 x, y,
                 width,
                 height,
                 align="center",
                 text='button',
                 scale=1,
                 font='Arial',
                 fontsize=40,
                 color=(0, 0, 0),
                 onclick=None,
                 onhover=None,
                 multipress=False,
                 normalcolor='#ffffff',
                 normaltransparency=255,
                 hovercolor='#666666',
                 hovertransparency=255,
                 pressedcolor='#333333',
                 pressedtransparency=255,
                 normalimage=None,
                 hoverimage=None,
                 pressedimage=None
                 ):
        
        self.game = game
        self.scene = scene
        self.screen = self.game.screen
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.onclick = onclick
        self.onhover = onhover
        
        self.multipress = multipress
        self.alreadyPressed = False
        self.image = normalimage
        self.scale = scale
        
        self.image_to_render = self.image
        self.is_visible = True
        self.color = color
        self.text = text
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
        
        self.fillImages = {
            'normal': self.image,
            'hover': hoverimage,
            'pressed': pressedimage,
        }
         
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.devSurface = pygame.Surface((self.width, self.height))
        self.devSurface.set_alpha(64)
        self.devSurface.fill((0, 0, 255))
        
        self.devRect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.align = get_align(self.align)
        set_align(self.align, self.rect, self.x, self.y)
        set_align(self.align, self.devRect, self.x, self.y)
        
        # if self.align == "tl":
        #     self.align = "topleft"
            
        # elif self.align == "tr":
        #     self.align = "topright"
            
        # elif self.align == "br":
        #     self.align = "bottomright"
            
        # elif self.align == "bl":
        #     self.align = "bottomleft"
            
        # elif self.align == "l":
        #     self.align = "left"
            
        # elif self.align == "r":
        #     self.align = "right"
            
        # elif self.align == "t":
        #     self.align = "top"
            
        # elif self.align == "b":
        #     self.align = "bottom"
            
        # elif self.align == "c":
        #     self.align = "center"
        
        # if self.align in ['left', 'right']:
        #     setattr(self.rect, self.align, x)
        #     setattr(self.devRect, self.align, x)
            
        # elif self.align in ['top, bottom']:
        #     setattr(self.rect, self.align, y)
        #     setattr(self.devRect, self.align, y)
            
        # elif self.align in ['center', 'topleft', 'topright', 'bottomleft', 'bottomright']:
        #     setattr(self.rect, self.align, (x, y))
        #     setattr(self.devRect, self.align, (x, y))
                
        self.surface.set_alpha(self.fillTransparencies['normal'])

        if self.image == None:
            self.surf = self.font.render(self.text, True, self.color)
            self.devSurf = self.font.render(self.text, True, self.color)
            
        else:
            self.devSurf = pygame.Surface(self.scene.imageManager.get_surface(self.image_to_render, self.x, self.y, self.scale, self.align))
    
    def change_text(self, text):
        self.text = text
        
        if self.image == None:
            self.surf = self.font.render(self.text, True, self.color)
            self.devSurf = self.font.render(self.text, True, self.color)
    
    def change_font(self, font, fontsize):
        self.fontsize = fontsize if fontsize != None else self.fontsize
        
        try:
            self.font = pygame.font.Font(font, fontsize) if font != None else pygame.font.Font(self.fontname, fontsize)
        except Exception:
            self.font = pygame.font.SysFont(font, fontsize) if font != None else pygame.font.SysFont(self.fontname, fontsize)

        if self.image == None:
            self.surf = self.font.render(self.text, True, self.color)
            self.devSurf = self.font.render(self.text, True, self.color)
    
    def change_state(self, state):
        if self.image == None:
            if state == 'normal':
                self.surface.fill(self.fillColors['normal'])
                self.surface.set_alpha(self.fillTransparencies['normal'])
        
            elif state == 'hover':
                self.surface.fill(self.fillColors['hover'])
                self.surface.set_alpha(self.fillTransparencies['hover'])
            
            elif state == 'pressed':
                self.surface.fill(self.fillColors['pressed'])
                self.surface.set_alpha(self.fillTransparencies['pressed'])
        
        else:
            if state == 'normal':
                self.image_to_render = self.fillImages['normal']
            
            elif state == 'hover':
                self.image_to_render = self.fillImages['hover']
            
            elif state == 'pressed':
                self.image_to_render = self.fillImages['pressed']
    
    def update(self):
        mousePos = pygame.mouse.get_pos()
        
        self.change_state('normal')
        
        if self.devRect.collidepoint(mousePos):
            self.change_state('hover')
            
            if self.onhover: self.onhover()
            
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if self.multipress:
                    self.change_state('pressed')
                    if self.onclick: self.onclick()
                
                elif not self.alreadyPressed:
                    self.change_state('pressed')
                    if self.onclick: self.onclick()
                    self.alreadyPressed = True
            else:
                self.alreadyPressed = False
    
    def handle_event(self, event):
        pass          
    
    def render(self):
        if self.is_visible:
            if self.image == None:
                self.surface.blit(self.surf, [
                    self.rect.width/2 - self.surf.get_rect().width/2,
                    self.rect.height/2 - self.surf.get_rect().height/2
                ])
                self.screen.blit(self.surface, self.rect)
            else:
                self.scene.imageManager.render(self.screen, self.image_to_render, self.x, self.y, self.scale, self.align)
                
        if self.game.is_devmode:
            self.devSurface.blit(self.devSurf, [
                    self.devRect.width/2 - self.devSurf.get_rect().width/2,
                    self.devRect.height/2 - self.devSurf.get_rect().height/2
                ])
            self.screen.blit(self.devSurface, self.devRect)