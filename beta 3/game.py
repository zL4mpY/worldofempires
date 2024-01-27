import pygame, random, math
from datetime import datetime

import gameStateManager
import textManager
import imageManager
import settings

def get_countries_list():
    with open('countries.txt', 'r', encoding='utf-8') as countriesList:
        countries = countriesList.readlines()
    
    return countries

def distance(point1, point2):
    return math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)

class Notification:
    types = ['warDeclared', 'peaceDeclared', 'countryDestroyed', 'countryCreated']
    count = 0
    def __init__(self, text, timer = 3):
        self.type = type
        self.textManager = textManager.TextManager()
        self.timer = timer * 25**2


        self.font = game.settings['font']
        self.text_color = (0, 0, 0)
        self.text = text
        self.size = 12
    
    def render(self, y):
        self.textManager.render(game.screen, 7, game.height - y - 15, self.text, self.font, self.text_color, self.size)
        self.timer -= game.fps

class Event:
    def __init__(self, description):
        self.description = description
        self.time = datetime.now() - launch_time

        total_seconds = self.time.total_seconds()

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
        return f"{self.time}: {self.description}\n"

class Land:
    def __init__(self, country, position):
        self.country = country
        self.x, self.y = position
        self.color = country.territory_color
        self.size = game.gameState.LAND_CELL_SIZE

    def render(self):
        pygame.draw.rect(game.screen, self.color, (self.x, self.y, self.size, self.size))
    
    def __repr__(self):
        return f'Land of {self.country} (x={self.x} y={self.y})'

class City:
    def __init__(self, country, position, isCapital = False):
        self.country = country
        self.x, self.y = position

        # self.name = languageVars['city'] if isCapital == False else self.country.name_w_status

        self.name: str
        match game.settings['language']:
            case 'ru':
                self.name = self.country.name if isCapital else "Город"
            
            case 'en':
                self.name = self.country.name if isCapital else "City"
            
            case _:
                self.name = self.country.name if isCapital else "City"
        
        self.color = self.country.color
        self.text_color = self.color
        self.size = game.gameState.CELL_SIZE
        self.isCapital = isCapital
        self.textManager = textManager.TextManager()
        self.hp = 250
        self.max_hp = 250
        self.regen_size = {'min': round(random.uniform(0.05, 2), 2), 'max': round(random.uniform(2, 10), 2)}
    
    def render(self):
        pygame.draw.rect(game.screen, self.color, (self.x, self.y, self.size, self.size))
        self.textManager.render(game.screen, self.x - 20, self.y - 15, self.name, 'arialblack', self.text_color, 10)
    
    def act(self):
        if game.settings['auto_spawn']['humans']['enabled']:
            if random.uniform(0, 1) < game.settings['auto_spawn']['humans']['spawn_chance'] / 12500:
                self.spawn_human()
        
        if self.country.states['in_war'] == False:
            if self.hp <= self.max_hp:
                self.hp += round(random.uniform(self.regen_size['min'], self.regen_size['max']), 2)

                if self.hp >= self.max_hp:
                    self.hp = self.max_hp

    
    def spawn_human(self):
        self.country.humans.append(Human((self.x, self.y), self.country, self))

class Battle:
    def __init__(self, war, city):
        self.war = war
        self.enemies = self.war.enemies
        
        self.city = city
        self.country = city.country
        self.place = city

        self.render_message: str
        self.render_text_color = self.city.country.color

        match game.settings['language']:
            case 'ru':
                self.render_message = 'Битва'

            case "en":
                self.render_message = 'Battle'

            case _:
                self.render_message = 'Battle'
        
        self.textRenderer = textManager.TextManager()
    
    def get_place(self):
        x = random.randint(self.city.x - random.randrange(0, 20, 5), self.city.x + random.randrange(0, 20, 5))
        y = random.randint(self.city.y - random.randrange(0, 20, 5), self.city.y + random.randrange(0, 20, 5))

        self.place = Place(x, y)

    def end(self):
        self.war.remove(self)        
        del self

    def render(self):

        self.textRenderer.render(game.screen, self.place.x + 5, self.place.y - 5, self.render_message, 'arialblack', self.render_text_color, 9)
    
    def __repr__(self):
        return f'Battle ({self.enemy1} VS {self.enemy2})'

class War:
    def __init__(self, enemies):
        self.enemies = enemies
        self.textRenderer = textManager.TextManager()
        self.battles = []  # список битв в рамках войны
        self.render_message: str

        match game.settings['language']:
            case 'ru':
                self.render_message = 'Война'

            case "en":
                self.render_message = 'War'

            case _:
                self.render_message = 'War'
    
    def add_battle(self, battle: Battle):
        self.battles.append(battle)  # метод для добавления новой битвы в список
    
    def render(self):
        if len(self.battles) > 0:
            self.textRenderer.render(game.screen, self.battles[0].place.x + 5, self.battles[0].place.y - 5, self.render_message, 'arialblack', (0,0,0), 9)
    
    def end(self):
        war1 = None
        for country in self.enemies:
            for war in country.wars:
                if war == self:
                    country.states['in_war'] = False
                    country.states['return_to_homeland'] = True
                    country.wars.remove(self)
                else:
                    if war.enemies[1] == self.enemies[0] and war.enemies[0] == self.enemies[1]:
                        war1 = war
                        country.states['in_war'] = False
                        country.states['return_to_homeland'] = True
                        country.wars.remove(war)

        if self in game.gameState.wars:
            game.gameState.wars.remove(self)
        else:
            game.gameState.wars.remove(war1)
    
    def __repr__(self):
        return f'War ({self.enemies[0].name} VS {self.enemies[1].name})'

