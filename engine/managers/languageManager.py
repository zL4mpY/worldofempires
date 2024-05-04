from pathlib import Path
import json

class LanguageManager:
    def __init__(self, game):
        self.game = game
        self.language = None
        
        self.game.loggingManager.log(f'LanguageManager initialized!', 'INFO')
    
    def load_language(self, path: str | Path) -> dict:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        self.game.loggingManager.log(f'Loaded .lang file from {path}!', 'INFO')
        return data

    def get_language(self) -> str:
        return self.language