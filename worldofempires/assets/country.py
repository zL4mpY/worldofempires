import engine

from ..custom_managers.logManager import Log, LogsManager

from .city import City
from .land import Land
from .partnership import Partnership
from .alliance import Alliance
from .human import Human
from .king import King
from .war import War
from .battle import Battle
from .border import Border

from ..custom_managers.notificationManager import NotificationManager, Notification

import pygame
import random
import math

def distance(point1, point2):
    result = math.sqrt((point2.x - point1.x)**2 + (point2.y - point1.y)**2)
    return result

hard_to_walk = [(50, 89, 38), (80, 143, 61), (22, 156, 233), (45, 166, 235)]

class Country(engine.BaseObject):
    def __init__(self, game, scene, x, y, name, color):
        super().__init__(game, scene, x, y)
        
        self.name = name
        self.size = 2
        self.color = color
        # self.color = (255, 255, 255)
        self.step = self.size

        self.capital = City(self.game, self.scene, x, y, self, True)
        self.territory_color = tuple(max(0, channel - random.randint(40, 80)) for channel in self.color)

        self.territory = []
        self.borders = []
        self.cities = []
        
        from ..custom_managers.inventoryManager import Inventory
        self.inventory = Inventory(self, [])

        self.humans = []
        self.hp = 500
        self.max_hp = 500
        self.regen_size = {'min': round(random.uniform(0, 2.5), 2), 'max': round(random.uniform(2.5, 15), 2)}
        self.damage = {'min': round(random.uniform(0, 5), 2), 'max': round(random.uniform(0.5, 15), 2)}
        self.agression = {}
        self.wars = []

        self.states = {'in_war': False}
        self.allies = []
        self.alliances = []

        self.watch_radius = 50.0
        
        self.king = King(game=self.game, scene=self.scene, x=x, y=y, country=self, homeland=self.capital)
        
        self.surface = pygame.Surface((self.size, self.size))
        self.surface.fill(self.color)
        self.rect = self.surface.get_rect()
        self.rect.x, self.rect.y = x,y
        
    def render(self):
        super().render()
    
    def act(self):
        for war in self.wars:
            if not all([self.scene.country_exists(country) for country in war.participants]):
                for battle in war.battles:
                    battle.end()
                war.end()
        
        for country, agression_value in self.agression.items():
            if agression_value >= 100.0:
                if not self.in_war_with(country):
                    if len(self.humans) + len([self.king]) > 1 and len(country.humans) + len([country.king]) > 1:
                        self.declare_war(country)
        
        actions, chances = ["nothing", "create_city", "declare_war", "create_alliance", "create_friendship"], [90 * self.game.game_speed, round(5 / self.game.fps * self.game.game_speed, 3), round(5 / self.game.fps * self.game.game_speed, 3), round(5 / self.game.fps * self.game.game_speed, 3), round(5 / self.game.fps * self.game.game_speed, 3)]
        action = random.choices(actions, chances, k=1)[0]

        match action:
            case "nothing":
                pass

            case "create_city":
                if not self.king.states['is_mining_resources'] and not self.king.states['return_to_homeland']:
                    all_distances_above_80 = all([distance(self.king.rect, city) >= 80 for city in self.scene.cities])
                    
                    if all_distances_above_80:
                        city = City(self.game, self.scene, self.king.rect.x, self.king.rect.y, self, False)
                        message = self.game.lang['onCityFound']
    
                        self.scene.notificationManager.add_notification(Notification(self.game, self.scene, message.format(self.name)))
                        self.scene.events.append(Log(message.format(self.name)))
                        self.cities.append(city)
                        self.scene.cities.append(city)
            
            case "declare_war":
                if random.random() < 1 / 25 * self.game.game_speed:
                    for country, agression in list(self.agression.items()):
                        if self.agression[country] >= 60:
                            if random.random() < 25 / 100 * self.game.game_speed:
                                if len(self.humans) + len([self.king]) > 1 and not self.in_war_with(country):
                                    self.declare_war(country)
                        else:
                            if random.random() < 1 / 100 * self.game.game_speed:
                                if len(self.humans) + len([self.king]) > 1 and not self.in_war_with(country):
                                    self.declare_war(country) 
            
            case "create_alliance":
                if random.random() < 1 / 100 * self.game.game_speed:
                    ally = None

                    for country in self.scene.countries:
                        if country != self and not country in self.allies:
                            if not engine.in_dict(country, self.agression):
                                if len(country.allies) > 0:
                                    for ally1 in country.allies:
                                        if engine.in_dict(ally1, self.agression):
                                            if self.agression[ally1] < 10:
                                                ally = country
                                else:
                                    ally = country
                            else:
                                if self.agression[country] <= 10:
                                    if len(country.allies) > 0:
                                        for ally1 in country.allies:
                                            if engine.in_dict(ally1, self.agression):
                                                if self.agression[ally1] < 10:
                                                    ally = country
                                    else:
                                        ally = country
                    
                    if ally != None:
                        self.create_alliance(ally)
            
            case "create_friendship":
                if random.random() < 1 / 75 * self.game.game_speed:
                    friend = None
                    
                    for country in self.scene.countries:
                        if country != self and not self.allied_with(country):
                            if not engine.in_dict(country, self.agression):
                                if len(country.allies) > 0:
                                    for ally1 in country.allies:
                                        if engine.in_dict(ally1, self.agression):
                                            if self.agression[ally1] < 10:
                                                friend = country
                                else:
                                    friend = country
                            else:
                                if self.agression[country] <= 10:
                                    if len(country.allies) > 0:
                                        for ally in country.allies:
                                            if engine.in_dict(ally, self.agression):
                                                if self.agression[ally] < 10:
                                                    friend = country
                                    else:
                                        friend = country
                    
                    if friend != None:
                        self.create_friendship(friend)
                        
            case _:
                pass
        
        if self.hp < self.max_hp:
            self.hp += round(random.uniform(self.regen_size['min'], self.regen_size['max']), 2)
            self.hp = self.max_hp if self.hp > self.max_hp else self.hp
    
    def get_people_in_war(self, war = None, battle = None):
        people_in_war = 0
        for human in self.humans:
            if war == None and battle == None:
                if human.states['current_war'] != None and human.states['current_battle'] != None:
                    people_in_war += 1
            elif war != None and battle == None:
                if human.states['current_war'] == war and human.states['current_battle'] != None:
                    people_in_war += 1
            elif war == None and battle != None:
                if human.states['current_war'] != None and human.states['current_battle'] == battle:
                    people_in_war += 1
            elif war != None and battle != None:
                if human.states['current_war'] == war and human.states['current_battle'] == battle:
                    people_in_war += 1
        
        return people_in_war
    
    def change_population_state(self, states: list, values: list, percentage_of_people: int) -> int:
        people = int((len(self.humans)) * percentage_of_people / 100)
        if people > 0:
            for i in range(people):
                for state in states:
                    value = values[states.index(state)]
                    self.humans[i].states[state] = value
            return people
        
        else:
            if len(self.humans) + len([self.king]) > 1:
                human = random.choice(list(filter(lambda x: isinstance(x, Human), self.humans)))
                 
                for state in states:
                    value = values[states.index(state)]
                    human.states[state] = value
                return 1
        
        return 0
    
    def allied_with(self, ally) -> bool:
        if ally in self.allies:
            if self in ally.allies:
                return True
        return False
    
    def attack(self, enemy):
        enemy.hp -= round(random.uniform(self.damage['min'], self.damage['max']), 2)
    
    def create_friendship(self, friend):
        if friend in self.allies and self in friend.allies:
            return
        
        self.allies.append(friend)
        friend.allies.append(self)

        self.agression[friend] = 0.0
        friend.agression[self] = 0.0
        
        self.capital.human_spawn_boost = 15
        map(lambda city: setattr(city, 'human_spawn_boost', 15), self.cities)
        
        friend.capital.human_spawn_boost = 15
        map(lambda city: setattr(city, 'human_spawn_boost', 15), friend.cities)

        message = self.game.lang['onFriendshipCreate']

        self.scene.notificationManager.add_notification(Notification(self.game, self.scene, message.format(self.name, friend.name)))
        self.scene.events.append(Log(message.format(self.name, friend.name)))
    
    def create_alliance(self, ally):
        alliance_name = random.choice(self.scene.all_alliances)
        times_fail = 0

        for alliance_name in [i.name for i in self.scene.countries]:
            alliance_name = random.choice(self.scene.all_alliances)
            times_fail += 1

            if times_fail > 15:
                return
        
        allies = [self, ally]
        random_ally = random.choice(allies)
        
        alliance_territory_color = random_ally.territory_color
        alliance_color = random_ally.color
        alliance = Alliance(self.game, self.scene, alliance_name, alliance_territory_color, alliance_color)
        alliance.add_ally(self)
        alliance.add_ally(ally)

        for ally in allies:
            for land in ally.territory:
                alliance.add_territory(land)
            map(lambda land: alliance.add_territory(land), ally.territory)

        self.agression[ally] = 0.0
        ally.agression[self] = 0.0
        self.allies.append(ally)
        ally.allies.append(self)

        self.alliances.append(alliance)
        ally.alliances.append(alliance)

        message = self.game.lang['onAllianceCreate']

        self.scene.notificationManager.add_notification(Notification(self.game, self.scene, message.format(self.name, ally.name, alliance.name)))
        self.scene.events.append(Log(message.format(self.name, ally.name, alliance.name)))
        self.scene.alliances.append(alliance)
        
    def declare_war(self, enemy):
        city = random.choice(enemy.cities + [enemy.capital])
        
        # Create a new War object
        war = War(game=self.game, scene=self.scene, participants=[self, enemy])

        battle = Battle(game=self.game, scene=self.scene, war=war, city=city)
        war.add_battle(battle)

        # Add the War to the list of wars for both countries
        self.wars.append(war)
        enemy.wars.append(war)

        # Change the 'in_war' state for both countries
        self.states['in_war'] = True
        enemy.states['in_war'] = True

        # Change the 'in_war' state for 30% of the population of both countries
        self.change_population_state(states=['current_war', 'current_battle'], values=[war, battle], percentage_of_people=40)
        enemy.change_population_state(states=['current_war', 'current_battle'], values=[war, battle], percentage_of_people=40)

        # Check if any allies will join the war
        for ally in self.allies:
            if ally not in war.participants and ally not in enemy.allies and random.random() < 0.75 * self.game.game_speed:
                ally.states['in_war'] = True
                war.add_participant(participant=ally)
                ally.wars.append(war)
                ally.change_population_state(states=['current_war', 'current_battle'], values=[war, battle], percentage_of_people=20)

        for ally in enemy.allies:
            if ally not in war.participants and ally not in self.allies and random.random() < 0.75 * self.game.game_speed:
                ally.states['in_war'] = True
                war.add_participant(participant=ally)
                ally.wars.append(war)
                ally.change_population_state(states=['current_war', 'current_battle'], values=[war, battle], percentage_of_people=20)
        
        self.scene.wars.append(war)

        # Send a notification that the war has been declared
        message = self.game.lang['onWarDeclare']

        self.scene.notificationManager.add_notification(Notification(self.game, self.scene, message.format(self.name, enemy.name)))
        self.scene.events.append(Log(message.format(self.name, enemy.name)))
    
    def in_war_with(self, country):
        for war in self.wars:
            if country in war.participants:
                return True
        
        return False

    def in_war(self):
        if len(self.wars) > 0:
            return True
        
        return False
        
    def is_claimed_territory(self, x, y):
        zone_x = (x // self.scene.land_cell_size) * self.scene.land_cell_size
        zone_y = (y // self.scene.land_cell_size) * self.scene.land_cell_size
        
        for land in self.territory:
            if (land.rect.x, land.rect.y) == (zone_x, zone_y):
                return True
        
        return False

    def is_on_enemy_territory(self, x, y):
        for country in self.scene.countries:
            if country != self and country.is_claimed_territory(x, y):
                return True
        return False
    
    def is_neighbor(self, x, y):
        # Проверяем, есть ли соседняя территория по указанным координатам
        for other_land in self.territory:
            if other_land.rect.x == x and other_land.rect.y == y:
                if not self.is_on_enemy_territory(x, y):
                    return True
        return False

    def claim_territory(self, x, y):
        zone_x = (x // self.scene.land_cell_size) * self.scene.land_cell_size
        zone_y = (y // self.scene.land_cell_size) * self.scene.land_cell_size

        if zone_x <= x <= zone_x + self.scene.land_cell_size and zone_y <= y <= zone_y + self.scene.land_cell_size:
            self.territory.append(Land(self.game, self.scene, zone_x, zone_y, self))
        
        # self.create_borders()

    def remove_territory(self, x, y):
        zone_x = (x // self.scene.land_cell_size) * self.scene.land_cell_size
        zone_y = (y // self.scene.land_cell_size) * self.scene.land_cell_size

        for land in self.territory:
            if (land.rect.x, land.rect.y) == (zone_x, zone_y):
                if len(self.alliances) > 0:
                    for alliance in self.alliances:
                        if land in alliance.total_territory:
                            alliance.remove_territory(land)
                
                self.territory.pop(self.territory.index(land))
                return True
    
    def defended_from_enemy(self, war, battle, destroyer):
        for human in self.humans:
            if human.states['current_war'] == war and human.states['current_battle'] == battle:
                human.states['current_war'] = None
                human.states['current_battle'] = None
                human.states['return_to_homeland'] = True
        
        for human in destroyer.humans:
            if human.states['current_war'] == war and human.states['current_battle'] == battle:
                human.states['current_war'] = None
                human.states['current_battle'] = None
                human.states['return_to_homeland'] = True
        
        war.battles.remove(battle)
        war.end()
        
        message = self.game.lang['onWarLose']

        self.scene.notificationManager.add_notification(Notification(self.game, self.scene, message.format(destroyer.name, self.name)))
        self.scene.events.append(Log(message.format(destroyer.name, self.name)))
    
    def destroy_city(self, city, destroyer):
        self.hp = 1 if self.hp <= 0 else self.hp
        
        this_war = None
        this_battle = None
        
        for war in self.wars:
            if destroyer in war.participants and self in war.participants:
                this_war = war
                break
        
                
        for battle in this_war.battles:
            if destroyer in battle.participants and self in battle.participants:
                this_battle = battle
                break
        
        if not (this_war or this_battle):
            return False
        
        closest_territories, closest_humans = [], []
        distance_threshold = 80

        for land in self.territory:
            distance = math.sqrt((city.x - land.rect.x)**2 + (city.y - land.rect.y)**2)
            if distance < distance_threshold:
                closest_territories.append(land)

        for human in self.humans:
            distance = math.sqrt((city.x - human.x)**2 + (city.y - human.y)**2)
            if distance < distance_threshold:
                closest_humans.append(human)
        
        if city == self.capital:
            city.country = destroyer
            city.color = destroyer.color

            if city in self.cities:
                self.cities.remove(city)
                
            if not city in destroyer.cities:
                destroyer.cities.append(city)

            for land in closest_territories:
                land.country = destroyer
                land.color = destroyer.territory_color
                land.surface.set_alpha(128)
                land.surface.fill(land.color)
                self.territory.remove(land)
                destroyer.territory.append(land)

            for human in closest_humans:
                if human.states['current_war'] == this_war:
                    human.states['current_war'] = None
                    human.states['return_to_homeland'] = True
                
                human.country = destroyer
                human.color = destroyer.color
                self.humans.remove(human)
                destroyer.humans.append(human)

            for human in self.humans:
                if human.states['current_war'] == this_war and human.states['current_battle'] == this_battle:
                    human.states['current_war'] = None
                    human.states['current_battle'] = None
                    human.states['return_to_homeland'] = True
                    human.step = 4

            for human in destroyer.humans:
                if human.states['current_war'] == this_war and human.states['current_battle'] == this_battle:
                    human.states['current_war'] = None
                    human.states['current_battle'] = None
                    human.states['return_to_homeland'] = True
                    human.step = 4

            for ally in self.allies:
                if ally.in_war_with(destroyer):
                    for human in ally.humans:
                        if human.states['current_war'] == this_war and human.states['current_battle'] == this_battle:
                            human.states['in_war'] = False
                            human.states['return_to_homeland'] = True
                            human.step = 4

                            ally.states['in_war'] = False
                            ally.states['return_to_homeland'] = True
                            ally.agression[destroyer] = 0.0

            for ally in destroyer.allies:
                if ally.in_war_with(self):
                    for human in ally.humans:
                        if human.states['current_war'] == this_war and human.states['current_battle'] ==this_battle:
                            human.states['current_war'] = None
                            human.states['current_battle'] = None
                            human.states['return_to_homeland'] = True
                            human.step = human.size

                            ally.states['in_war'] = False
                            ally.states['return_to_homeland'] = True
                            ally.agression[self] = 0.0

        else:
            city = self.capital
            city.country = destroyer
            city.color = destroyer.color
            city.isCapital = False

            city.name = city.country.name if city.isCapital else self.game.lang['cityRenderMessage']

            destroyer.cities.append(city)
            new_capital = random.choice(self.cities)
            new_capital.isCapital = True

            for land in closest_territories:
                land.country = destroyer
                land.color = destroyer.territory_color
                land.surface.set_alpha(128)
                land.surface.fill(land.color)
                self.territory.remove(land)
                destroyer.territory.append(land)

            for human in closest_humans:
                human.country = destroyer
                human.color = destroyer.color
                self.humans.remove(human)
                destroyer.humans.append(human)

            for human in self.humans:
                if human.states['current_war'] == this_war and human.states['current_battle'] == this_battle:
                    human.states['current_war'] = None
                    human.states['current_battle'] = None
                    human.states['return_to_homeland'] = True
                    human.step = 4

            for human in destroyer.humans:
                if human.states['current_war'] == this_war and human.states['current_battle'] == this_battle:
                    human.states['current_war'] = None
                    human.states['current_battle'] = None
                    human.states['return_to_homeland'] = True
                    human.step = 4

            for ally in self.allies:
                if ally.in_war_with(destroyer):
                    for human in ally.humans:
                        if human.states['current_war'] == this_war and human.states['current_battle'] == this_battle:
                            human.states['in_war'] = False
                            human.states['return_to_homeland'] = True
                            human.step = 4

                            ally.states['in_war'] = False
                            ally.states['return_to_homeland'] = True
                            ally.agression[destroyer] = 0.0

            for ally in destroyer.allies:
                if ally.in_war_with(self):
                    for human in ally.humans:
                        if human.states['current_war'] == this_war and human.states['current_battle'] == this_battle:
                            human.states['current_war'] = None
                            human.states['current_battle'] = None
                            human.states['return_to_homeland'] = True
                            human.step = human.size

                            ally.states['in_war'] = False
                            ally.states['return_to_homeland'] = True
                            ally.agression[self] = 0.0

        message = self.game.lang['onCityCapture']
            
        self.agression[destroyer] = 30.0
        destroyer.agression[self] = 30.0

        self.scene.notificationManager.add_notification(Notification(self.game, self.scene, message.format(destroyer.name, self.name)))
        self.scene.events.append(Log(message.format(destroyer.name, self.name)))

    # def destroy_city(self, city, destroyer):
    #     if self.hp <= 0:
    #         self.hp = 1

    #     if isinstance(destroyer, Human) or isinstance(destroyer, King):
    #         destroyer = destroyer.country

    #     my_battle = None

    #     for war in self.wars:
    #         if destroyer in war.participants and self in war.participants:
    #             for battle in war.battles:
    #                 if battle.place == city:
    #                     my_battle = battle
    #                     self.states['in_war'] = False
    #                     self.agression[destroyer] = 0.0
    #                     war.battles.remove(battle)

    #     my_war = None
    #     for war in self.scene.wars:
    #         if self in war.participants and destroyer in war.participants:
    #             my_war = war

    #     if not my_battle or not my_war:
    #         return

    #     city = my_battle.place

    #     closest_territories, closest_humans = [], []
    #     distance_threshold = 80

    #     for land in self.territory:
    #         distance = math.sqrt((city.x - land.rect.x)**2 + (city.y - land.rect.y)**2)
    #         if distance < distance_threshold:
    #             closest_territories.append(land)

    #     for human in self.humans:
    #         distance = math.sqrt((city.x - human.x)**2 + (city.y - human.y)**2)
    #         if distance < distance_threshold:
    #             closest_humans.append(human)

    #     if city.country == self:
    #         if not city.isCapital:
    #             city.country = destroyer
    #             city.color = destroyer.color

    #             self.cities.remove(city)
    #             destroyer.cities.append(city)

    #             for land in closest_territories:
    #                 land.country = destroyer
    #                 land.color = destroyer.territory_color
    #                 land.surface.set_alpha(128)
    #                 land.surface.fill(land.color)
    #                 self.territory.remove(land)
    #                 destroyer.territory.append(land)

    #             for human in closest_humans:
    #                 if human.states['in_war']:
    #                     human.states['in_war'] = False
    #                     human.states['return_to_homeland'] = True
    #                 human.country = destroyer
    #                 human.color = destroyer.color
    #                 self.humans.remove(human)
    #                 destroyer.humans.append(human)

    #             for human in self.humans:
    #                 if human.states['current_war'] == my_war and human.states['current_battle'] == my_battle:
    #                     human.states['current_war'] = None
    #                     human.states['current_battle'] = None
    #                     human.states['return_to_homeland'] = True
    #                     human.step = 4

    #             for human in destroyer.humans:
    #                 if human.states['current_war'] == my_war and human.states['current_battle'] == my_battle:
    #                     human.states['current_war'] = None
    #                     human.states['current_battle'] = None
    #                     human.states['return_to_homeland'] = True
    #                     human.step = 4

    #             for ally in self.allies:
    #                 if ally.in_war_with(destroyer):
    #                     for human in ally.humans:
    #                         if human.states['current_war'] == my_war and human.states['current_battle'] == my_battle:
    #                             human.states['in_war'] = False
    #                             human.states['return_to_homeland'] = True
    #                             human.step = 4

    #                             ally.states['in_war'] = False
    #                             ally.states['return_to_homeland'] = True
    #                             ally.agression[destroyer] = 0.0

    #             for ally in destroyer.allies:
    #                 if ally.in_war_with(self):
    #                     for human in ally.humans:
    #                         if human.states['current_war'] == my_war and human.states['current_battle'] == my_battle:
    #                             human.states['current_war'] = None
    #                             human.states['current_battle'] = None
    #                             human.states['return_to_homeland'] = True
    #                             human.step = human.size

    #                             ally.states['in_war'] = False
    #                             ally.states['return_to_homeland'] = True
    #                             ally.agression[self] = 0.0

    #             message = self.game.lang['onCityCapture']

    #             self.scene.notificationManager.add_notification(Notification(self.game, self.scene, message.format(destroyer.name, self.name)))
    #             self.scene.events.append(Log(message.format(destroyer.name, self.name)))

    #         else:
    #             if len(self.cities) > 0:
    #                 city = self.capital
    #                 city.country = destroyer
    #                 city.color = destroyer.color
    #                 city.isCapital = False

    #                 city.name = city.country.name if city.isCapital else self.game.lang['cityRenderMessage']

    #                 destroyer.cities.append(city)
    #                 new_capital = random.choice(self.cities)
    #                 new_capital.isCapital = True

    #                 for land in closest_territories:
    #                     land.country = destroyer
    #                     land.color = destroyer.territory_color
    #                     land.surface.set_alpha(128)
    #                     land.surface.fill(land.color)
    #                     self.territory.remove(land)
    #                     destroyer.territory.append(land)

    #                 for human in closest_humans:
    #                     human.country = destroyer
    #                     human.color = destroyer.color
    #                     self.humans.remove(human)
    #                     destroyer.humans.append(human)

    #                 for human in self.humans:
    #                     if human.states['current_war'] == my_war and human.states['current_battle'] == my_battle:
    #                         human.states['current_war'] = None
    #                         human.states['current_battle'] = None
    #                         human.states['return_to_homeland'] = True
    #                         human.step = 4

    #                 for human in destroyer.humans:
    #                     if human.states['current_war'] == my_war and human.states['current_battle'] == my_battle:
    #                         human.states['current_war'] = None
    #                         human.states['current_battle'] = None
    #                         human.states['return_to_homeland'] = True
    #                         human.step = 4

    #                 for ally in self.allies:
    #                     if ally.in_war_with(destroyer):
    #                         for human in ally.humans:
    #                             if human.states['current_war'] == my_war and human.states['current_battle'] == my_battle:
    #                                 human.states['in_war'] = False
    #                                 human.states['return_to_homeland'] = True
    #                                 human.step = 4

    #                                 ally.states['in_war'] = False
    #                                 ally.states['return_to_homeland'] = True
    #                                 ally.agression[destroyer] = 0.0

    #                 for ally in destroyer.allies:
    #                     if ally.in_war_with(self):
    #                         for human in ally.humans:
    #                             if human.states['current_war'] == my_war and human.states['current_battle'] == my_battle:
    #                                 human.states['current_war'] = None
    #                                 human.states['current_battle'] = None
    #                                 human.states['return_to_homeland'] = True
    #                                 human.step = human.size

    #                                 ally.states['in_war'] = False
    #                                 ally.states['return_to_homeland'] = True
    #                                 ally.agression[self] = 0.0

    #                 message = self.game.lang['onCapitalCapture']

    #                 self.scene.notificationManager.add_notification(Notification(self.game, self.scene, message.format(destroyer.name, self.name)))
    #                 self.scene.events.append(Log(message.format(destroyer.name, self.name)))

    #             else:
    #                 self.destroy()

    #     else:
    #         if self.hp > 0:
    #             self.hp -= city.hp

    #             if self.hp <= 0:
    #                 self.destroy()

    #             message = self.game.lang['onCityAttack']

    #             self.scene.notificationManager.add_notification(Notification(self.game, self.scene, message.format(destroyer.name, self.name)))
    #             self.scene.events.append(Log(message.format(destroyer.name, self.name)))


    def destroy(self, destroyer):
        if isinstance(destroyer, Human) or isinstance(destroyer, King):
            destroyer = destroyer.country
        
        for human in destroyer.humans:
            human.states['return_to_homeland'] = True
            human.states['current_war'] = None
            human.states['current_battle'] = None
        
        destroyer.states['in_war'] = False
        destroyer.states['return_to_homeland'] = True
        destroyer.agression[self] = 0.0
        destroyer.agression.pop(self, None)
        
        this_war = None
        this_battle = None
        
        for war in self.scene.wars:
            if self in war.participants and destroyer in war.participants:
                this_war = war
        
        if not this_war:
            return
        
        for battle in this_war.battles:
            if self in battle.participants and destroyer in battle.participants:
                this_battle = battle
        
        for human in self.humans:
            human.country = destroyer
            human.color = destroyer.color
            human.step = human.size
            human.states['current_war'] = None
            human.states['current_battle'] = None

            self.humans.remove(human)
            destroyer.humans.append(human)
            human.states['return_to_homeland'] = True

        for city in self.cities:
            city.country = destroyer
            city.color = destroyer.color
            
            self.cities.remove(city)
            destroyer.cities.append(city)
        
        self.capital.country = destroyer
        self.capital.color = destroyer.color
        self.capital.isCapital = False

        self.capital.name = self.capital.country.name if self.capital.isCapital else self.game.lang['cityRenderMessage']

        destroyer.cities.append(self.capital)

        for land in self.territory:
            land.color = destroyer.territory_color
            land.country = destroyer
            land.surface.set_alpha(128)
            land.surface.fill(land.color)
            destroyer.territory.append(land)
        
        self.territory = []
        
        for ally in destroyer.allies: 
            if engine.in_dict(self, ally.agression):
                ally.agression.pop(self, None)
        
        for ally in self.allies:
            if engine.in_dict(self, ally.agression):
                ally.agression.pop(self, None)

        for ally in self.allies:
            ally.allies.remove(self)
            for alliance in ally.alliances:
                if len(alliance.allies) > 2:
                    if self in alliance.allies:
                        alliance.allies.remove(self)
                
                else:
                    for ally1 in alliance.allies:
                        if self in alliance.allies:
                            ally1.alliances.remove(alliance)
    
                            if alliance in self.scene.alliances:
                                self.scene.alliances.remove(alliance)

                for human in ally.humans:
                    if human.states['current_war'] == this_war and human.states['current_battle'] == this_battle:
                        human.states['current_war'] = None
                        human.states['current_battle'] = None
                        human.states['return_to_homeland'] = True
                        human.step = 4
        
        this_battle.end()
        this_war.end()

        message = self.game.lang['onCountryDestroy']
        
        self.scene.notificationManager.add_notification(Notification(self.game, self.scene, message.format(self.name, destroyer.name)))
        self.scene.events.append(Log(message.format(self.name, destroyer.name)))

        self.scene.countries.remove(self)
        del self
    
    def __repr__(self):
        return f'{self.name} ({len(self.humans) + len([self.king])} population)'