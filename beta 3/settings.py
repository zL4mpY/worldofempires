# [ SETTINGS ]

class Settings:
    def __init__(self):
        self.settings = {
            'language': 'ru',
            'fullscreen': False,
            'resolution': (800, 600),
            'max_FPS': 15,
            'play_as_country': False,
            'font': 'arialblack',

            'countries': {
                'play_as_country': False,
                'min_countries': 2,
                'max_countries': 6
            },

            'auto_spawn': {
                'humans': {
                    'enabled': True,
                    'spawn_chance': 25
                },
                'countries': {
                    'enabled': True,
                    'spawn_chance': 30
                }
            }
        }
    
    def getResolution(self):
        return self.settings['resolution']

    def getMaxFPS(self):
        return self.settings['max_FPS']