class Place:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.size = game.gameState.CELL_SIZE

class Human:
    def __init__(self, position, country, homeland):
        self.x, self.y = position
        self.country = country
        self.color = self.country.color
        self.size = 2
        self.step = 2

        self.homeland = homeland

        self.hp = 150
        self.max_hp = 150
        self.regen_size = {'min': round(random.uniform(0.05, 2), 2), 'max': round(random.uniform(2, 10), 2)}
        self.damage = {'min': round(random.uniform(0, 0.5), 1), 'max': round(random.uniform(0.5, 5), 1)}

        self.states = {'in_war': False, 'return_to_homeland': False}

        self.watch_radius = 25.0
        self.watch_radius_rect = pygame.Rect(self.x - self.watch_radius, self.y - self.watch_radius, self.watch_radius * 2, self.watch_radius * 2)
    
    def render(self):
        pygame.draw.rect(game.screen, self.color, (self.x, self.y, self.size, self.size))

    def act(self):
        if self.states['in_war']:
            for war in self.country.wars:
                if len(war.battles) > 0:
                    current_battle = war.battles[0]
                    if self.move_to(current_battle.place):
                        enemies = self.find_enemies()

                        if len(enemies) > 0:
                            chosen_enemy = random.choice(enemies)
                            self.attack(chosen_enemy)

                            if chosen_enemy.hp <= 0:
                                if isinstance(chosen_enemy, Country):
                                    chosen_enemy.destroy_city(current_battle.place, self)
                                else:
                                    chosen_enemy.destroy()
        
        else:
            if self.states['return_to_homeland']:
                if self.move_to_zone(self.homeland):
                    self.states['return_to_homeland'] = False
                return
            
            actions, chances = ["move"], [100]
            action = random.choices(actions, chances, k=1)[0]

            match action:
                case "move":
                    self.move()

                case _:
                    self.move()
            
            if self.hp < self.max_hp:
                self.hp += round(random.uniform(self.regen_size['min'], self.regen_size['max']), 2)
                self.hp = self.max_hp if self.hp > self.max_hp else self.hp

    def move(self):
        if not self.country.is_claimed_territory(self.x, self.y):
            if self.country.is_on_enemy_territory(self.x, self.y):
                for country in game.gameState.countries:
                    if country != self.country and country.is_claimed_territory(self.x, self.y):
                        country.remove_territory(self.x, self.y)

                        if random.random() < 1 / 2:
                            if country.hp >= 150:
                                found = False

                                if len(country.agression) > 0:
                                    for country1 in country.agression.keys():
                                        if country1 == self.country:
                                            found = True
                                else:
                                    country.agression[self.country] = 0.0
                                    found = True

                                if found:
                                    country.agression[self.country] += float(random.randint(5, 20))
                                    country.agression[self.country] = 100.0 if country.agression[self.country] > 100.0 else country.agression[self.country]
                                # country.declare_war(self)
                                # pass
            
            self.country.claim_territory(self.x, self.y)

        dx = random.choice([-(self.step), 0, self.step])
        dy = random.choice([-(self.step), 0, self.step])
        
        self.x += dx
        self.y += dy

        if self.x < self.size:
            self.x = self.size
        elif self.x > game.width:
            self.x = game.width

        if self.y < self.size:
            self.y = self.size
        elif self.y > game.height:
            self.y = game.height
    
    def find_enemies(self):
        enemies = []

        zone_x = (self.x // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE
        zone_y = (self.y // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE

        for country in game.gameState.countries:
            if country != self.country:
                if zone_x <= country.x <= zone_x + game.gameState.LAND_CELL_SIZE and zone_y <= country.y <= zone_y + game.gameState.LAND_CELL_SIZE:
                    enemies.append(country)
                else:
                    for human in country.humans:
                        if zone_x <= human.x <= zone_x + game.gameState.LAND_CELL_SIZE and zone_y <= human.y <= zone_y + game.gameState.LAND_CELL_SIZE:
                            enemies.append(human)
        
        return enemies

    def is_in_territory(self, territory):
        zone_x = (territory.x // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE
        zone_y = (territory.y // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE

        if zone_x <= self.x <= zone_x + game.gameState.LAND_CELL_SIZE and zone_y <= self.y <= zone_y + game.gameState.LAND_CELL_SIZE:
            return True
        
        return False
    
    def move_to_zone(self, rect):
        if self.is_in_territory(rect):
            return True

        center1 = (self.x + self.size / 2, self.y + self.size / 2)
        center2 = (rect.x + rect.size / 2, rect.y + rect.size / 2)

        dx = center2[0] - center1[0]
        dy = center2[1] - center1[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > self.step:
            scale = min(self.step, distance) / distance
            dx *= scale
            dy *= scale

        self.x = self.x + dx
        self.y = self.y + dy
        self.x = round(self.x / self.step) * self.step
        self.y = round(self.y / self.step) * self.step
    
    def move_to(self, rect):
        if self.x == rect.x and self.y == rect.y:
            return True
        
        center1 = (self.x + self.size / 2, self.y + self.size / 2)
        center2 = (rect.x + rect.size / 2, rect.y + rect.size / 2)

        dx = center2[0] - center1[0]
        dy = center2[1] - center1[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > self.step:
            scale = min(self.step, distance) / distance
            dx *= scale
            dy *= scale

        self.x = self.x + dx
        self.y = self.y + dy
        self.x = round(self.x / self.step) * self.step
        self.y = round(self.y / self.step) * self.step
    
    def attack(self, enemy):
        enemy.hp -= round(random.uniform(self.damage['min'], self.damage['max']), 2)
    
    def destroy(self):
        self.country.humans.remove(self)
        del self
        
class Country:
    def __init__(self, name, position, color):
        self.name = name
        self.x, self.y = position
        self.size = game.gameState.CELL_SIZE
        self.step = self.size

        self.color = color
        self.capital = City(self, position, True)
        self.territory_color = tuple(max(0, channel - random.randint(40, 80)) for channel in self.color)

        self.territory = []
        self.cities = []

        self.humans = []
        self.hp = 500
        self.max_hp = 500
        self.regen_size = {'min': round(random.uniform(0, 2.5), 2), 'max': round(random.uniform(2.5, 15), 2)}
        self.damage = {'min': round(random.uniform(0, 5), 2), 'max': round(random.uniform(0.5, 15), 2)}
        self.agression = {}
        self.wars = []

        self.states = {'in_war': False, 'return_to_homeland': False, 'run_from_enemy_territory': False}

        self.watch_radius = 50.0
        
    
    def render(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))
        
        # watchRadius = pygame.Rect(self.x - self.watch_radius, self.y - self.watch_radius, self.watch_radius * 2, self.watch_radius * 2)
        # pygame.draw.rect(screen, self.color, watchRadius)
        # pygame.draw.circle(screen, self.color, (self.x, self.y), self.watch_radius)

        # for country in game.gameState.countries:
        #     if country == self:
        #         continue

        #     countryRect = pygame.Rect(country.x, country.y, country.x + game.gameState.CELL_SIZE, country.y + game.gameState.CELL_SIZE)
    
    def render_capital(self):
        self.capital.render()
    
    def act(self):
        # for country in game.gameState.countries:
        #     if country != self:
        #         self.move_to_zone(country)
        #         return False
        
        if self.states['in_war']:
            for war in self.wars:
                if len(war.battles) > 0:
                    current_battle = war.battles[0]
                    if self.move_to(current_battle.place):
                        enemies = self.find_enemies()

                        if len(enemies) > 0:
                            chosen_enemy = random.choice(enemies)
                            self.attack(chosen_enemy)

                            if chosen_enemy.hp <= 0:
                                if isinstance(chosen_enemy, Country):
                                    chosen_enemy.destroy_city(current_battle.place, self)
                                else:
                                    chosen_enemy.destroy()
        
        else:
            if self.states['return_to_homeland']:
                if self.hp < self.max_hp:
                    self.hp += round(random.uniform(self.regen_size['min'], self.regen_size['max']), 2)
                    self.hp = self.max_hp if self.hp > self.max_hp else self.hp
                
                if self.states['run_from_enemy_territory']:
                    if distance(self, self.capital) > 30:
                        self.move_to_zone(self.capital)
                    else:
                        self.states['return_to_homeland'] = False
                        self.states['run_from_enemy_territory'] = False
                
                else:
                    if self.move_to_zone(self.capital):
                        self.states['return_to_homeland'] = False
                return

            for country, agression_value in self.agression.items():
                if agression_value >= 100.0:
                    if country.hp >= country.max_hp - 50 and len(country.wars) == 0 and self.hp >= self.max_hp - 50:
                        self.declare_war(country)


            actions, chances = ["move", "create_city"], [90, 10]
            action = random.choices(actions, chances, k=1)[0]

            match action:
                case "move":
                    self.move()

                case "create_city":
                    all_distances_above_30 = all(distance(self, city) >= 90 for city in game.gameState.cities)

                    if all_distances_above_30:
                        city = City(self, (self.x, self.y), False)

                        message: str

                        match game.settings['language']:
                            case 'ru':
                                message = 'Государство {} возвело новый город'

                            case 'en':
                                message = 'Country {} has founded a new city'

                            case _:
                                message = 'Country {} has founded a new city'

                        game.gameState.notifications.append(Notification(message.format(self.name)))
                        game.gameState.events.append(Event(message.format(self.name)))

                        self.cities.append(city)
                        game.gameState.cities.append(city)
                    

                case _:
                    self.move()
            
            if self.hp < self.max_hp:
                self.hp += round(random.uniform(self.regen_size['min'], self.regen_size['max']), 2)
                self.hp = self.max_hp if self.hp > self.max_hp else self.hp
    
    def move(self):
        if not self.is_claimed_territory(self.x, self.y):
            if self.is_on_enemy_territory(self.x, self.y):
                for country in game.gameState.countries:
                    if country != self and country.is_claimed_territory(self.x, self.y):
                        if len(self.humans) > 0:
                            self.states['return_to_homeland'] = True
                            self.states['run_from_enemy_territory'] = True
                        else:

                            country.remove_territory(self.x, self.y)

                            if random.random() < 1 / 2:
                                if country.hp >= 150:
                                    found = False

                                    if len(country.agression) > 0:
                                        for country1 in country.agression.keys():
                                            if country1 == self:
                                                found = True
                                    else:
                                        country.agression[self] = 0.0
                                        found = True

                                    if found:
                                        country.agression[self] += float(random.randint(5, 20))
                                        country.agression[self] = 100.0 if country.agression[self] > 100.0 else country.agression[self]
                                    # country.declare_war(self)
                                # pass
                            
                            self.claim_territory(self.x, self.y)
            else:
                self.claim_territory(self.x, self.y)
        
        dx = random.choice([-(self.step), 0, self.step])
        dy = random.choice([-(self.step), 0, self.step])
        
        self.x += dx
        self.y += dy

        if self.x < self.step:
            self.x = self.step
        elif self.x > game.width:
            self.x = game.width

        if self.y < self.step:
            self.y = self.step
        elif self.y > game.height:
            self.y = game.height
        
    def is_in_territory(self, territory):
        zone_x = (territory.x // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE
        zone_y = (territory.y // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE

        if zone_x <= self.x <= zone_x + game.gameState.LAND_CELL_SIZE and zone_y <= self.y <= zone_y + game.gameState.LAND_CELL_SIZE:
            return True
        
        return False

    def find_enemies(self):
        enemies = []

        zone_x = (self.x // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE
        zone_y = (self.y // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE

        for country in game.gameState.countries:
            if country != self:
                if zone_x <= country.x <= zone_x + game.gameState.LAND_CELL_SIZE and zone_y <= country.y <= zone_y + game.gameState.LAND_CELL_SIZE:
                    enemies.append(country)
                else:
                    for human in country.humans:
                        if zone_x <= human.x <= zone_x + game.gameState.LAND_CELL_SIZE and zone_y <= human.y <= zone_y + game.gameState.LAND_CELL_SIZE:
                            enemies.append(human)
        
        return enemies
    
    def move_to_zone(self, rect):
        if self.is_in_territory(rect):
            return True

        center1 = (self.x + self.size / 2, self.y + self.size / 2)
        center2 = (rect.x + rect.size / 2, rect.y + rect.size / 2)

        dx = center2[0] - center1[0]
        dy = center2[1] - center1[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > self.step:
            scale = min(self.step, distance) / distance
            dx *= scale
            dy *= scale

        self.x = self.x + dx
        self.y = self.y + dy
        self.x = round(self.x / self.step) * self.step
        self.y = round(self.y / self.step) * self.step
    
    def move_to(self, rect):
        if self.x == rect.x and self.y == rect.y:
            return True
        
        center1 = (self.x + self.size / 2, self.y + self.size / 2)
        center2 = (rect.x + rect.size / 2, rect.y + rect.size / 2)

        dx = center2[0] - center1[0]
        dy = center2[1] - center1[1]

        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance > self.step:
            scale = min(self.step, distance) / distance
            dx *= scale
            dy *= scale

        self.x = self.x + dx
        self.y = self.y + dy
        self.x = round(self.x / self.step) * self.step
        self.y = round(self.y / self.step) * self.step
    
    def attack(self, enemy):
        enemy.hp -= round(random.uniform(self.damage['min'], self.damage['max']), 2)
        
    def declare_war(self, enemy):
        if isinstance(enemy, Human):
            enemy = enemy.country

        country_of_war = enemy
        city_of_war = random.choice(country_of_war.cities) if len(country_of_war.cities) > 0 else country_of_war.capital

        war1 = War((self, enemy))
        war2 = War((enemy, self))

        battle1 = Battle(war1, city_of_war)
        battle2 = Battle(war2, city_of_war)

        war1.add_battle(battle1)
        war2.add_battle(battle2)

        send_notification = [False, False]

        if not war1 in self.wars:
            self.wars.append(war1)
            send_notification[0] = True
            self.states['in_war'] = True

            num_to_apply = int(len(self.humans) * 0.45)
            for i, human in enumerate(self.humans):
                if i < num_to_apply:
                    human.step = 5
                    human.states['in_war'] = True
        
        if not war2 in enemy.wars:
            enemy.wars.append(war2)
            send_notification[1] = True
            enemy.states['in_war'] = True

            num_to_apply = int(len(enemy.humans) * 0.45)
            for i, human in enumerate(enemy.humans):
                if i < num_to_apply:
                    human.step = 5
                    human.states['in_war'] = True
        
        if all(send_notification):

            message: str

            match game.settings['language']:
                case 'ru':
                    message = 'Государство {} объявило войну государству {}'

                case "en":
                    message = 'Country {} declared a war to {}'

                case _:
                    message = 'Country {} declared a war to {}'

            game.gameState.notifications.append(Notification(message.format(self.name, enemy.name)))
            game.gameState.events.append(Event(message.format(self.name, enemy.name)))
            game.gameState.wars.append(war1)
    
    def in_war_with(self, country):
        for war in self.wars:
            if war.enemies[1] == country:
                return True
        
        return False
    
    def is_claimed_territory(self, x, y):
        zone_x = (x // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE
        zone_y = (y // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE
        
        for land in self.territory:
            if (land.x, land.y) == (zone_x, zone_y):
                return True
        
        return False

    def is_on_enemy_territory(self, x, y):
        for country in game.gameState.countries:
            if country != self and country.is_claimed_territory(x, y):
                return True
        return False

    def find_closest_enemy(self):
        closest_enemy = None
        closest_distance = float('inf')
        for enemy in self.enemyCountries:
            if enemy != self:

                distance = math.sqrt((enemy.x - self.x)**2 + (enemy.y - self.y)**2)
                if distance < closest_distance:
                    closest_distance = distance
                    closest_enemy = enemy

        return closest_enemy
    
    def claim_territory(self, x, y):
        zone_x = (x // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE
        zone_y = (y // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE

        if zone_x <= x <= zone_x + game.gameState.LAND_CELL_SIZE and zone_y <= y <= zone_y + game.gameState.LAND_CELL_SIZE:
            self.territory.append(Land(self, (zone_x, zone_y)))

    def remove_territory(self, x, y):
        zone_x = (x // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE
        zone_y = (y // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE

        for land in self.territory:
            if (land.x, land.y) == (zone_x, zone_y):
                self.territory.pop(self.territory.index(land))
                return True
    
    def destroy_city(self, city, destroyer):
        if isinstance(destroyer, Human):
            destroyer = destroyer.country
        
        my_battle = None
        for war in self.wars:
            if war.enemies[1] == destroyer:
                for battle in war.battles:
                    if destroyer in battle.enemies and battle.place == city:
                        my_battle = battle
                        self.states['in_war'] = False
                        self.states['return_to_homeland'] = True
                        self.agression[destroyer] = 0.0
                        war.battles.remove(battle)

        for war in destroyer.wars:
            if war.enemies[1] == self:
                for battle in war.battles:
                    if self in battle.enemies and battle.place == city:
                        destroyer.states['in_war'] = False
                        destroyer.states['return_to_homeland'] = True
                        destroyer.agression[self] = 0.0
                        war.battles.remove(battle)
        
        for war in self.wars:
            if war.enemies[1] == destroyer:
                war.end()
        
        for war in destroyer.wars:
            if war.enemies[1] == self:
                war.end()
        
        if not my_battle:
            return

        city = my_battle.place

        closest_territories, closest_humans = [], []
        distance_threshold = 80

        for land in self.territory:
            # Вычисляем расстояние между городом и территорией
            distance = math.sqrt((city.x - land.x)**2 + (city.y - land.y)**2)
            # Если расстояние меньше порогового значения, добавляем территорию в список ближайших
            if distance < distance_threshold:
                closest_territories.append(land)
        
        for human in self.humans:
            # Вычисляем расстояние между целевой точкой и человеком
            distance = math.sqrt((city.x - human.x)**2 + (city.y - human.y)**2)
            # Если расстояние меньше порогового значения, добавляем человека в список ближайших
            if distance < distance_threshold:
                closest_humans.append(human)
        
        if city.country == self:
            if not city.isCapital:
                city.country = destroyer
                city.color = destroyer.color
                city.text_color = city.color

                self.cities.remove(city)
                destroyer.cities.append(city)

                for land in closest_territories:
                    land.country = destroyer
                    land.color = destroyer.territory_color
                    self.territory.remove(land)
                    destroyer.territory.append(land)
                
                # for human in closest_humans:
                #     if human.states['in_war']:
                #         human.states['in_war'] = False
                #         human.states['return_to_homeland'] = True
                #     human.country = destroyer
                #     human.color = destroyer.color
                #     self.humans.remove(human)
                #     destroyer.humans.append(human)

                for human in self.humans:
                    if human.states['in_war']:
                        human.states['in_war'] = False
                        human.states['return_to_homeland'] = True
                        human.step = human.size
                
                for human in destroyer.humans:
                    if human.states['in_war']:
                        human.states['in_war'] = False
                        human.states['return_to_homeland'] = True
                        human.step = human.size

                message: str

                match game.settings['language']:
                    case 'ru':
                        message = 'Государство {} захватило город государства {}'
                    
                    case 'en':
                        message = 'Country {} has captured the city of {}'
                    
                    case _:
                        message = 'Country {} has captured the city of {}'

                game.gameState.notifications.append(Notification(message.format(self.name, destroyer.name)))
                game.gameState.events.append(Event(message.format(self.name, destroyer.name)))
            
            else:
                if len(self.cities) > 0:
                    city = self.capital
                    city.country = destroyer
                    city.color = destroyer.color
                    city.text_color = city.color
                    city.isCapital = False
                    
                    match game.settings['language']:
                        case 'ru':
                            city.name = city.country.name if city.isCapital else "Город"

                        case 'en':
                            city.name = city.country.name if city.isCapital else "City"

                        case _:
                            city.name = city.country.name if city.isCapital else "City"

                    destroyer.cities.append(city)
                    new_capital = random.choice(self.cities)
                    new_capital.isCapital = True

                    for land in closest_territories:
                        land.country = destroyer
                        land.color = destroyer.territory_color
                        self.territory.remove(land)
                        destroyer.territory.append(land)
                    
                    for human in self.humans:
                        if human.states['in_war']:
                            human.states['in_war'] = False
                            human.states['return_to_homeland'] = True
                            human.step = human.size
                        
                    for human in destroyer.humans:
                        if human.states['in_war']:
                            human.states['in_war'] = False
                            human.states['return_to_homeland'] = True
                            human.step = human.size

                    # for human in closest_humans:
                    #     if human.states['in_war']:
                    #         human.states['in_war'] = False
                    #         human.states['return_to_homeland'] = True
                    #     human.country = destroyer
                    #     human.color = destroyer.color
                    #     self.humans.remove(human)
                    #     destroyer.humans.append(human)

                    match game.settings['language']:
                        case 'ru':
                            new_capital.name = new_capital.country.name if new_capital.isCapital else "Город"

                        case 'en':
                            new_capital.name = new_capital.name if new_capital.isCapital else "City"

                        case _:
                            new_capital.name = new_capital.name if new_capital.isCapital else "City"

                    self.capital = new_capital
                    self.cities.remove(new_capital)

                    message: str

                    match game.settings['language']:
                        case 'ru':
                            message = 'Государство {} захватило город государства {}'

                        case 'en':
                            message = 'Country {} has captured the city of {}'

                        case _:
                            message = 'Country {} has captured the city of {}'

                    game.gameState.notifications.append(Notification(message.format(self.name, destroyer.name)))
                    game.gameState.events.append(Event(message.format(self.name, destroyer.name)))

                else:
                    self.destroy(destroyer)
                    return
        
        elif my_battle.place.country == destroyer:
            
            people_in_war = [human for human in destroyer.humans if human.states['in_war'] == True]
            num = int(len(people_in_war) * (10 / 100))

            for i, human in enumerate(people_in_war):
                if i < num:
                    human.destroy()
                else:
                    human.states['in_war'] = False
                    human.states['return_to_homeland'] = True
            
            list(map(lambda human: setattr(human, 'step', human.size), destroyer.humans))
        
            people_in_war = [human for human in self.humans if human.states['in_war'] == True]
            num = int(len(people_in_war) * (20 / 100))

            for i, human in enumerate(people_in_war):
                if i < num:
                    human.destroy()
                else:
                    human.states['in_war'] = False
                    human.states['return_to_homeland'] = True

            list(map(lambda human: setattr(human, 'step', human.size), self.humans))

            message: str

            match game.settings['language']:
                case 'ru':
                    message = 'Государство {} проиграло войну государству {}'

                case 'en':
                    message = 'Country {} lost the war to {}'

                case _:
                    message = 'Country {} lost the war to {}'

            game.gameState.notifications.append(Notification(message.format(self.name, destroyer.name)))
            game.gameState.events.append(Event(message.format(self.name, destroyer.name)))


    def destroy(self, destroyer):
        if isinstance(destroyer, Human):
            destroyer = destroyer.country
        
        for human in destroyer.humans:
            human.states['return_to_homeland'] = True
            human.states['in_war'] = False
        
        destroyer.states['in_war'] = False
        destroyer.states['return_to_homeland'] = True
        destroyer.agression[self] = 0.0
        destroyer.agression.pop(self, None)

        for country in game.gameState.countries:
            if country != destroyer:
                for country1, agression in list(country.agression.items()):
                    if country1 == self:
                        if country.in_war_with(self):
                            for war in country.wars:
                                if war.enemies[1] == self:
                                    war.end()
                        country.agression.pop(self, None)

        # allocate who should die and who should live in country-destroyer
        # who should die
        
        people_in_war = [human for human in self.humans if human.states['in_war'] == True]
        num = int(len(people_in_war) * (25 / 100))
        
        for i, human in enumerate(people_in_war):
            if i < num:
                self.humans.remove(human)
                del human
            
            # who should live in country-destroyer
            else:
                human.country = destroyer
                human.color = destroyer.color
                human.step = human.size
                human.states['in_war'] = False

                self.humans.remove(human)
                destroyer.humans.append(human)
                human.states['return_to_homeland'] = True

        for city in self.cities:
            city.country = destroyer
            city.color = destroyer.color
            city.text_color = city.color
            
            self.cities.remove(city)
            destroyer.cities.append(city)
        
        self.capital.country = destroyer
        self.capital.color = destroyer.color
        self.capital.text_color = self.capital.color
        self.capital.isCapital = False

        match game.settings['language']:
            case 'ru':
                self.capital.name = self.capital.country.name if self.capital.isCapital else "Город"

            case 'en':
                self.capital.name = self.capital.country.name if self.capital.isCapital else "City"

            case _:
                self.capital.name = self.capital.country.name if self.capital.isCapital else "City"

        destroyer.cities.append(self.capital)

        for land in self.territory:
            land.color = destroyer.territory_color
            land.country = destroyer
            destroyer.territory.append(land)
        
        self.territory = []
        
        for war in self.wars:
            if war.enemies[1] == destroyer:
                war.end()
        
        for war in destroyer.wars:
            if war.enemies[1] == self:
                war.end()

        message: str

        match game.settings['language']:
            case 'ru':
                message = 'Государство {} было уничтожено государством {}'
            
            case "en":
                message = 'Country {} was destroyed by {}'
            
            case _:
                message = 'Country {} was destroyed by {}'
        
        game.gameState.notifications.append(Notification(message.format(self.name, destroyer.name)))
        game.gameState.events.append(Event(message.format(self.name, destroyer.name)))

        game.gameState.countries.remove(self)
        del self
    
    def __repr__(self):
        return f'{self.name} ({len(self.humans)+1} population)'

class GameState:
    def __init__(self):
        self.CELL_SIZE = 5
        self.LAND_CELL_SIZE = 20

        self.all_countries = get_countries_list()

        self.countries, self.cities, self.notifications, self.wars, self.events = [], [], [], [], []
        
        self.textManager = textManager.TextManager()

        # self.keys = {pygame.K_6: self.spawn_country}
        self.customEvents = {'start': pygame.event.Event(pygame.USEREVENT+1, attr1='start')}
        
        self.started = False
    
    def spawn_country(self, name, position, color):
        country = Country(name, position, color)

        message: str

        match game.settings['language']:
            case 'ru':
                message = 'Государство {} было создано'
            
            case "en":
                message = 'Country {} was created'
            
            case _:
                message = 'Country {} was created'
        
        self.notifications.append(Notification(message.format(name)))
        self.events.append(Event(message.format(name)))
        self.countries.append(country)
        self.cities.append(country.capital)
        return country

    def draw_grid(self, color):
        for x in range(0, game.width, self.CELL_SIZE):
            pygame.draw.line(game.screen, color, (x, 0), (x, game.height))
        for y in range(0, game.height, self.CELL_SIZE):
            pygame.draw.line(game.screen, color, (0, y), (game.width, y))
        
    def draw_debug_grid(self, cell_size, color):
        for x in range(0, game.width, cell_size):
            pygame.draw.line(game.screen, color, (x, 0), (x, game.height))
        for y in range(0, game.height, cell_size):
            pygame.draw.line(game.screen, color, (0, y), (game.width, y))
    
    def draw_legend(self, country, y):

        pygame.draw.rect(game.screen, country.territory_color, (20, y + 30, 15, 15))
        pygame.draw.rect(game.screen, country.color, (20, y + 30, 15, 15), 2)

        if game.settings['countries']['play_as_country']:
            if not self.countries[self.player] == country:
                text = f'{country.name} ({len(country.humans) + 1}) (AI)'
            else:
                text = f'{country.name} ({len(country.humans) + 1}) (Player)'
        else:
            text = f'{country.name} ({len(country.humans) + 1})'
        
        if country.hp < country.max_hp:
            text += f' (HP: {int(round(country.hp, 0))})'
        
        self.textManager.render(game.screen, 20 + 20, y + 25, text, game.settings['font'], (0, 0, 0), 16)
    
    def update(self):
        for country in self.countries:
            country.act()
            list(map(lambda human: human.act(), country.humans))
        
        for country in self.countries:
            list(map(lambda city: city.act(), country.cities))
            country.capital.act()
        
        if game.settings['auto_spawn']['countries']['enabled']:
            if random.uniform(0, 1) < game.settings['auto_spawn']['countries']['spawn_chance'] / 15000:
                if len(self.countries) < game.settings['countries']['max_countries']:
                    countryRandomName = random.choice(self.all_countries)

                    name: str

                    match game.settings['language']:
                        case 'ru':
                            name = countryRandomName.split(" #!\\ ", 1)[0]
                        
                        case 'en':
                            name = countryRandomName.split(" #!\\ ", 1)[1]
                        
                        case _:
                            name = countryRandomName.split(" #!\\ ", 1)[1]

                    while name in [i.name for i in self.countries]:
                        countryRandomName = random.choice(self.all_countries)

                        name: str

                        match game.settings['language']:
                            case 'ru':
                                name = countryRandomName.split(" #!\\ ", 1)[0]

                            case 'en':
                                name = countryRandomName.split(" #!\\ ", 1)[1]

                            case _:
                                name = countryRandomName.split(" #!\\ ", 1)[1]
                    
                    available_territory = False

                    while True:
                        if available_territory:
                            break

                        x, y = random.randrange(self.CELL_SIZE, game.width, self.CELL_SIZE), random.randrange(self.CELL_SIZE, game.height, self.CELL_SIZE)

                        zone_x = (x // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE
                        zone_y = (y // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE
                        
                        # all(distance(self, city) >= 90 for city in game.gameState.cities)
                        if not all(country.is_claimed_territory(zone_x, zone_y) for country in self.countries) and not all(distance(Place(x, y), city) >= 90 for city in self.cities):
                            # if not country.is_claimed_territory(Land(country, (zone_x, zone_y))):
                            # if not (Land(country, (zone_x, zone_y)) in country.territory):
                            available_territory = True
                            break
                    
                    pos = (x, y)
                    color = random.randint(20, 230), random.randint(20, 230), random.randint(20, 230)

                    self.spawn_country(name, pos, color)
    
    def handle_event(self, event, type = None):
        if not type:
            type = event.type
        
        # print(type)
        
        if type == pygame.USEREVENT+1:
            if not self.started:
                if event == self.customEvents['start']:
                    self.started = True
                    # on start we create some countries depending on min and max count of they
                    for i in range(random.randint(game.settings['countries']['min_countries'], game.settings['countries']['max_countries'])):
                        # name = languageVars['getCountry']()
                        countryRandomName = random.choice(self.all_countries)

                        name: str

                        match game.settings['language']:
                            case 'ru':
                                name = countryRandomName.split(" #!\\ ", 1)[0]
                            
                            case 'en':
                                name = countryRandomName.split(" #!\\ ", 1)[1]
                            
                            case _:
                                name = countryRandomName.split(" #!\\ ", 1)[1]

                        while name in [i.name for i in self.countries]:
                            countryRandomName = random.choice(self.all_countries)

                            name: str

                            match game.settings['language']:
                                case 'ru':
                                    name = countryRandomName.split(" #!\\ ", 1)[0]

                                case 'en':
                                    name = countryRandomName.split(" #!\\ ", 1)[1]

                                case _:
                                    name = countryRandomName.split(" #!\\ ", 1)[1]
                        
                        available_territory = False
                        

                        while True:
                            if available_territory:
                                break
                            
                            pos = (random.randrange(self.CELL_SIZE, game.width, self.CELL_SIZE), random.randrange(self.CELL_SIZE, game.height, self.CELL_SIZE))
                            x, y = pos[0], pos[1]

                            zone_x = (x // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE
                            zone_y = (y // game.gameState.LAND_CELL_SIZE) * game.gameState.LAND_CELL_SIZE

                            # all(distance(self, city) >= 90 for city in game.gameState.cities)
                            if len(self.countries) > 0 and len(self.cities) > 0:
                                if not all(country.is_claimed_territory(zone_x, zone_y) for country in self.countries) and not all(distance(Place(x, y), city) >= 90 for city in self.cities):
                                    # if not country.is_claimed_territory(Land(country, (zone_x, zone_y))):
                                    # if not (Land(country, (zone_x, zone_y)) in country.territory):
                                    available_territory = True
                                
                                # else:
                                #     pos = (random.randrange(self.CELL_SIZE, game.width, self.CELL_SIZE), random.randrange(self.CELL_SIZE, game.height, self.CELL_SIZE))
                            else:
                                available_territory = True
                                               
                        color = random.randint(20, 230), random.randint(20, 230), random.randint(20, 230)

                        self.spawn_country(name, pos, color)
                        # self.notifications.append(Notification(languageVars['onCountryCreate'].format(name)))
                        # self.events.append(Event(languageVars['onCountryCreate'].format(name)))
        
        elif type in ['KEYDOWN', 'KEYUP', 'TEXTINPUT']:
            if event.key == pygame.K_1:
                for country in self.countries:
                    print(f'Country {country.name} {country.agression}')
            
            elif event.key == pygame.K_2:
                for event in self.events:
                    print(f'- [{event.time}] {event.description}')
    
    def render(self, screen):
        self.draw_debug_grid(self.LAND_CELL_SIZE, (193, 193, 193))

        for country in self.countries:
            list(map(lambda land: land.render(), country.territory))
        
        for country in self.countries:
            country.render(screen)

        for country in self.countries:
            list(map(lambda human: human.render(), country.humans))
        
        for country in self.countries:
            country.render_capital()
        
        for country in self.countries:
            list(map(lambda city: city.render(), country.cities))
        
        for war in self.wars:
            for battle in war.battles:
                battle.render()
        
        mul = 0
        for notification in self.notifications:
            if notification.timer > 0:
                notification.render(10 * (self.notifications.index(notification)) + 5 * mul)
                mul += 1
            else:
                self.notifications.remove(notification)
        
        for i, country in enumerate(self.countries):
            self.draw_legend(country, 20 * i)


class Game:
    def __init__(self):
        # initializing managers

        self.settingsManager = settings.Settings()
        self.settings = self.settingsManager.settings
        self.gameStateManager = gameStateManager.GameStateManager()

        self.resolution = self.settingsManager.getResolution()
        self.fps = self.settingsManager.getMaxFPS()
        self.width, self.height = self.resolution

        # initializing pygame and the game itself

        pygame.init()

        if self.settings['fullscreen']:
            self.screen = pygame.display.set_mode(self.resolution, pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode(self.resolution)
        
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("World of Empires")
        
        # creating game states

        self.gameState = GameState()

        self.gameStateManager.add_state('gameState', self.gameState)
        # self.gameStateManager.add_state('pauseState', self.pauseState)
        self.gameStateManager.switch_state('gameState')
        self.is_running = True

        
    def run(self):
        while self.is_running:
            current_state = self.gameStateManager.current_state
            if not self.gameState.started:
                pygame.event.post(self.gameState.customEvents['start'])
                # pygame.time.set_timer(game.gameState.customEvents['addAge'], 60000)

            self.screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.gameStateManager.switch_state('pauseState')
                    else:
                        current_state.handle_event(event, 'KEYDOWN')

            current_state.handle_event(event)
            current_state.update()
            current_state.render(self.screen)

            pygame.display.flip()
            self.clock.tick(self.fps)

if __name__ == '__main__':
    game = Game()
    launch_time = datetime.now()
    game.run()