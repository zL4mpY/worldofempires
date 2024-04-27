class Place():
    def __init__(self, game, scene, x, y):
        self.game = game
        self.scene = scene
        
        self.x, self.y = x, y
        self.size = self.scene.cell_size