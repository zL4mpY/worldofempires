import engine
import pygame
import random
import math

from ..custom_managers.logManager import Log
from ..custom_managers.notificationManager import Notification
from .king import King

def distance(point1, point2):
    result = math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)
    return result

hard_to_walk = [(50, 89, 38), (80, 143, 61), (22, 156, 233), (45, 166, 235)]
original_step_size = 4

available_resources = ["Tree", "Stone", "IronOre", "SilverOre", "GoldOre"]

class Human(engine.BaseObject):
    def __init__(self, game, scene, x, y, country, homeland):
        super().__init__(game, scene, x, y)
        
        self.country = country
        # self.color = self.country.color
        self.color = (255, 255, 255)
        self.size = 2
        
        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = x,y
        self.camerarect = self.surface.get_rect()
        self.camerarect.x, self.camerarect.y = x,y
        
        self.step = original_step_size

        self.homeland = homeland

        self.hp = 150
        self.max_hp = 150
        self.regen_size = {'min': round(random.uniform(0.05, 2), 2), 'max': round(random.uniform(2, 10), 2)}
        self.damage = {'min': round(random.uniform(0, 0.5), 1), 'max': round(random.uniform(0.5, 5), 1)}

        self.states = {'current_war': None,
                       'current_battle': None,
                       'return_to_homeland': False,
                       'is_mining_resources': False,
                       'can_mine_resources': False}
        
        self.temp_states = {}
        def allow_mine_resources():
            self.states['can_mine_resources'] = True

        self.scene.eventManager.create_event(allow_mine_resources, 10)

        self.watch_radius = 25.0
        self.watch_radius_rect = pygame.Rect(self.rect.x - self.watch_radius, self.rect.y - self.watch_radius, self.watch_radius * 2, self.watch_radius * 2)
        
        self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        from ..custom_managers.inventoryManager import Inventory
        self.inventory = Inventory(self, [])
    
    def render(self, add_x=0, add_y=0):
        self.screen.blit(self.surface, (self.rect.x + add_x, self.rect.y + add_y))
        self.camerarect.x = self.rect.x + add_x
        self.camerarect.y = self.rect.y + add_y
    
    def act_war(self):
        war = self.states['current_war']
        current_battle = self.states['current_battle']

        if self._move_to(current_battle.city.rect):

            enemies = self.find_enemies()
            # print(f'Human from {self.country} found {len(enemies)} enemies')

            if len(enemies) > 0:
                chosen_enemy = enemies[0]
                if not ('war_enemy_country' in self.temp_states) and not (chosen_enemy.country == self.country):
                    self.temp_states['war_enemy_country'] = chosen_enemy.country

                self.attack(chosen_enemy)

                if chosen_enemy.hp <= 0:
                    chosen_enemy.destroy()

            else:
                if engine.in_dict('war_enemy_country', self.temp_states):
                    enemy_country = self.temp_states['war_enemy_country']
                else:
                    enemy_country = None

                if enemy_country != None and enemy_country!= self.country:
                    # print(enemy_country.get_people_in_war(battle=current_battle))
                    if enemy_country.get_people_in_war(battle=current_battle) <= 0:
                        if enemy_country == current_battle.participants[0]:
                            # if current_battle.city in self.country.cities:
                            self.country.defended_from_enemy(war, current_battle, enemy_country)
                        else:
                            if len(enemy_country.cities) > 0:
                                enemy_country.destroy_city(current_battle.city, self.country)
                            else:
                                enemy_country.destroy(self.country)
            
                # print(f'[DEBUG] {self.country} Human: {enemy_country=}')
            
            if "war_enemy_country" in self.temp_states:
                pass
                # print(f'[DEBUG] {self.country} Human: {self.temp_states["war_enemy_country"]=}')
    
    def mine_resources(self):
        closest_object = None
        closest_distance = 80
        
        if self.temp_states["mined_resources"] >= self.temp_states["mine_goal"]:
            self.states['is_mining_resources'] = False
            self.states['return_to_homeland'] = True
            self.states['can_mine_resources'] = False
            
            def can_mine_res(): self.states['can_mine_resources'] = True
            self.scene.eventManager.create_event(can_mine_res, random.randrange(60,120,15))

        if not "mine_object" in self.temp_states:
            self.temp_states["mine_object"] = None
        
        if self.temp_states['mine_object'] == None:
            for resource in list(filter(lambda res: res.__class__.__name__==self.temp_states['resource_mine_type'], self.scene.resources)):
                distance_to_object = distance(self, resource)
                if distance_to_object < closest_distance:
                    closest_object = resource
                    self.temp_states['mine_object'] = closest_object
                    closest_distance = distance_to_object

        if self.temp_states['mine_object'] != None:
            if self._move_to(self.temp_states['mine_object'].rect):
                self.mine_resource(self.temp_states['mine_object'])
        else:
            if not 'mine_object_found_fail_times' in self.temp_states:
                self.temp_states['mine_object_found_fail_times'] = 0
                
            self.temp_states['mine_object_found_fail_times'] += 1
            
            if self.temp_states['mine_object_found_fail_times'] > 10:
                self.states['is_mining_resources'] = False
                self.states['return_to_homeland'] = True
                self.states['can_mine_resources'] = False
                
                def can_mine_res(): self.states['can_mine_resources'] = True
                self.scene.eventManager.create_event(can_mine_res, random.randrange(60,120,15))
    
    def mine_resource(self, resource):
        if self.temp_states['can_break']:
            if not resource.durability <= 0:
                resource.durability -= random.randint(1, 4)
            else:
                resource.destroy(self)
            self.temp_states['can_break'] = False
            
            def make_breakable():
                self.temp_states['can_break'] = True

            self.scene.eventManager.create_event(make_breakable, 0.4)
                
    def act(self):
        if self.states['current_war'] != None:
            self.act_war()
            return
        
        elif self.states['is_mining_resources']:
            self.mine_resources()
            return
        
        else:
            if self.states['return_to_homeland']:
                if self._move_to_zone(self.homeland):
                    self.states['return_to_homeland'] = False
                return
            
            actions, chances = ["move", "create_city", "mine_resources"], [95 * self.game.game_speed, round(1 / self.game.fps * self.game.game_speed, 3), round(4 / self.game.fps * self.game.game_speed, 3)]
            action = random.choices(actions, chances, k=1)[0]

            match action:
                case "move":
                    self.move()
                    
                case "create_city":
                    if not self.states['is_mining_resources'] and not self.states['return_to_homeland']:
                        all_distances_above_80 = all([distance(self.rect, city) >= 80 for city in self.scene.cities])

                        if all_distances_above_80:
                            from .city import City
                            city = City(self.game, self.scene, self.rect.x, self.rect.y, self.country, False)
                            message = self.game.lang['onCityFound']

                            self.scene.notificationManager.add_notification(Notification(self.game, self.scene, message.format(self.country.name)))
                            self.scene.events.append(Log(message.format(self.country.name)))
                            self.country.cities.append(city)
                            self.scene.cities.append(city)

                            self.move()
                
                case "mine_resources":
                    if self.states['can_mine_resources']:
                    
                        humans_mining = 0

                        for human in self.country.humans:
                            if human.states['is_mining_resources']:
                                humans_mining += 1

                            if humans_mining >= 3:
                                self.move()
                                break
                            
                        if self.country.king.states['is_mining_resources']: humans_mining += 1

                        if not humans_mining >= 3:
                            random_resource = random.choice(available_resources)
                            self.states['is_mining_resources'] = not self.states['is_mining_resources']
                            self.states['can_mine_resources'] = True
                            self.temp_states["mine_goal"] = random.randrange(1, 8, 1)
                            self.temp_states["mined_resources"] = 0
                            self.temp_states['resource_mine_type'] = random_resource
                            self.temp_states['can_break'] = True

                case _:
                    self.move()
            
            if self.hp < self.max_hp:
                self.hp += round(random.uniform(self.regen_size['min'], self.regen_size['max']), 2)
                self.hp = self.max_hp if self.hp > self.max_hp else self.hp

    def can_move(self, pos):
        if pos.x < 0 or pos.x + self.rect.width > self.scene.terrain.width:
            return False  # Check if the position is outside the screen
        if pos.y < 0 or pos.y + self.rect.height > self.scene.terrain.height:
            return False  # Check if the position is outside the screen
        terrain_color = self.scene.terrain.get_at((pos.x, pos.y))  # Get the terrain color at the new position
        
        if terrain_color != None:
            if terrain_color == (68, 176, 238):
                return False  # Check if the new position is on water
            if terrain_color == (58, 29, 19) or terrain_color == (92, 61, 61) or terrain_color == (245, 240, 240):
                return False # Check if the new position is on mountains
        
        return True
    
    def move(self):
        state = True
        if not self.country.is_claimed_territory(self.rect.x, self.rect.y):
            if self.country.is_on_enemy_territory(self.rect.x, self.rect.y):
                for country in self.scene.countries:
                    if country != self.country and country.is_claimed_territory(self.rect.x, self.rect.y):
                        if not self.country.allied_with(country):
                            if len(self.country.alliances) > 0:
                                for alliance in self.country.alliances:
                                    for ally in alliance.allies:
                                        if ally.allied_with(country):
                                            state = False
                            
                            if state:
                                country.remove_territory(self.rect.x, self.rect.y)
                                found = False

                                if len(country.agression) > 0:
                                    if engine.in_dict(self.country, country.agression):
                                        found = True
                                else:
                                    country.agression[self.country] = 0.0
                                    found = True

                                if found:
                                    country.agression[self.country] += float(random.randint(0, 10))
                                    country.agression[self.country] = 100.0 if country.agression[self.country] > 100.0 else country.agression[self.country]
                                # country.declare_war(self)
                                # pass
            
            else:
                if state:
                    self.country.claim_territory(self.rect.x, self.rect.y)
                    if len(self.country.alliances) > 0:
                        for alliance in self.country.alliances:
                            alliance.add_territory(self.country.territory[-1])

        terrain_color = self.scene.terrain.get_at((self.rect.x, self.rect.y))
        if terrain_color in hard_to_walk:
            self.step = original_step_size - 1
        else:
            self.step = original_step_size

        direction = random.choice(self.directions)
        new_x = math.ceil(direction[0] * self.step * self.game.game_speed * self.game.dt) if direction[0] > 0 else math.floor(direction[0] * self.step * self.game.game_speed * self.game.dt)
        new_y = math.ceil(direction[1] * self.step * self.game.game_speed * self.game.dt) if direction[1] > 0 else math.floor(direction[1] * self.step * self.game.game_speed * self.game.dt)
        
        new_pos = self.rect.move(new_x, new_y)  # Calculate the new position
        if self.can_move(new_pos):  # Check if the new position is valid
            self.rect = new_pos  # Update the position
    
    def find_enemies(self):
        enemies = []

        for country in self.scene.countries:
            if country != self.country:
                for human in list(filter(lambda x: isinstance(x, Human)==True, country.humans)):
                    if (human.states['current_war'] == self.states['current_war'] and
                        human.states['current_battle'] == self.states['current_battle']):
                    
                        if (abs(human.rect.x - self.rect.x) < self.scene.land_cell_size and
                            abs(human.rect.y - self.rect.y) < self.scene.land_cell_size):
                            enemies.append(human)

        return enemies

    def is_in_territory(self, territory):
        zone_x = (territory.x // self.scene.land_cell_size) * self.scene.land_cell_size
        zone_y = (territory.y // self.scene.land_cell_size) * self.scene.land_cell_size

        if zone_x <= self.rect.x <= zone_x + self.scene.land_cell_size and zone_y <= self.rect.y <= zone_y + self.scene.land_cell_size:
            return True
        
        return False
    
    def move_to_zone(self, rect):
        if self.is_in_territory(rect):
            return True

        center1 = ((self.rect.x + self.size) / 2, (self.rect.y + self.size) / 2)
        center2 = ((rect.x + rect.size) / 2, (rect.y + rect.size) / 2)

        dx = center2[0] - center1[0]
        dy = center2[1] - center1[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > self.step:
            scale = min(self.step, distance) / distance
            dx *= scale
            dy *= scale

        self.rect.x = self.rect.x + dx
        self.rect.y = self.rect.y + dy
        self.rect.x = round(self.rect.x / self.step) * self.step
        self.rect.y = round(self.rect.y / self.step) * self.step
    
    def _move_to_zone(self, rect):
        if self.is_in_territory(rect):
            return True

        pos_a = pygame.Vector2(self.rect.x, self.rect.y)
        pos_b = pygame.Vector2(rect.rect.x, rect.rect.y)
        
        terrain_color = self.scene.terrain.get_at((self.rect.x, self.rect.y))
        if terrain_color in hard_to_walk:
            self.step = original_step_size - 1
        else:
            self.step = original_step_size
        
        vel = self.step * self.game.dt * self.game.game_speed
        vel = math.ceil(vel)
        
        # print(f'[DEBUG] HUMAN from {self.country} (1): {pos_a=}, {pos_b=}, {vel=}')
        
        pos_a = pos_a.move_towards(pos_b, vel)
        # print(f'[DEBUG] HUMAN from {self.country} (2): {pos_a=}, {pos_b=}, {vel=}')
        
        pos_a.x, pos_a.y = round(pos_a.x, 0), round(pos_a.y, 0)
        # print(f'[DEBUG] HUMAN from {self.country} (3): {pos_a=}, {pos_b=}, {vel=}')

        self.rect.x, self.rect.y = pos_a.x, pos_a.y
        # print(f'[DEBUG] HUMAN from {self.country} (4): {self.rect.x=}, {self.rect.y=}, {pos_b=}')
        
        return False
    
    def move_to(self, rect):
        center1 = ((self.rect.x + self.size) / 2, (self.rect.y + self.size) / 2)
        center2 = ((rect.x + rect.size) / 2, (rect.y + rect.size) / 2)

        dx = center2[0] - center1[0]
        dy = center2[1] - center1[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > self.step:
            scale = min(self.step, distance) / distance
            dx *= scale
            dy *= scale

        self.rect.x += dx
        self.rect.y += dy
        self.rect.x = round(self.rect.x / self.step) * self.step
        self.rect.y = round(self.rect.y / self.step) * self.step

        if distance <= self.step:
            return True
        else:
            return False
    
    def _move_to(self, rect):
        # center1 = ((self.rect.x + self.size) / 2, (self.rect.y + self.size) / 2)
        # center2 = ((rect.x + rect.width) / 2, (rect.y + rect.height) / 2)
    
        # dx = center2[0] - center1[0]
        # dy = center2[1] - center1[1]
    
        # distance = math.sqrt(dx ** 2 + dy ** 2)
    
        # if distance > self.step * self.game.dt:
        #     scale = min(self.step * self.game.dt, distance) / distance
        #     dx *= scale
        #     dy *= scale
    
        # self.rect.x += dx
        # self.rect.y += dy
        # self.rect.x = round(self.rect.x / self.step) * self.step * self.game.dt
        # self.rect.y = round(self.rect.y / self.step) * self.step * self.game.dt
    
        # if distance <= self.step:
        #     return True
        # else:
        #     return False
        
        pos_a = pygame.Vector2(self.rect.x, self.rect.y)
        pos_b = pygame.Vector2(rect.x, rect.y)
        
        terrain_color = self.scene.terrain.get_at((self.rect.x, self.rect.y))
        if terrain_color in hard_to_walk:
            self.step = original_step_size - 1
        else:
            self.step = original_step_size
        
        vel = self.step * self.game.dt * self.game.game_speed
        vel = math.ceil(vel)
        
        # print(f'[DEBUG] HUMAN from {self.country} (1): {pos_a=}, {pos_b=}, {vel=}')
        
        pos_a = pos_a.move_towards(pos_b, vel)
        # print(f'[DEBUG] HUMAN from {self.country} (2): {pos_a=}, {pos_b=}, {vel=}')
        
        pos_a.x, pos_a.y = round(pos_a.x, 0), round(pos_a.y, 0)
        # print(f'[DEBUG] HUMAN from {self.country} (3): {pos_a=}, {pos_b=}, {vel=}')

        self.rect.x, self.rect.y = pos_a.x, pos_a.y
        # print(f'[DEBUG] HUMAN from {self.country} (4): {self.rect.x=}, {self.rect.y=}, {pos_b=}')
        
        if (self.rect.x, self.rect.y) == (rect.x, rect.y):
            return True
        return False
    
    def attack(self, enemy):
        enemy.hp -= round(random.uniform(self.damage['min'], self.damage['max']), 2)
    
    def destroy(self):
        self.country.humans.remove(self)
        del self