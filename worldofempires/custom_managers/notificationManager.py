from engine.managers.textManager import TextManager
import pygame

class NotificationManager():
    def __init__(self):
        self.notifications = []

    def add_notification(self, notification):
        self.notifications.append(notification)
    
    def remove_notification(self, notification):
        self.notifications.remove(notification)
    
    def render_notifications(self):
        for notification in self.notifications:
            if notification == None: self.notifications.remove(notification)
        
        for i, notification in enumerate(list(filter(lambda x: getattr(x, "side")=="lb", self.notifications))):
            x = 10
            y = notification.game.height - (10 + i * 25)
            notification.render(x, y)
        
        for i, notification in enumerate(list(filter(lambda x: getattr(x, "side")=="lt", self.notifications))):
            x = 10
            y = 10 + i * 25 - 15
            notification.render(x, y)
        
        for i, notification in enumerate(list(filter(lambda x: getattr(x, "side")=="rb", self.notifications))):
            x = notification.game.get_resolution()[0] - 20
            y = notification.game.height - (10 + i * 25)
            notification.render(x, y)
        
        for i, notification in enumerate(list(filter(lambda x: getattr(x, "side")=="rt", self.notifications))):
            x = notification.game.get_resolution()[0] - 20
            y = 10 + i * 25 - 15
            notification.render(x, y)
        
        for i, notification in enumerate(list(filter(lambda x: getattr(x, "side")=="cb", self.notifications))):
            x = notification.game.get_resolution()[0] / 2
            y = notification.game.height - (10 + i * 25)
            notification.render(x, y)
        
        for i, notification in enumerate(list(filter(lambda x: getattr(x, "side")=="ct", self.notifications))):
            x = notification.game.get_resolution()[0] / 2
            y = 10 + i * 25 - 15
            notification.render(x, y)

        for notification in self.notifications:
            if notification.time <= 0:
                self.notifications.remove(notification)
            
class Notification():
    """
    
    This is a notification class. 
    
    """
    def __init__(self, game, scene, text: str, time: int = 5, side='lb', align='left', color=(0, 0, 0), size=26):

        """
        
        The text parameter is the description of notification,
        the timer parameter is the time in seconds that the notification will be displayed.
        Side is where the notification will be rendered. Sides can be 'lb' (left bottom),
        'rb' (right bottom), 'lt' (left top) and 'rt' (right top).
        
        """
        
        
        self.game = game
        self.scene = scene
        
        self.textManager = self.game.textManager
        self.start_time = pygame.time.get_ticks()
        self.render_time = 0
        self.time = time * 1000
        self.side = side


        self.font = self.game.settingsManager.settings.get('font')
        self.text_color = color
        self.text = text
        self.size = size
        self.align = align
    
    def render(self, x, y):
        current_time = pygame.time.get_ticks()
        elapsed_time = current_time - self.start_time
        
        if elapsed_time < self.time:
            self.textManager.render(self.game.screen, x, y, self.text, self.font, self.text_color, self.size, self.side, self.align)
            self.render_time = pygame.time.get_ticks() - self.start_time
        
        else:
            self.time = 0