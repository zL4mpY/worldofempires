import win32.win32api as win32api

class DisplayManager():
    """
    
        This manager can be used to get your screen size or refresh rate.
    
    """
    
    def __init__(self):
        pass
    
    def get_refresh_rate(self) -> int:
        """
        
            Returns a refresh rate of your monitor.
        
        """
        
        device = win32api.EnumDisplayDevices()
        settings = win32api.EnumDisplaySettings(device.DeviceName, -1)
        return getattr(settings, 'DisplayFrequency')

    def get_width(self) -> int:
        """
        
            Returns a screen width of your monitor.
        
        """
        
        return win32api.GetSystemMetrics(0)

    def get_height(self) -> int:
        """
        
            Returns a screen height of your monitor.
        
        """
        
        return win32api.GetSystemMetrics(1)

    def get_resolution(self) -> tuple[int]:
        """
        
            Returns a screen size of your monitor.
        
        """
        
        return (self.get_width(), self.get_height())