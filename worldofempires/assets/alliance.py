class Alliance:
    def __init__(self, game, scene, name, territory_color, color):
        self.game = game
        self.scene = scene
        
        self.name = name
        self.allies = []
        self.total_territory = []
        self.territory_color = territory_color
        self.color = color
    
    def add_territory(self, territory):
        if territory in self.total_territory:
            territory.color = self.territory_color
            return
        
        territory.color = self.territory_color
        self.total_territory.append(territory)
    
    def remove_territory(self, territory):
        if not territory in self.total_territory:
            return
        
        self.total_territory.remove(territory)
        territory.color = territory.country.territory_color
    
    def add_ally(self, ally):
        self.allies.append(ally)
    
    def remove_ally(self, ally):
        self.allies.remove(ally)
    
    def render(self):
        for land in self.total_territory:
            land.render()
    
    def destroy(self):
        self.scene.alliances.remove(self)
        del self
    
    def __repr__(self):
        return f'Alliance {self.name}'