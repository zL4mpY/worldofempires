import pygame

class UIManager():
    def __init__(self, game, scene):
        self.game = game
        self.scene = scene
        self.objects = {}
    
        self.game.loggingManager.log(f'UIManager {{scene {self.scene.name}}} initialized!', 'INFO')
        
    def add_element(self, element, id):
        self.objects[id] = element
    
    def get_element(self, id):
        return self.objects[id]
    
    def update_ui(self):
        for object in list(self.objects.values()):
            object.update()
    
    def handle_event(self, event):
        for object in list(self.objects.values()):
            object.handle_event(event)
    
    def render_ui(self):
        for object in list(self.objects.values()):
            object.render()
        