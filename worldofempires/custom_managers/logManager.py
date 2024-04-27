import time

class Log():
    """
    
        A basic event that can be used in logs manager.
    
    """
    def __init__(self, description):
        self.description = description
        self.time = time.time()

        total_seconds = round(self.time, 0)

        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        if len(str(hours)) < 2:
            hours = '0' + str(hours)
        if len(str(minutes)) < 2:
            minutes = '0' + str(minutes)
        if len(str(seconds)) < 2:
            seconds = '0' + str(seconds)


        self.time = f"{hours}:{minutes}:{seconds}"
    
    def __repr__(self):
        return f"{time.strftime('%H:%M:%S', self.time)}: {self.description}\n"

class LogsManager():
    """
    
        Save your in-game events using Log Manager.
        
    """
    def __init__(self):
        self.logs = []
    
    def add_log(self, event: Log) -> None:
        """
        
            Adds event to logs list of your log manager.
        
        """
        
        self.logs.append(event)
    
    def remove_log(self, event: Log | int) -> None:
        if isinstance(event, int):
            self.logs.pop(event)
            return
        
        self.logs.remove(event)
        return
        
        