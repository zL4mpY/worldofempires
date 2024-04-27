from worldofempires.scenes.main_game import GameScene
from worldofempires.scenes.main_menu import MenuScene
from worldofempires.scenes.loading_screen import LoadingScene
from worldofempires.scenes.game_process_settings_menu import GameProcessSettingsMenuScene
import engine
import pygame

BASE_DIR = engine.get_base_dir()

class Game(engine.LumixGame):
    def __init__(self):
        super().__init__()
 
        self.settingsManager.load_settings(path="settings.json")
        self.is_devmode = self.settingsManager.get("dev_mode")

        self.set_resolution(self.settingsManager.get_resolution())
        self.fps = self.settingsManager.get_fps()
        self.fullscreen = self.settingsManager.get('fullscreen')
        
        if not self.fullscreen:
            self.set_screen(size=self.get_resolution(), fullscreen=self.fullscreen, max_fps=self.fps)
            self.width, self.height = self.settingsManager.get_resolution()
        else:
            self.set_screen(size=self.displayManager.get_resolution(), fullscreen=self.fullscreen, max_fps=self.fps)
            self.width, self.height = self.displayManager.get_resolution()
        
        self.lang = self.languageManager.load_language(path=BASE_DIR / "worldofempires" / "lang" / f"{self.settingsManager.settings['language']}.lang")
        self.set_title("World of Empires")
        
        icon = pygame.image.load(BASE_DIR / 'icon.ico')
        self.set_icon(icon)
        

        # LOADING SCENES

        self.sceneManager.add_scene("game_process", GameScene(self, "game_process"))
        self.sceneManager.add_scene("game_process_settings_menu", GameProcessSettingsMenuScene(self, "game_process_settings_menu"))
        self.sceneManager.add_scene("loading_screen", LoadingScene(self, "loading_screen", None))
        self.sceneManager.add_scene("menu", MenuScene(self, "menu"))
        
        self.sceneManager.switch_scene('menu')
        self.eventManager.add_keyboard_event('F11', self.set_fullscreen)
        
        self.is_running = True
    
    def set_fullscreen(self):
        if not self.settingsManager.get('fullscreen'):
            self.settingsManager.set('fullscreen', True)
        else: self.settingsManager.set('fullscreen', False)
        self.settingsManager.save_settings()
        
        self.restart()

    def run(self) -> None:
        super().run()

if __name__ == '__main__':
    Game().run()