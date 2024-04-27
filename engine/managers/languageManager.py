from pathlib import Path
import json

class LanguageManager:
    def __init__(self):
        self.language = None
    
    def load_language(self, path: str | Path) -> dict:
        with open(path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        return data

    def get_language(self) -> str:
        return self.language