class Partnership:
    def __init__(self, game, scene):
        self.game = game
        self.scene = scene
        
        self.partners = []
    
    def add_partner(self, partner):
        self.partners.append(partner)
    
    def remove_partner(self, partner):
        self.partners.remove(partner)
    
    def destroy(self):
        self.scene.partnerships.remove(self)
        del self
    
    def __repr__(self):
        return f'Partnership of {", ".join(self.partners)}'