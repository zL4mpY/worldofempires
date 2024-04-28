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
from engine.classes.button import Button

# from worldofempires.assets.country import Country
# from worldofempires.assets.city import City

import pygame
import random

class GameScene(Scene):
    def __init__(self, game, name):
        super().__init__(game, name)
    
        self.cell_size: int = 5
        self.land_cell_size: int = 20

        self.all_countries: list[str] = self.game.lang['countries']
        self.all_alliances: list[str] = self.game.lang['alliances']
        
        self.terrain = None

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
        
        self.sidebar = Sidebar(self.game, self)
        self.settings = {}
        
        self.scroll_x = 0
        self.scroll_y = 0
        
        self.current_mouse_pos = pygame.mouse.get_pos()
        self.previous_mouse_pos = self.current_mouse_pos
        self.is_scrolling = False
        self.scroll_rel = None
    
    def fill_sidebar(self):
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+40,
                        width=150, height=20,
                        align="center",
                        text="Start a war...",
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
                                                                           text="You need to choose exactly 2 countries",
                                                                           time=3,
                                                                           side='cb',
                                                                           align='center',
                                                                           color=(255, 0, 0),
                                                                           size=36))
            
            self.chosen_countries = [] if self.states['is_starting_a_war'] == True else self.chosen_countries
            self.states['is_starting_a_war'] = True if self.states['is_starting_a_war'] == False else False
            text = "Start a war..." if self.states['is_starting_a_war'] == False else "Cancel starting a war..."
            self.sidebar.get_object(1).change_text(text)
        
        self.sidebar.get_object(1).onclick = lambda: start_war()
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+65,
                        width=150, height=20,
                        align="center",
                        text="Select all",
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
                            
                    self.sidebar.get_object(2).change_text("Deselect all")
                    
                else:
                    self.chosen_countries = []
                    self.sidebar.get_object(2).change_text("Select all")
                
                
            elif len(self.chosen_countries) == len(self.countries):
                self.chosen_countries = []
                self.sidebar.get_object(2).change_text("Select all")
            
            else:
                if len(self.countries) > 0:
                    for country in self.countries:
                        if not country in self.chosen_countries:
                            self.chosen_countries.append(country)
                            
                    self.sidebar.get_object(2).change_text("Deselect all")
                    
                else:
                    self.chosen_countries = []
                    self.sidebar.get_object(2).change_text("Select all")
                
                
                # self.sidebar.get_object(2).change_text("Deselect all")

        self.sidebar.get_object(2).onclick = lambda: select_deselect_all()

        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+90,
                        width=150, height=20,
                        align="center",
                        text="Spawn human",
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
                                                                       text="You need to choose any country first",
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
                        text="Spawn country",
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
                        text="Create an alliance",
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
                                                                           text="You need to choose exactly 2 countries",
                                                                           time=3,
                                                                           side='cb',
                                                                           align='center',
                                                                           color=(255, 0, 0),
                                                                           size=36))
            
            self.chosen_countries = [] if self.states['is_creating_an_alliance'] == True else self.chosen_countries
            self.states['is_creating_an_alliance'] = True if self.states['is_creating_an_alliance'] == False else False
            fontsize = 14 if self.states['is_creating_an_alliance'] == False else 10 
            text = "Create an alliance..." if self.states['is_creating_an_alliance'] == False else "Cancel creating an alliance..."
            self.sidebar.get_object(5).change_text(text)
            self.sidebar.get_object(5).change_font(None, fontsize)

        self.sidebar.get_object(5).onclick = lambda: create_alliance()
        
        button = Button(game=self.game,
                        scene=self,
                        x=self.game.width-100, y=0+165,
                        width=150, height=20,
                        align="center",
                        text="Destroy country",
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
                                                                       text="Choose the country first",
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
                        x=self.game.width-100, y=self.game.height-20,
                        width=150, height=20,
                        align="center",
                        text="Main menu",
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
                self.game.sceneManager.switch_scene('menu')
            
            self.game.sceneManager.get_scene('loading_screen').custom_action = switch_to_menu
            self.game.sceneManager.switch_scene('loading_screen')

        self.sidebar.get_object(25).onclick = lambda: start_main_menu()
    
    def generate_terrain(self):
        # scale = random.randint(75, 100)
        scale = 100
        seed = 0
        sea_level = random.randint(100, 125)
        # persistence = random.randint(55, 100)
        persistence = 55
        lacunarity = 25
        octaves = 6
        
        width = self.game.width
        height = self.game.height
        
        if 'map' in self.settings:
            if 'width' in self.settings['map']:
                width = self.settings.get('map').get('width')
            
            if 'height' in self.settings['map']:
                height = self.settings.get('map').get('height')
            
        shape = (height, width)
        
        noise_array = self.terrainGenerator.generate(scale=scale,
                                                      shape=shape,
                                                      octaves=octaves,
                                                      persistence=persistence,
                                                      lacunarity=lacunarity,
                                                      seed=seed)

        color_array = self.terrainGenerator.assign_colors(layers, noise_array, sea_level)
        image = self.terrainGenerator.color_array_to_image(color_array)
        landscape = pilImageToSurface(image)
        
        terrain = Terrain(game=self.game, scene=self, x=0, y=0, image=image, landscape=landscape, width=width, height=height)
        return terrain
    
    def start(self):
        self.terrain = self.generate_terrain()
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

        # while not spawn_successful:
        #     if times_not_available >= 20:
        #         break
        #     x = random.randint(0, WIDTH - 2)
        #     y = random.randint(0, HEIGHT - 2)
        #     terrain_color = landscape.get_at((x, y))
        #     if terrain_color != (22, 156, 233) and terrain_color != (45, 166, 235) and terrain_color != (68, 176, 238) and terrain_color != (58, 29, 19) and terrain_color != (92, 61, 61) and terrain_color != (245, 240, 240):
        #         humans.append(Human(screen, landscape, (x, y)))
        #     spawn_successful = True
        #     # x, y = random.randrange(self.cell_size, game.width, self.cell_size), random.randrange(self.cell_size, game.height, self.cell_size)
        #     x, y = random.randint(self.cell_size, self.game.width - self.cell_size), random.randint(self.cell_size, self.game.height - self.cell_size)

        #     x = (x // self.cell_size) * self.cell_size
        #     y = (y // self.cell_size) * self.cell_size  

        #     zone_x = (x // self.land_cell_size) * self.land_cell_size
        #     zone_y = (y // self.land_cell_size) * self.land_cell_size
            
            # available_territory = True
            # if not all(country.is_claimed_territory(zone_x, zone_y) for country in self.countries):
            #     available_territory = True
            # else:
            #     times_not_available += 1
    
    def draw_legend(self, country, y):

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
            if random.uniform(0, 1) < self.game.settingsManager.settings.get('auto_spawn').get('countries').get('spawn_chance') / 15000:
                if len(self.countries) < self.game.settingsManager.settings.get('countries').get('max_value'):
                    self.create_country()
        
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
                    
                case '9':
                    print(self.scroll_x, self.scroll_y)
                    print(self.terrain.rect.x + self.scroll_x, self.terrain.rect.y + self.scroll_y)
                    print(self.terrain.rect.x, self.terrain.rect.y)
                    print(self.terrain.width, self.terrain.height)
                    print(self.terrain.width - self.game.width)
                    print(self.terrain.height - self.game.height)

                case '0':
                    self.create_country()
        
        elif event.type == pygame.KEYDOWN:
            match event.key:
                # case pygame.K_LEFT:
                #     if self.chosen_country == None:
                #         self.chosen_country = self.countries[0]
                #     else:
                #         index = self.countries.index(self.chosen_country) - 1
                #         self.chosen_country = self.countries[self.countries.index(self.chosen_country)-1]
                    
                #     message = self.game.lang['onCountryChoose'].format(self.chosen_country)
                #     self.notificationManager.add_notification(Notification(game=self.game,
                #                                                            scene=self,
                #                                                            text=message, 
                #                                                            side='rb', 
                #                                                            align='r'))
                
                # case pygame.K_RIGHT:
                #     if self.chosen_country == None:
                #         self.chosen_country = self.countries[0]
                #     else:
                #         index = self.countries.index(self.chosen_country) + 1
                #         if index >= len(self.countries):
                #             index = 0
                        
                #         self.chosen_country = self.countries[index]
                    
                #     message = self.game.lang['onCountryChoose'].format(self.chosen_country)
                #     self.notificationManager.add_notification(Notification(game=self.game,
                #                                                            scene=self,
                #                                                            text=message, 
                #                                                            side='rb',
                #                                                            align='r'))
                
                case pygame.K_8:
                    print("People in war from countries:")
                    for country in self.countries:
                        print(f'- {country.name}: {country.get_people_in_war()}')
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.is_scrolling = True
            
        elif event.type == pygame.MOUSEBUTTONUP:
            self.is_scrolling = False
 
        # Make your image move continuously
        elif event.type == pygame.MOUSEMOTION and self.is_scrolling:
            self.scroll_x += event.rel[0]
            self.scroll_y += event.rel[1]
            self.scroll_rel = event.rel
        
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
        
        self.notificationManager.render_notifications()
        
        for i, country in enumerate(self.countries):
            self.draw_legend(country, 20 * i)
        
        for i, alliance in enumerate(self.alliances):
            i = len(self.countries) + i
            self.draw_legend_alliance(alliance, 20 * i)
        
        self.sidebar.render()