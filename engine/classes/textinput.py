import pygame
from engine import get_align, set_align, set_align_add

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
                 outlinewidth=2,
                 activeoutlinecolor=(220, 220, 220),
                 align='tl',
                 allowedchars='all'):
        
        self.game = game
        self.scene = scene
        self.screen = self.scene.screen
        self.align = align
        self.outlinewidth = outlinewidth
        
        self.width, self.height = width, height
        
        if self.height < fontsize + 2:
            self.height = fontsize + 2
            
        self.bgsurface = pygame.Surface((width-(outlinewidth*2), height-(outlinewidth*2)))
        self.bgrect = pygame.Rect(x-(outlinewidth*2), y-(outlinewidth*2), self.width-(outlinewidth*2), self.height-(outlinewidth*2))
            
        self.surface = pygame.Surface((width, height))
        self.rect = pygame.Rect(x, y, self.width, self.height)
            
        self.align = get_align(self.align)
        self.rect.x, self.rect.y = set_align(self.align, self.rect, x, y)
        self.bgrect.x, self.bgrect.y = set_align_add(self.align, self.bgrect, self.outlinewidth, self.outlinewidth, x, y)
        
        # if self.align in ['left', 'right']:
        #     setattr(self.rect, self.align, x)
        #     setattr(self.bgrect, self.align, x-outlinewidth)
        #     setattr(self.bgrect, "top", y-2)
            
        # elif self.align in ['top, bottom']:
        #     setattr(self.rect, self.align, y)
        #     setattr(self.bgrect, self.align, y-outlinewidth*2)
            
        # elif self.align in ['center', 'topleft', 'topright', 'bottomleft', 'bottomright']:
        #     setattr(self.rect, self.align, (x, y))
        #     setattr(self.bgrect, self.align, (x-outlinewidth*2, y-outlinewidth*2))
        
        # elif self.align == 'centerleft':
        #     setattr(self.rect, "center", (x, y))
        #     setattr(self.rect, "left", x)
        #     setattr(self.bgrect, "center", (x-outlinewidth, y-outlinewidth))
        #     setattr(self.bgrect, "left", x-2)
        
        # elif self.align == 'centerright':
        #     setattr(self.rect, "center", (x, y))
        #     setattr(self.rect, "right", x)
        #     setattr(self.bgrect, "center", (x-outlinewidth, y-outlinewidth))
        #     setattr(self.bgrect, "right", x-outlinewidth)

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
        
        self.bgrect.w = text_surface.get_width()+10 + self.outlinewidth * 2
        self.bgsurface = pygame.Surface((self.bgrect.w, self.height+(self.outlinewidth*2)))
        
        self.bgsurface.fill(self.currentoutlinecolor)
        self.surface.fill(self.currentcolor)
         
        self.screen.blit(self.bgsurface, (self.bgrect.x+5, self.bgrect.y+5))
        self.screen.blit(self.surface, (self.rect.x+5, self.rect.y+5))
        self.screen.blit(text_surface, (self.rect.x+10, self.rect.y+5))
        