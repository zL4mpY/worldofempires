from engine.managers.settingsManager import SettingsManager
from engine.managers.sceneManager import SceneManager
from engine.managers.languageManager import LanguageManager
from engine.managers.imageManager import ImageManager
from engine.managers.textManager import TextManager
from engine.managers.eventManager import EventManager, Event, get_pygame_key
from engine.managers.displayManager import DisplayManager
# from engine.managers.crashManager import CrashManager

from pathlib import Path
import pygame
import time
import os
import sys
import engine.classes.traceback_gui as traceback_gui

def get_base_dir():
    if getattr(sys, 'frozen', False):
        return Path(os.path.abspath(os.path.dirname(sys.executable)))
    elif __file__:
        return Path(os.path.abspath(os.path.dirname(__file__))).resolve().parent
    
BASE_DIR = get_base_dir()

def in_dict(item, dict):
    for key in list(dict.keys()):
        if key == item:
            return True
    return False

class BaseObject():
    """

            This is a basic Lumix object.
            
    """
    
    def __init__(self, game, scene, x, y):
        self.game = game
        self.scene = scene
        self.x = x
        self.y = y
        self.screen = self.game.screen
    
    def render(self):
        """

            Render your object here
            
        """
        
        pass

class LumixGame():
    """
    
        This is a basic class for a game. Recommended to use.
    
    """
    
    def __init__(self):
        """
        
            Initializes your game, its functions and other things.
        
        """
        
        pygame.init()
        traceback_gui.set_hook()
        
        self.engineSettings = SettingsManager().load_settings(BASE_DIR / "engine" / ".settings")
        self.fill_color = self.engineSettings.get("fill-color")
        
        self.settingsManager = SettingsManager()
        self.displayManager = DisplayManager()
        self.sceneManager = SceneManager()
        self.languageManager = LanguageManager()
        self.eventManager = EventManager()
        self.textManager = TextManager(self)
        self.imageManager = ImageManager(self)
        # self.crashManager = CrashManager(self)
        self.dt = 0
        
        self.fps = self.displayManager.get_refresh_rate()
        self.resolution = self.displayManager.get_resolution()
        self.width, self.height = self.resolution
        
        self.fullscreen = False
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(0, self.height // 5 - self.height // 15)
        self.screen = pygame.display.set_mode(size=self.resolution, flags=0)
        self.clock = pygame.time.Clock()
        self.title = "Lumix.py project"
        self.icon = None
        
        pygame.display.set_caption(self.title)
        
        self.eventManager.set_start_time(time=time.time())
        self.is_running = True
    
    def set_screen(self, size: tuple[int] | list[int], fullscreen: bool = False, max_fps: int = 60) -> None:
        """
        
            Sets your screen settings for your game.
        
        """
        fullscreen = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE if fullscreen else pygame.DOUBLEBUF | pygame.HWSURFACE
        self.fullscreen = True if fullscreen else False
        size = list(size)
        size[0] = size[0] - 10 if size[0] == self.displayManager.get_width() else size[0]
        size = tuple(size)
        
        self.screen = pygame.display.set_mode(size=size, flags=fullscreen)
        self.fps = max_fps
    
    def set_title(self, title: str = "Lumix.py project") -> None:
        """
        
            Changes the title of your game's window.
        
        """
        self.title = title
        pygame.display.set_caption(self.title)
    
    def set_icon(self, icon) -> None:
        self.icon = icon
        pygame.display.set_icon(icon)
    
    def get_fullscreen(self) -> bool:
        return self.fullscreen
    
    def get_resolution(self) -> tuple[int]:
        return self.resolution

    def set_resolution(self, resolution: tuple) -> None:
        self.resolution = resolution
        self.width, self.height = self.resolution
        
    def run(self) -> None:
        """
        
            Runs your game.
        
        """
        
        while self.is_running:
            current_scene = self.sceneManager.current_scene

            # self.screen.fill(self.fill_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.KEYDOWN:
                    for custom_event in self.eventManager.get_keyboard_events():
                        if event.key == get_pygame_key(custom_event.key):
                            custom_event.run()

                current_scene.handle_event(event)

            current_scene.update()
            current_scene.render()

            pygame.display.flip()
            dt = self.clock.tick(self.fps) / 1000
            self.dt = dt
            
    
    def exit(self):
        self.is_running = False
    
    def restart(self):
        self.__init__()