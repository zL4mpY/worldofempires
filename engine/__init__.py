from engine.managers.settingsManager import SettingsManager
from engine.managers.sceneManager import SceneManager
from engine.managers.languageManager import LanguageManager
from engine.managers.imageManager import ImageManager
from engine.managers.textManager import TextManager
from engine.managers.eventManager import EventManager, Event, get_pygame_key
from engine.managers.displayManager import DisplayManager
from engine.managers.loggingManager import LoggingManager
from engine.managers.cameraManager import CameraManager

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

def get_align(align: str) -> str:
    if align == "c" or align == "center":
        align = 'center'
    elif align == 't' or align == "top":
        align = 'top'
    elif align == 'b' or align == "bottom":
        align = 'bottom'
    elif align == 'l' or align == "left":
        align = 'left'
    elif align == 'r' or align == "right":
        align = 'right'
    elif align == 'tl' or align == "topleft":
        align = 'topleft'
    elif align == 'tr' or align == "topright":
        align = 'topright'
    elif align == 'bl' or align == "bottomleft":
        align = 'bottomleft'
    elif align == 'br' or align == "bottomright":
        align = 'bottomright'
    elif align == 'cl' or align == "centerleft":
        align = 'centerleft'
    elif align == 'cr' or align == "centerright":
        align = 'centerright'
    else:
        align = 'center'
    return align

def set_align_add(align, rect, add_x, add_y, x, y):
    if align == 'left':
        setattr(rect, align, x-add_x)
    
    elif align == 'right':
        setattr(rect, align, x+add_x)
        
    elif align == 'top':
        setattr(rect, align, y-add_y)
    
    elif align == 'bottom':
        setattr(rect, align, y-add_y*3)
        
    elif align == 'center':
        setattr(rect, align, (x-add_x, y-add_y*2))
    
    elif align == 'centerleft':
        setattr(rect, "center", (x-add_x, y-add_y*2))
        setattr(rect, "left", x-add_x)
    
    elif align == 'centerright':
        setattr(rect, "center", (x+add_x, y+add_y*2))
        setattr(rect, "left", x+add_x)
    
    elif align == 'topleft':
        setattr(rect, align, (x-add_x, y-add_y))
    
    elif align == 'topright':
        setattr(rect, align, (x+add_x, y-add_y))
    
    elif align == 'bottomleft':
        setattr(rect, align, (x-add_x, y-add_y*3))
    
    elif align == 'bottomright':
        setattr(rect, align, (x+add_x, y-add_y*3))
    
    return (rect.x, rect.y)

def set_align(align, rect, x, y):
    if align in ['topleft', 'topright', 'bottomleft', 'bottomright', 'center']:
        setattr(rect, align, (x, y))
    elif align in ['top', 'bottom']:
        setattr(rect, align, y)
    elif align in ['left', 'right']:
        setattr(rect, align, x)
    elif align in 'centerleft':
        setattr(rect, 'center', (x, y))
        setattr(rect, 'left', x)
    elif align in 'centerright':
        setattr(rect, 'center', (x, y))
        setattr(rect, 'right', x)
    
    return (rect.x, rect.y)

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
        
        self.loggingManager = LoggingManager(self)
        self.loggingManager.log("LoggingManager initialized!", "INFO")
        
        pygame.init()
        
        self.loggingManager.log("Pygame initialized!", "INFO")
        
        traceback_gui.set_hook()
        
        self.loggingManager.log("Custom traceback hook set!", "INFO")
        
        self.engineSettings = SettingsManager(self).load_settings(BASE_DIR / "engine" / ".settings")
        
        self.loggingManager.log("Loaded engine settings!", "INFO")
        
        self.fill_color = self.engineSettings.get("fill-color")
        self.game_speed = 1
        
        self.loggingManager.log("Default screen fill color set!", "INFO")
        
        self.settingsManager = SettingsManager(self)
        self.displayManager = DisplayManager(self)
        self.sceneManager = SceneManager(self)
        self.languageManager = LanguageManager(self)
        self.eventManager = EventManager(self)
        self.textManager = TextManager(self)
        self.imageManager = ImageManager(self)

        self.dt = 0
        self.loggingManager.log("Default deltatime set to 0!", "INFO")
        
        self.fps = self.displayManager.get_refresh_rate()
        
        self.loggingManager.log("Default FPS set to user's refresh rate!", "INFO")
        
        self.resolution = self.displayManager.get_resolution()
        
        self.loggingManager.log("Default resolution set to user's screen resolution!", "INFO")
        
        self.width, self.height = self.resolution
        
        self.loggingManager.log("Default width and height set to user's screen resolution!", "INFO")
        
        self.fullscreen = False
        self.loggingManager.log("Fullscreen state set to False!", "INFO")
        
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" %(0, self.height // 5 - self.height // 15)
        self.loggingManager.log("Set program's default place on screen!", "INFO")
        
        self.screen = pygame.display.set_mode(size=self.resolution, flags=0)
        self.loggingManager.log("Screen initialized!", "INFO")
        
        self.clock = pygame.time.Clock()
        self.loggingManager.log("Clock initialized!", "INFO")
        
        self.title = "Lumix.py project"
        self.loggingManager.log(f"Default title set to {self.title}!", "INFO")
        
        self.icon = None
        self.loggingManager.log(f"Default icon set to {self.icon}!", "INFO")
        
        pygame.display.set_caption(self.title)
        self.loggingManager.log(f"Pygame title set to {self.title}!", "INFO")
        
        self.eventManager.set_start_time(time=time.time())
        self.loggingManager.log(f"Set start time to {self.eventManager.get_start_time()}!", "INFO")
        
        self.is_running = True
        self.loggingManager.log(f"Set program as running!", "INFO")
    
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
            self.screen.fill(self.fill_color)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

                if event.type == pygame.KEYDOWN:
                    for custom_event in self.eventManager.get_keyboard_events():
                        if event.key == get_pygame_key(custom_event.key):
                            custom_event.run()

                current_scene.handle_event(event)
            current_scene.eventManager.run_events()

            current_scene.update()
            current_scene.render()

            pygame.display.flip()
            dt = self.clock.tick(self.fps * self.game_speed * 2) / 1000
            self.dt = dt
        
        self.loggingManager.save_logs()
            
    
    def exit(self):
        self.is_running = False
    
    def restart(self):
        self.loggingManager.log("The game has restarted!", "INFO")
        self.__init__()