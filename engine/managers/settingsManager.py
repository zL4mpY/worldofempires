# [ SETTINGS ]

from pathlib import Path
import json

class SettingsManager:
    def __init__(self, game):
        self.game = game
        
        self.settings: dict
        self.file_path = None
        
        self.game.loggingManager.log(f'SettingsManager initialized!', 'INFO')
    
    def get(self, key):
        return self.settings[key]
    
    def set(self, key, value):
        self.settings[key] = value
    
    def get_resolution(self) -> tuple:
        width, height = self.settings['resolution'].split("x")
        width, height = int(width), int(height)

        resolution: tuple = (width, height)

        return resolution

    def get_width(self) -> int:
        width: int = self.settings['resolution'].split("x")[0]

        return width

    def get_height(self) -> int:
        height: int = self.settings['resolution'].split("x")[1]

        return height

    def get_fps(self) -> int:
        return self.settings['max_fps']
    
    def load_settings(self, path: str | Path) -> dict:        
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        self.settings = data
        self.file_path = path
        return data
    
    def save_settings(self):
        with open(self.file_path, 'w') as f:
            json.dump(self.settings, f, indent=4)
