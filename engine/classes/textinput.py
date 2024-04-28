import pygame

class TextInputBox():
    def __init__(self,
                 game,
                 scene,
                 x, y,
                 width, height,
                 defaulttext='',
                 textlimit=32,
                 textcolor=(0, 0, 0),
                 font='Arial',
                 fontsize=14,
                 boxcolor=(225, 225, 225),
                 activecolor=(255, 255, 255),
                 outlinecolor=(190, 190, 190),
                 activeoutlinecolor=(220, 220, 220),
                 align='tl',
                 allowedchars='all'):
        
        self.game = game
        self.scene = scene
        self.screen = self.scene.screen
        self.align = align
        
        self.width, self.height = width, height
        
        if self.height < fontsize + 2:
            self.height = fontsize + 2
            
        self.bgsurface = pygame.Surface((width-4, height-4))
        self.bgrect = pygame.Rect(x-4, y-4, self.width-4, self.height-4)
            
        self.surface = pygame.Surface((width, height))
        self.rect = pygame.Rect(x, y, self.width, self.height)
            
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
            setattr(self.rect, self.align, x)
            setattr(self.bgrect, self.align, x-4)
            
        elif self.align in ['top, bottom']:
            setattr(self.rect, self.align, y)
            setattr(self.bgrect, self.align, y-4)
            
        elif self.align in ['center', 'topleft', 'topright', 'bottomleft', 'bottomright']:
            setattr(self.rect, self.align, (x, y))
            setattr(self.bgrect, self.align, (x-4, y-4))

        self.color = boxcolor
        self.activecolor = activecolor
        
        self.outlinecolor = outlinecolor
        self.activeoutlinecolor = activeoutlinecolor
        
        self.defaulttext = defaulttext
        self.text = self.defaulttext
        self.textcolor = textcolor
        self.textlimit = textlimit
        self.fontname = font
        self.fontsize = fontsize
        self.allowedchars = allowedchars
        
        try:
            self.font = pygame.font.Font(self.fontname, self.fontsize)
        except Exception:
            self.font = pygame.font.SysFont(self.fontname, self.fontsize)
        
        self.isactive = False
        self.currentcolor = self.color
        self.currentoutlinecolor = self.outlinecolor
        self.is_erasing = False
    
    def get_value(self) -> str:
        return self.text
    
    def handle_event(self, event): 
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.isactive = True
                self.currentcolor = self.activecolor
                self.currentoutlinecolor = self.activeoutlinecolor
            else:
                self.isactive = False
                self.currentcolor = self.color
                self.currentoutlinecolor = self.outlinecolor

        else:
            if self.isactive:
                if event.type == pygame.KEYDOWN:  
                    if event.key == pygame.K_RETURN:
                        self.isactive = False

                    elif event.key == pygame.K_BACKSPACE:
                        self.is_erasing = True
                
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_BACKSPACE:
                        self.is_erasing = False
                    
                elif event.type == pygame.TEXTINPUT:
                    if len(self.text) < self.textlimit:
                        if self.allowedchars != 'all':
                            if event.text in self.allowedchars:
                                self.text += event.text
    
    def update(self):
        if self.is_erasing:
            self.text = self.text[:-1]
    
    def render(self):
        text_surface = self.font.render(self.text, True, self.textcolor)
        self.rect.w = text_surface.get_width()+10
        self.surface = pygame.Surface((self.rect.w, self.height))
        
        self.bgrect.w = text_surface.get_width()+14
        self.bgsurface = pygame.Surface((self.bgrect.w, self.height+4))
        
        self.bgsurface.fill(self.currentoutlinecolor)
        self.surface.fill(self.currentcolor)
         
        self.screen.blit(self.bgsurface, (self.bgrect.x+5, self.bgrect.y+5))
        self.screen.blit(self.surface, (self.rect.x+5, self.rect.y+5))
        self.screen.blit(text_surface, (self.rect.x+10, self.rect.y+5))
        