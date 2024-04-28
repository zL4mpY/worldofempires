import engine
import pygame

class Sidebar():
    def __init__(self, game, scene):
        self.game = game
        self.scene = scene
        self.screen = self.scene.screen
        
        self.menu = pygame.Surface((200, self.game.height))
        self.menu.set_alpha(255)
        self.menu.fill((255, 255, 255))
        self.rect = self.menu.get_rect()
        self.rect.x = self.game.width - 200
        
        self.devSurface = pygame.Surface((200, self.game.height))
        self.devSurface.set_alpha(64)
        self.devSurface.fill((0, 0, 255))
        
        self.devRect = pygame.Rect(self.rect.x, self.rect.y, 200, self.game.height)
        self.is_visible = False
        
        def show_hide():
            self.is_visible = False if self.is_visible == True else True
        
        from engine.classes.button import Button
        self.open_btn = Button(game=self.game,
                               scene=self.scene,
                               x=self.game.width, y=0,
                               width=50, height=20,
                               align="tr",
                               text="Menu",
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
        return self.objects[id]
    
    def update(self):
        if self.is_visible:
            for object in self.objects.values():
                from engine.classes.button import Button
                if isinstance(object, Button):
                    object.handle_event()
            
            object = self.get_object(2)
            if 0 < len(object.scene.chosen_countries) < len(object.scene.countries):
                object.change_text("Select all")
        
        self.open_btn.handle_event()
    
    def render(self):
        if self.is_visible:
            self.screen.blit(self.menu, (self.game.width - 200, 0))
            if self.game.is_devmode:
                self.screen.blit(self.devSurface, self.devRect)
        
            for object in self.objects.values():
                object.render()

        self.open_btn.render()
        
        