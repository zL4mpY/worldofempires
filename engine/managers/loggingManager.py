import os, pathlib

class LoggingManager():
    def __init__(self, game):
        self.game = game
        
        self.logs = ""
        self.levels = ['INFO', 'DEBUG', 'WARN', 'ERROR']
        self.log(f'LoggingManager successfully initialized!', 'INFO')
    
    def log(self, message, level="DEBUG"):
        self.logs += f"[{level}] {message}\n"
        
    def save_logs(self):
        from engine import get_base_dir
        from datetime import datetime
        
        log_file_name = f"log-{datetime.strftime(datetime.now(), '%d-%m-%Y-%H-%m-%S')}"
        log_file = log_file_name + ".txt"
        
        if not os.path.isdir(get_base_dir() / "logs"):
            os.mkdir(get_base_dir() / "logs")
        
        with open(get_base_dir() / "logs" / log_file, "a") as log_file:
            for log in self.logs.split('\n')[:-1]:
                log_file.write(f'{log}\n')
            
            log_file.write(f'[INFO] Successfully saved logs to file {log_file_name}.txt')

    def get_logs(self):
        return self.logs