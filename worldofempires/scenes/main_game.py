from engine.managers.sceneManager import Scene
from engine.managers.cameraManager import CameraManager

from ..custom_managers.notificationManager import NotificationManager, Notification
from ..custom_managers.terrainGenerator import TerrainGenerator, Terrain, layers, pilImageToSurface

from ..assets.city import City
from ..assets.land import Land
from ..assets.partnership import Partnership
from ..assets.alliance import Alliance
from ..assets.human import Human
from ..assets.king import King
from ..assets.war import War
from ..assets.battle import Battle
from ..assets.border import Border
from ..assets.country import Country
from ..layers.sidebar import Sidebar

from ..assets.tree import Tree
from ..assets.stone import Stone
from ..assets.iron_ore import IronOre
from ..assets.silver_ore import SilverOre
from ..assets.gold_ore import GoldOre

from engine.classes.button import Button

# from worldofempires.assets.country import Country
# from worldofempires.assets.city import City

import pygame
import random

available_resources = [Tree, Stone, IronOre, SilverOre, GoldOre]

class GameScene(Scene):
    def __init__(self, game, name):
        super().__init__(game, name)
    
        self.cell_size: int = 5
        self.land_cell_size: int = 20

        self.all_countries: list[str] = self.game.lang['countries']
        self.all_alliances: list[str] = self.game.lang['alliances']
        
        self.terrain = None
        self.resources = []

        self.countries: list = []
        self.cities: list = []
        self.wars: list = []
        self.alliances: list = []
        self.events: list = []
        
        self.notificationManager = NotificationManager()
        self.terrainGenerator = TerrainGenerator(game, self)
        self.cameraManager = CameraManager(game=self.game,
                                           scene=self,
                                           x=0, y=0,
                                           width=self.game.width,
                                           height=self.game.height,
                                           align='tl')
        
        self.chosen_countries = []
        self.already_pressed = False
        
        self.states = {'is_starting_a_war': False,
                       'is_creating_an_alliance': False}
        
        self.sidebar = Sidebar(self.game, self, 'right')
        self.settings = {}
        
        self.scroll_x = 0
        self.scroll_y = 0
        
        self.current_mouse_pos = pygame.mouse.get_pos()
        self.previous_mouse_pos = self.current_mouse_pos
        self.is_scrolling = False
        self.legend_visible = True
        self.notifications_visible = True
    
    def fill_sidebar(self):
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+40,
                        width=150, height=20,
                        align="center",
                        text=f"{self.game.lang.get('start_war')}",
                        color=(0, 0, 0),
                        fontsize=14,
                        normalcolor=(255, 255, 255),
                        hovercolor=(220, 220, 220),
                        pressedcolor=(190, 190, 190))
        
        self.sidebar.add_object(button, 1)
        del button
        
        def start_war():
            
            if not self.states['is_starting_a_war']:
                if len(self.chosen_countries) == 2:
                    if not (self.chosen_countries[0].in_war_with(self.chosen_countries[1])):
                        self.chosen_countries[0].declare_war(self.chosen_countries[1])
                        self.states['is_starting_a_war'] = True
                
                else:
                    self.notificationManager.add_notification(Notification(self.game,
                                                                           self,
                                                                           text=f"{self.game.lang.get('need_choose_2_countries')}",
                                                                           time=3,
                                                                           side='cb',
                                                                           align='center',
                                                                           color=(255, 0, 0),
                                                                           size=36))
            
            self.chosen_countries = [] if self.states['is_starting_a_war'] == True else self.chosen_countries
            self.states['is_starting_a_war'] = True if self.states['is_starting_a_war'] == False else False
            text = f"{self.game.lang.get('start_war')}" if self.states['is_starting_a_war'] == False else f"{self.game.lang.get('cancel')}"
            self.sidebar.get_object(1).change_text(text)
        
        self.sidebar.get_object(1).onclick = lambda: start_war()
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+65,
                        width=150, height=20,
                        align="center",
                        text=f"{self.game.lang.get('select_all')}",
                        color=(0, 0, 0),
                        fontsize=14,
                        normalcolor=(255, 255, 255),
                        hovercolor=(220, 220, 220),
                        pressedcolor=(190, 190, 190))
        
        self.sidebar.add_object(button, 2)
        del button
        
        def select_deselect_all():
            if len(self.chosen_countries) == 0:
                if len(self.countries) > 0:
                    for country in self.countries:
                        if not country in self.chosen_countries:
                            self.chosen_countries.append(country)
                            
                    self.sidebar.get_object(2).change_text(f"{self.game.lang.get('cancel')}")
                    
                else:
                    self.chosen_countries = []
                    self.sidebar.get_object(2).change_text(f"{self.game.lang.get('select_all')}")
                
                
            elif len(self.chosen_countries) == len(self.countries):
                self.chosen_countries = []
                self.sidebar.get_object(2).change_text(f"{self.game.lang.get('cancel')}")
            
            else:
                if len(self.countries) > 0:
                    for country in self.countries:
                        if not country in self.chosen_countries:
                            self.chosen_countries.append(country)
                            
                    self.sidebar.get_object(2).change_text(f"{self.game.lang.get('cancel')}")
                    
                else:
                    self.chosen_countries = []
                    self.sidebar.get_object(2).change_text(f"{self.game.lang.get('select_all')}")
                
                
                # self.sidebar.get_object(2).change_text("Deselect all")

        self.sidebar.get_object(2).onclick = lambda: select_deselect_all()

        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+90,
                        width=150, height=20,
                        align="center",
                        text=f"{self.game.lang.get('spawn_human')}",
                        color=(0, 0, 0),
                        fontsize=14,
                        normalcolor=(255, 255, 255),
                        hovercolor=(220, 220, 220),
                        pressedcolor=(190, 190, 190))
        
        self.sidebar.add_object(button, 3)
        del button
        
        def spawn_human():
            if len(self.chosen_countries) <= 0:
                self.notificationManager.add_notification(Notification(self.game,
                                                                       self,
                                                                       text=f"{self.game.lang.get('need_choose_any_country')}",
                                                                       time=3,
                                                                       side='cb',
                                                                       align='center',
                                                                       color=(255, 0, 0),
                                                                       size=36))
            for country in self.chosen_countries:
                random.choice(country.cities + [country.capital]).spawn_human()

        self.sidebar.get_object(3).onclick = lambda: spawn_human()
        self.sidebar.get_object(3).multipress = True

        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+115,
                        width=150, height=20,
                        align="center",
                        text=f"{self.game.lang.get('spawn_country')}",
                        color=(0, 0, 0),
                        fontsize=14,
                        normalcolor=(255, 255, 255),
                        hovercolor=(220, 220, 220),
                        pressedcolor=(190, 190, 190))
        
        self.sidebar.add_object(button, 4)
        del button
        
        def create_country():
            self.create_country()

        self.sidebar.get_object(4).onclick = lambda: create_country()
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+140,
                        width=150, height=20,
                        align="center",
                        text=f"{self.game.lang.get('create_alliance')}",
                        color=(0, 0, 0),
                        fontsize=14,
                        normalcolor=(255, 255, 255),
                        hovercolor=(220, 220, 220),
                        pressedcolor=(190, 190, 190))
        
        self.sidebar.add_object(button, 5)
        del button
        
        def create_alliance():
            if not self.states['is_creating_an_alliance']:
                if len(self.chosen_countries) == 2:
                    if not (self.chosen_countries[0].in_war_with(self.chosen_countries[1])):
                        self.chosen_countries[0].create_alliance(self.chosen_countries[1])
                        self.states['is_creating_an_alliance'] = True
                
                else:
                    self.notificationManager.add_notification(Notification(self.game,
                                                                           self,
                                                                           text=f"{self.game.lang.get('need_choose_2_countries')}",
                                                                           time=3,
                                                                           side='cb',
                                                                           align='center',
                                                                           color=(255, 0, 0),
                                                                           size=36))
            
            self.chosen_countries = [] if self.states['is_creating_an_alliance'] == True else self.chosen_countries
            self.states['is_creating_an_alliance'] = True if self.states['is_creating_an_alliance'] == False else False
            fontsize = 14 if self.states['is_creating_an_alliance'] == False else 10 
            text = f"{self.game.lang.get('create_alliance')}" if self.states['is_creating_an_alliance'] == False else f"{self.game.lang.get('cancel')}"
            self.sidebar.get_object(5).change_text(text)
            self.sidebar.get_object(5).change_font(None, fontsize)

        self.sidebar.get_object(5).onclick = lambda: create_alliance()
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+165,
                        width=150, height=20,
                        align="center",
                        text=f"{self.game.lang.get('destroy_country')}",
                        color=(255, 0, 0),
                        fontsize=14,
                        normalcolor=(255, 255, 255),
                        hovercolor=(220, 220, 220),
                        pressedcolor=(190, 190, 190))
        
        self.sidebar.add_object(button, 6)
        del button
        
        def destroy_country():
            if len(self.chosen_countries) <= 0:
                self.notificationManager.add_notification(Notification(self.game,
                                                                       self,
                                                                       text=f"{self.game.lang.get('need_choose_any_country')}",
                                                                       time=3,
                                                                       side='cb',
                                                                       align='center',
                                                                       color=(255, 0, 0),
                                                                       size=36))
            for country in self.chosen_countries:
                self.chosen_countries.remove(country)
                self.countries.remove(country)
                
                for war in self.wars:
                    if country in war.participants:
                        war.participants.remove(country)
                        if len(war.participants) <= 1:
                            war.end()
                
                for another_country in self.countries:
                    if another_country.allied_with(country):
                        another_country.allies.remove(country)
                
                for alliance in self.alliances:
                    if country in alliance.allies:
                        alliance.remove_ally(country)
                
                del country

        self.sidebar.get_object(6).onclick = lambda: destroy_country()
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+190,
                        width=150, height=20,
                        align="center",
                        text=f"{self.game.lang.get('time_label')} 1x",
                        color=(0, 0, 0),
                        fontsize=14,
                        normalcolor=(255, 255, 255),
                        hovercolor=(220, 220, 220),
                        pressedcolor=(190, 190, 190))
        
        self.sidebar.add_object(button, 7)
        del button
        
        def change_game_speed():
            match self.game.game_speed:
                case 1:
                    self.game.game_speed = 2
                    self.sidebar.get_object(7).change_text(f"{self.game.lang.get('time_label')} {self.game.game_speed}x")
                case 2:
                    self.game.game_speed = 4
                    self.sidebar.get_object(7).change_text(f"{self.game.lang.get('time_label')} {self.game.game_speed}x")
                case 4:
                    self.game.game_speed = 8
                    self.sidebar.get_object(7).change_text(f"{self.game.lang.get('time_label')} {self.game.game_speed}x")
                case 8:
                    self.game.game_speed = 16
                    self.sidebar.get_object(7).change_text(f"{self.game.lang.get('time_label')} {self.game.game_speed}x")
                case 16:
                    self.game.game_speed = 32
                    self.sidebar.get_object(7).change_text(f"{self.game.lang.get('time_label')} {self.game.game_speed}x")
                case 32:
                    self.game.game_speed = 64
                    self.sidebar.get_object(7).change_text(f"{self.game.lang.get('time_label')} {self.game.game_speed}x")
                case 64:
                    self.game.game_speed = 0.25
                    self.sidebar.get_object(7).change_text(f"{self.game.lang.get('time_label')} {self.game.game_speed}x")
                case 0.25:
                    self.game.game_speed = 0.5
                    self.sidebar.get_object(7).change_text(f"{self.game.lang.get('time_label')} {self.game.game_speed}x")
                case 0.5:
                    self.game.game_speed = 1
                    self.sidebar.get_object(7).change_text(f"{self.game.lang.get('time_label')} {self.game.game_speed}x")
                    
            fontsize = 14
            self.sidebar.get_object(7).change_font(None, fontsize)
        
        self.sidebar.get_object(7).onclick = lambda: change_game_speed()
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+240,
                        width=150, height=20,
                        align="center",
                        text=f"{self.game.lang.get('hide_legend_label')}",
                        color=(0, 0, 0),
                        fontsize=14,
                        normalcolor=(255, 255, 255),
                        hovercolor=(220, 220, 220),
                        pressedcolor=(190, 190, 190))
        
        self.sidebar.add_object(button, 8)
        del button
        
        def hide_show_legend():
            if self.legend_visible:
                self.legend_visible = False
                self.sidebar.get_object(8).change_text(f"{self.game.lang.get('show_legend_label')}")
            else:
                self.legend_visible = True
                self.sidebar.get_object(8).change_text(f"{self.game.lang.get('hide_legend_label')}")
                    
            fontsize = 14
            self.sidebar.get_object(8).change_font(None, fontsize)
        
        self.sidebar.get_object(8).onclick = lambda: hide_show_legend()
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+215,
                        width=150, height=20,
                        align="center",
                        text=f"{self.game.lang.get('hide_notifications_label')}",
                        color=(0, 0, 0),
                        fontsize=14,
                        normalcolor=(255, 255, 255),
                        hovercolor=(220, 220, 220),
                        pressedcolor=(190, 190, 190))
        
        self.sidebar.add_object(button, 9)
        del button
        
        def hide_show_notifications():
            if self.notifications_visible:
                self.notifications_visible = False
                self.sidebar.get_object(9).change_text(f"{self.game.lang.get('show_notifications_label')}")
            else:
                self.notifications_visible = True
                self.sidebar.get_object(9).change_text(f"{self.game.lang.get('hide_notifications_label')}")
                    
            fontsize = 14
            self.sidebar.get_object(9).change_font(None, fontsize)
        
        self.sidebar.get_object(9).onclick = lambda: hide_show_notifications()
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=self.game.height-20,
                        width=150, height=20,
                        align="center",
                        text=f"{self.game.lang.get('main_menu')}",
                        color=(0, 0, 0),
                        fontsize=14,
                        normalcolor=(255, 255, 255),
                        hovercolor=(220, 220, 220),
                        pressedcolor=(190, 190, 190))
        
        self.sidebar.add_object(button, 25)
        del button
        
        def start_main_menu():
            self.__init__(self.game, "game_process")
            
            def switch_to_menu():
                self.game.sceneManager.get_scene('loading_screen').__init__(self.game, 'loading_screen')
                self.game.sceneManager.get_scene('menu').__init__(self.game, 'menu')
                self.game.game_speed = 1
                self.game.sceneManager.switch_scene('menu')
            
            self.game.sceneManager.get_scene('loading_screen').custom_action = switch_to_menu
            self.game.sceneManager.switch_scene('loading_screen')

        self.sidebar.get_object(25).onclick = lambda: start_main_menu()
    
    def generate_terrain(self):
        # scale = random.randint(75, 100)
        seed = 0
        sea_level = random.randint(100, 125)
        # persistence = random.randint(55, 100)
        persistence = 55
        lacunarity = 25
        octaves = 6
        
        width = self.settings.get('map').get('width')
        height = self.settings.get('map').get('height')
        zoom = self.settings.get('map').get('zoom')
        sea_level = self.settings.get('map').get('sea_level')
        seed = self.settings.get('map').get('seed')
            
        shape = (height, width)
        
        noise_array = self.terrainGenerator.generate(scale=zoom,
                                                      shape=shape,
                                                      octaves=octaves,
                                                      persistence=persistence,
                                                      lacunarity=lacunarity,
                                                      seed=seed)

        color_array = self.terrainGenerator.assign_colors(layers, noise_array, sea_level)
        image = self.terrainGenerator.color_array_to_image(color_array)
        landscape = pilImageToSurface(image)
        
        self.resources_spawn = {}
        
        terrain = Terrain(game=self.game, scene=self, x=0, y=0, image=image, landscape=landscape, width=width, height=height, zoom=zoom)
        return terrain
    
    def generate_resources(self, resource=None, dist=50):
        resources_good_place = [(181, 202, 116),
                            (116, 186, 94),
                            (80, 143, 61),
                            (50, 89, 38)]
        resources_fail = 0
        
        if resource == None: target_resource = random.choice(available_resources)
        else: target_resource = resource

        resource = None
        spawn_chance = ((100 - self.resources_spawn.get(target_resource).get('spawn_chance')) / self.game.game_speed)
        min_dist = self.resources_spawn.get(target_resource).get('min_dist')
        max_dist = self.resources_spawn.get(target_resource).get('max_dist')
        
        while True:
            if random.random() < 1 / spawn_chance / self.game.fps:
                x, y = random.randint(0, self.terrain.width), random.randint(0, self.terrain.height)
                if self.terrain.get_at((x, y)) in resources_good_place:
                    is_close_to_other_resource = False
                    for some_resource in list(filter(lambda resource: isinstance(resource, target_resource), self.resources)):
                        if ((x - some_resource.x) ** 2 + (y - some_resource.y) ** 2) ** 0.5 < random.randint(min_dist, max_dist):
                            is_close_to_other_resource = True
                            resources_fail += 1
                            if resources_fail > 100:
                                return
                            break
                    
                    if not is_close_to_other_resource:
                        resource = target_resource(game=self.game,
                                    scene=self,
                                    x=x,
                                    y=y)
                        self.resources.append(resource)

    # def generate_resources(self):
    #     resource_good_place = [(181, 202, 116),
    #                         (116, 186, 94),
    #                         (80, 143, 61),
    #                         (50, 89, 38)]
    #     trees_fail = 0

    #     while True:
    #         x, y = random.randint(0, self.terrain.width), random.randint(0, self.terrain.height)
    #         if self.terrain.get_at((x, y)) in trees_good_place:
    #             is_close_to_other_tree = False
    #             for tree in list(filter(lambda resource: isinstance(resource, Tree), self.resources)):
    #                 if ((x - tree.x) ** 2 + (y - tree.y) ** 2) ** 0.5 < 50:
    #                     is_close_to_other_tree = True
    #                     trees_fail += 1
    #                     if trees_fail > 1000:
    #                         return
    #                     break
    #             if not is_close_to_other_tree:
    #                 tree = Tree(game=self.game,
    #                             scene=self,
    #                             x=x,
    #                             y=y)
    #                 self.resources.append(tree)
                    
    # def generate_stones(self):
    #     stones_good_place = [(181, 202, 116),
    #                         (116, 186, 94),
    #                         (80, 143, 61),
    #                         (50, 89, 38)]
    #     stones_fail = 0

    #     while True:
    #         x, y = random.randint(0, self.terrain.width), random.randint(0, self.terrain.height)
    #         if self.terrain.get_at((x, y)) in stones_good_place:
    #             is_close_to_other_stone = False
    #             for stone in list(filter(lambda resource: isinstance(resource, Stone), self.resources)):
    #                 if ((x - stone.x) ** 2 + (y - stone.y) ** 2) ** 0.5 < 100:
    #                     is_close_to_other_stone = True
    #                     stones_fail += 1
    #                     if stones_fail > 1000:
    #                         return
    #                     break
    #             if not is_close_to_other_stone:
    #                 stone = Stone(game=self.game,
    #                             scene=self,
    #                             x=x,
    #                             y=y)
    #                 self.resources.append(stone)
    
    def generate_resource(self, resource=None, dist=50):
        resources_good_place = [(181, 202, 116),
                            (116, 186, 94),
                            (80, 143, 61),
                            (50, 89, 38)]
        resources_fail = 0
        if resource == None: target_resource = random.choice(available_resources)
        else: target_resource = resource
        
        resource = None

        x, y = random.randint(0, self.terrain.width), random.randint(0, self.terrain.height)
        if self.terrain.get_at((x, y)) in resources_good_place:
            is_close_to_other_resource = False
            for some_resource in list(filter(lambda resource: isinstance(resource, target_resource), self.resources)):
                if ((x - some_resource.x) ** 2 + (y - some_resource.y) ** 2) ** 0.5 < dist:
                    is_close_to_other_resource = True
                    resources_fail += 1
                    if resources_fail > 1000:
                        return
                    break
            if not is_close_to_other_resource:
                resource = target_resource(game=self.game,
                            scene=self,
                            x=x,
                            y=y)
                self.resources.append(resource)
    
    def new_generate_resources(self):
        resources_good_place = [(181, 202, 116),
                            (116, 186, 94),
                            (80, 143, 61),
                            (50, 89, 38)]
        
        all_resources = list(self.resources_spawn.keys())
        resources_chances = []
        infos = list(self.resources_spawn.values())
                
        for info in infos:
            resources_chances.append(info['spawn_chance'])
        
        del infos
        
        for x in range(0, self.terrain.width, self.land_cell_size):
            for y in range(0, self.terrain.height, self.land_cell_size):
                resources_in_chunk = random.randint(0, 5)
                
                for _ in range(resources_in_chunk):
                    resource = random.choices(all_resources, resources_chances, k=1)[0]
                    resource_pos = (random.randint(x, x + self.land_cell_size),
                                    random.randint(y, y + self.land_cell_size))
                    
                    if random.random() < 1 / (100 - self.resources_spawn[resource]['spawn_chance']):
                        if self.terrain.get_at(resource_pos) in resources_good_place:  
                            resource = resource(game=self.game,
                                                scene=self,
                                                x=resource_pos[0],
                                                y=resource_pos[1])
                            self.resources.append(resource)
    
    def start(self):
        self.terrain = self.generate_terrain()
        
        self.resources_spawn[Tree] = self.settingsManager.settings.get('auto_spawn').get('terrain').get('trees')
        self.resources_spawn[Stone] = self.settingsManager.settings.get('auto_spawn').get('terrain').get('stone')
        self.resources_spawn[IronOre] = self.settingsManager.settings.get('auto_spawn').get('terrain').get('iron_ore')
        self.resources_spawn[SilverOre] = self.settingsManager.settings.get('auto_spawn').get('terrain').get('silver_ore')
        self.resources_spawn[GoldOre] = self.settingsManager.settings.get('auto_spawn').get('terrain').get('gold_ore')
        
        self.new_generate_resources()
        # self.generate_resources(Tree)
        # self.generate_resources(Stone)
        # self.generate_resources(IronOre)
        
        self.fill_sidebar()

        if self.settings == {}:
            countries_len = random.randint(self.game.settingsManager.settings.get('countries').get('min_value'), self.game.settingsManager.settings.get('countries').get('max_value'))
        else:
            countries_len = random.randint(self.settings.get('countries').get('min_value'), self.settings.get('countries').get('max_value'))
        
        for i in range(countries_len):
            self.create_country()
        
        self.chosen_country = self.countries[0]
    
    def spawn_country(self, name, x, y, color):
        country = Country(self.game, self, x, y, name, color)
        
        message = self.game.lang['onCountryCreate']
        
        self.notificationManager.add_notification(Notification(self.game, self, message.format(name)))
        self.cities.append(country.capital)
        self.countries.append(country)
    
    def country_exists(self, country):
        if country in self.countries:
            return True
        
        return False
        
    def draw_grid(self, cell_size, color):
        for x in range(0, self.game.width, cell_size):
            pygame.draw.line(self.game.screen, color, (x, 0), (x, self.game.height))
        for y in range(0, self.game.height, cell_size):
            pygame.draw.line(self.game.screen, color, (0, y), (self.game.width, y))
        
    def create_country(self):
        countryRandomName = random.choice(self.all_countries)

        while countryRandomName in [i.name for i in self.countries]:
            countryRandomName = random.choice(self.all_countries)
        
        name = countryRandomName
        color = random.randint(20, 230), random.randint(20, 230), random.randint(20, 230)
        
        spawn_successful = False
        
        while not spawn_successful:
            x = random.randint(20, self.terrain.width - 20)
            y = random.randint(20, self.terrain.height - 20)
            terrain_color = self.terrain.get_at((x, y))
            
            if terrain_color != (22, 156, 233) and terrain_color != (45, 166, 235) and terrain_color != (68, 176, 238) and terrain_color != (58, 29, 19) and terrain_color != (92, 61, 61) and terrain_color != (245, 240, 240):
                self.spawn_country(name, x, y, color)
                spawn_successful = True
    
    def draw_legend(self, country, y):
        if self.legend_visible:

            rect = pygame.draw.rect(self.game.screen, country.territory_color, (20, y + 30, 15, 15))
            pygame.draw.rect(self.game.screen, country.color, (20, y + 30, 15, 15), 2)

            if self.game.settingsManager.settings.get('countries').get('play_as_country'):
                if not self.countries[self.player] == country:
                    text = f'{country.name} ({len(country.humans) + len([country.king])}) (AI)'
                else:
                    text = f'{country.name} ({len(country.humans) + len([country.king])}) (Player)'
            else:
                text = f'{country.name} ({len(country.humans) + len([country.king])})'

            if country.hp < country.max_hp:
                text += f' (HP: {int(round(country.hp, 0))})'

            color = (0, 0, 0) if not (country in self.chosen_countries) else (0, 255, 0)

            self.textManager.render(surface=self.game.screen,
                                    x=rect.right + 5,
                                    y=rect.center[1],
                                    text=text,
                                    font=self.game.settingsManager.settings.get('font'),
                                    color=color,
                                    size=16,
                                    align='l')
    
    def draw_legend_alliance(self, alliance, y):
        if self.legend_visible:

            rect = pygame.draw.rect(self.game.screen, alliance.territory_color, (20, y + 30, 15, 15))
            pygame.draw.rect(self.game.screen, alliance.color, (20, y + 30, 15, 15), 2)
            alliance_allies = [ally.name for ally in alliance.allies]

            text = f'{alliance.name} ({", ".join(alliance_allies)})'

            self.textManager.render(surface=self.game.screen,
                                    x=rect.right + 5,
                                    y=rect.center[1],
                                    text=text,
                                    font=self.game.settingsManager.settings.get('font'),
                                    color=(0, 0, 0),
                                    size=16,
                                    align='l')
    
    def update(self):
        for country in self.countries:
            country.act()
            country.king.act()
            list(map(lambda human: human.act(), country.humans))

        for country in self.countries:
            list(map(lambda city: city.act(), country.cities))
            country.capital.act()

        if self.game.settingsManager.settings.get('auto_spawn').get('countries').get('enabled'):
            if random.uniform(0, 1) < self.game.settingsManager.settings.get('auto_spawn').get('countries').get('spawn_chance') / 15000 * self.game.game_speed:
                if len(self.countries) < self.game.settingsManager.settings.get('countries').get('max_value'):
                    self.create_country()
        
        def spawn_resources():
            if self.game.settingsManager.settings.get('auto_spawn').get('terrain').get('enabled'):
                resources = list(self.resources_spawn.keys())
                infos = list(self.resources_spawn.values())
                chances = []
                
                for info in infos:
                    chances.append(info['spawn_chance'])
                
                resource = random.choices(resources, chances, k=1)[0]

                if random.uniform(0, 1) < 1 / self.resources_spawn.get(resource).get('spawn_chance') * self.game.game_speed:
                    # self.generate_resource(resource, self.resources_spawn.get(resource).get('min_dist'))
                    pass
            
        self.eventManager.start_in_thread(spawn_resources)
        
        self.sidebar.update()
    
    def select_country(self, country):
        if country not in self.chosen_countries:
            self.chosen_countries.append(country)
            
            message = self.game.lang['onCountrySelect'].format(country.name)
            self.notificationManager.add_notification(Notification(game=self.game,
                                                                   scene=self,
                                                                   text=message, 
                                                                   side='rb', 
                                                                   align='r'))
        else:
            self.chosen_countries.remove(country)
            
            message = self.game.lang['onCountryDeselect'].format(country.name)
            self.notificationManager.add_notification(Notification(game=self.game,
                                                                   scene=self,
                                                                   text=message, 
                                                                   side='rb', 
                                                                   align='r'))
        
        if self.states['is_starting_a_war']:
            if len(self.chosen_countries) == 2:
                if not (self.chosen_countries[0].in_war_with(self.chosen_countries[1])):
                    self.chosen_countries[0].declare_war(self.chosen_countries[1])
                    self.chosen_countries = []
                    self.sidebar.get_object(1).onclick()
        
        elif self.states['is_creating_an_alliance']:
            if len(self.chosen_countries) == 2:
                if not (self.chosen_countries[0].in_war_with(self.chosen_countries[1])):
                    self.chosen_countries[0].create_alliance(self.chosen_countries[1])
                    self.chosen_countries = []
                    self.sidebar.get_object(5).onclick()
    
    def handle_event(self, event):
        self.current_mouse_pos = pygame.mouse.get_pos()
                             
        if event.type == pygame.TEXTINPUT:
            match event.text:
                case '1':
                    for country in self.countries:
                        print(f'Country {country.name} {country.agression}')

                case '2':
                    for event in self.events:
                        print(f'- [{event.time}] {event.description}')

                case '3':
                    print('Alliances:')
                    for alliance in self.alliances:
                        print(f'- {alliance}\n')

                case '4':
                    for country in self.countries:
                        print(f'{country.name} {country.allies}')

                case '5':
                    random_country1 = random.choice(self.countries)
                    random_country2 = random.choice(self.countries)

                    if random_country1 != random_country2:
                        if len(random_country1.humans) > 1 and len(random_country2.humans) > 1:
                            random_country1.declare_war(random_country2)

                case '6':
                    print(f'Cities:')
                    for city in self.cities:
                        print(f'- {city}\n')

                case '0':
                    self.create_country()
        
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_7:
                    print("People in war from countries:")
                    for country in self.countries:
                        print(f'- {country.name}: {country.get_people_in_war()}')
                        
                        for human in list(filter(lambda human: human.states['current_war']!=None, country.humans)):
                            print(f'Human from {country.name} {human.rect.x=} {human.rect.y=}')
                            print(f'Human\'s war: {human.states["current_war"]}\n')
                case pygame.K_8:
                    print("Inventory:")
                    for country in self.countries:
                        print(f'- {country.name}\'s inventory:')
                        country.inventory.print_inventory()
                        print('\n')
                            
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.is_scrolling = True
            
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_scrolling = False
 
        # Make your image move continuously
        elif event.type == pygame.MOUSEMOTION and self.is_scrolling:
            self.scroll_x += event.rel[0]
            self.scroll_y += event.rel[1]
        
        elif pygame.mouse.get_pressed(num_buttons=3)[0]:
            is_colliding = False
            
            for country in self.countries:   
                if not is_colliding:
                    for territory in country.territory:
                        if (territory.camerarect.colliderect(self.sidebar.rect) and not self.sidebar.is_visible) or not territory.camerarect.colliderect(self.sidebar.rect):
                            if territory.camerarect.collidepoint(self.current_mouse_pos):
                                if not self.already_pressed:
                                    self.select_country(country)
                                    self.already_pressed = True
                                    is_colliding = True
                
                if not is_colliding:
                    for human in country.humans:
                        if (human.camerarect.colliderect(self.sidebar.rect) and not self.sidebar.is_visible) or not human.camerarect.colliderect(self.sidebar.rect):
                            if human.camerarect.collidepoint(self.current_mouse_pos):
                                if not self.already_pressed:
                                    self.select_country(country)
                                    self.already_pressed = True
                                    is_colliding = True
                
                if not is_colliding:
                    for city in country.cities + [country.capital]:
                        if (city.camerarect.colliderect(self.sidebar.rect) and not self.sidebar.is_visible) or not city.camerarect.colliderect(self.sidebar.rect):
                            if city.camerarect.collidepoint(self.current_mouse_pos):
                                if not self.already_pressed:
                                    self.select_country(country)
                                    self.already_pressed = True
                                    is_colliding = True

        elif not pygame.mouse.get_pressed(num_buttons=3)[0]:
            self.already_pressed = False
            
        if -self.scroll_x > self.terrain.width - self.game.width:
            self.scroll_x = -(self.terrain.width - self.game.width)
        
        if -self.scroll_y > self.terrain.height - self.game.height:
            self.scroll_y = -(self.terrain.height - self.game.height)
        
        if self.scroll_x > 0:
            self.scroll_x = 0
        
        if self.scroll_y > 0:
            self.scroll_y = 0
        
        self.previous_mouse_pos = pygame.mouse.get_pos()
    
    def render(self):
        self.screen.fill((22, 156, 233))
        if self.terrain != None:
            self.terrain.render(self.scroll_x, self.scroll_y)
            list(map(lambda tree: tree.render(self.scroll_x, self.scroll_y), self.resources))

        for country in self.countries:
            list(map(lambda land: land.render(self.scroll_x, self.scroll_y), country.territory))

        for country in self.countries:
            country.render()

        for country in self.countries:
            country.king.render(self.scroll_x, self.scroll_y)
            list(map(lambda human: human.render(self.scroll_x, self.scroll_y), country.humans))

        for country in self.countries:
            country.capital.render(self.scroll_x, self.scroll_y)

        for country in self.countries:
            list(map(lambda city: city.render(self.scroll_x, self.scroll_y), country.cities))

        for war in self.wars:
            for battle in war.battles:
                battle.render(self.scroll_x, self.scroll_y)

        if self.notifications_visible:
            self.notificationManager.render_notifications()

        for i, country in enumerate(self.countries):
            self.draw_legend(country, 20 * i)

        for i, alliance in enumerate(self.alliances):
            i = len(self.countries) + i
            self.draw_legend_alliance(alliance, 20 * i)

        self.sidebar.render()