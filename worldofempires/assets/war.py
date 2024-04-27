from engine.managers.textManager import TextManager
from worldofempires.assets.battle import Battle

class War:
    def __init__(self, game, scene, participants):
        self.game = game
        self.scene = scene
        
        self.participants = participants
        self.textRenderer = self.game.textManager
        self.battles = []  # список битв в рамках войны
        self.render_message = game.lang['warRenderMessage']
    
    def add_battle(self, battle: Battle):
        self.battles.append(battle)  # метод для добавления новой битвы в список
        
    def add_participant(self, participant):
        self.participants.append(participant)
    
    def render(self):
        if len(self.battles) > 0:
            self.textRenderer.render(self.game.screen, self.battles[0].place.x + 5, self.battles[0].place.y - 5, self.render_message, 'arialblack', (0,0,0), 9)
    
    def end(self):
        for country in self.participants:
            if self in country.wars:
                country.states['in_war'] = False
                country.states['return_to_homeland'] = True
                country.wars.remove(self)
        
        for country in self.participants:
            for country1 in self.participants:
                if country != country1:
                    country.agression[country1] = 0.0
        
        if self in self.scene.wars:
            self.scene.wars.remove(self)
    
    def __repr__(self):
        return f'War ({self.participants[0].name} VS {self.participants[1].name})'