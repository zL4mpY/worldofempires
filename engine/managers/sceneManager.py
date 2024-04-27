import os
import pygame

class SceneManager:
    def __init__(self):
        self.scenes: dict = {}
        self.current_state = None

    def add_scene(self, scene_name: str, scene):
        self.scenes[scene_name] = scene

    def switch_scene(self, new_scene_name: str):
        if new_scene_name in self.scenes:
            self.current_scene = self.scenes[new_scene_name]
            self.current_scene.start()
        else:
            print(f"Scene \'{new_scene_name}\' does not exist.")
        
    def get_scene(self, scene: str):
        if scene in self.scenes:
            return self.scenes[scene]
        else:
            print(f'Scene \'{scene}\' does not exist')
    
    def get_scenes(self, count: bool = False, printout: bool = False):
        if count:
            for i, scene in enumerate(list(self.scenes.keys)):
                if printout:
                    print(i, scene)
        
        else:
            for scene in list(self.scenes.keys):
                if printout:
                    print(scene)

        return list(self.scenes.keys)

    def update(self):
        if self.current_scene:
            self.current_scene.update()

    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)
            
        

class Scene:
    def __init__(self, game, name):
        self.game = game
        self.screen = self.game.screen
        
        self.settingsManager = self.game.settingsManager
        self.displayManager = self.game.displayManager
        self.sceneManager = self.game.sceneManager
        self.languageManager = self.game.languageManager
        self.eventManager = self.game.eventManager
        self.textManager = self.game.textManager
        self.imageManager = self.game.imageManager
        
        self.name = name
        
        self.start_time = pygame.time.get_ticks()
        
        '''
            Set your variables here
        '''
        
        pass

    def start(self):
        '''
            Starts the scene and initializes start events.
        '''
        
        pass
    
    def update(self):
        '''
            Update your variables here
        '''
        
        pass
    
    def handle_event(self, event):
        '''
            Handle your events here
        '''

        pass
    
    def render(self):
        '''
            Render your objects here
        '''
        
        pass