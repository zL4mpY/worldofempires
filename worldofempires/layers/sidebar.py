import engine
import pygame

class Sidebar():
    def __init__(self, game, scene, side='right'):
        self.game = game
        self.scene = scene
        self.screen = self.scene.screen
        
        self.width = 200
        self.height = self.game.height
        
        match side:
            case 'right':
                x = self.game.width - self.width
                y = 0
            case 'left':
                x = 0
                y = 0
            case 'bottom':
                x = 0
                self.height = 200
                self.width = self.game.width
                y = self.game.height - self.height
            case 'top':
                x = 0
                self.height = 200
                self.width = self.game.width
                y = 0 + self.height
        
        self.menu = pygame.Surface((self.width, self.height))
        self.menu.set_alpha(255)
        self.menu.fill((255, 255, 255))
        
        self.rect = self.menu.get_rect()
        self.rect.x, self.rect.y = x, y
        
        self.devSurface = pygame.Surface((200, self.height))
        self.devSurface.set_alpha(64)
        self.devSurface.fill((0, 0, 255))
        
        self.devRect = pygame.Rect(x, y, 200, self.height)
        self.is_visible = False
        
        def show_hide():
            self.is_visible = False if self.is_visible == True else True
            
        match side:
            case 'left':
                open_btn_x = 50
                open_btn_y = 0
            case 'right':
                open_btn_x = self.game.width
                open_btn_y = 0
            case 'bottom':
                open_btn_x = 50
                open_btn_y = self.game.height - 20
            case 'top':
                open_btn_x = 50
                open_btn_y = 0
        
        from engine.classes.button import Button
        self.open_btn = Button(game=self.game,
                               scene=self.scene,
                               x=open_btn_x, y=open_btn_y,
                               width=50, height=20,
                               align="tr",
                               text=self.game.lang.get('menu'),
                               onclick=show_hide,
                               fontsize=14,
                               color=(0, 0, 0),
                               normalcolor=(255, 255, 255),
                               normaltransparency=128,
                               hovercolor=(220, 220, 220),
                               hovertransparency=128,
                               pressedcolor=(190, 190, 190),
                               pressedtransparency=128)
        self.objects = {}
    
    def add_object(self, object, id):
        self.objects[id] = object
    
    def get_object(self, id):
        if engine.in_dict(id, self.objects):
            return self.objects[id]
        return None
    
    def update(self):
        if self.is_visible:
            for object in self.objects.values():
                from engine.classes.button import Button
                if isinstance(object, Button):
                    object.update()
            
            # object = self.get_object(2)
            
            # if object != None:
            #     if 0 < len(object.scene.chosen_countries) < len(object.scene.countries):
            #         object.change_text("Select all")
        
        self.open_btn.update()
    
    def render(self):
        if self.is_visible:
            self.screen.blit(self.menu, (self.rect.x, 0))
            if self.game.is_devmode:
                self.screen.blit(self.devSurface, self.devRect)
        
            for object in self.objects.values():
                object.render()

        self.open_btn.render()
        
        