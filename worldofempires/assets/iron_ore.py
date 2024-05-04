from engine import BaseObject, get_base_dir
import pygame
import random

iron_ore_texture = pygame.image.load(get_base_dir() / "worldofempires" / "textures" / "iron_ore.png", "")
width = iron_ore_texture.get_width()
height = iron_ore_texture.get_height()

class IronOre(BaseObject):
    def __init__(self, game, scene, x, y):
        super().__init__(game, scene, x, y)
        
        new_width = int(width * self.scene.terrain.zoom / 100) * 4
        new_height = int(height * self.scene.terrain.zoom / 100) * 4
        
        self.surface = pygame.transform.scale(iron_ore_texture, (new_width, new_height))
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = x, y
        
        self.camerarect = self.surface.get_rect()
        self.camerarect.x, self.camerarect.y = x, y
        
        self.amount = random.randint(1, 5)
        self.durability = 65
        
    def render(self, add_x=0, add_y=0):
        self.screen.blit(self.surface, (self.rect.x + add_x, self.rect.y + add_y))
        self.camerarect.x = self.rect.x + add_x
        self.camerarect.y = self.rect.y + add_y
    
    def destroy(self, destroyer):
        destroyer.inventory.add_item(3, self.amount)
        destroyer.homeland.inventory.add_item(3, self.amount)
        destroyer.country.inventory.add_item(3, self.amount)
        destroyer.temp_states['mine_object'] = None
        destroyer.temp_states['mined_resources'] += 1
        
        if self in self.scene.resources:
            self.scene.resources.remove(self)
        del self