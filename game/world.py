import pygame
from typing import List, Dict
from game.enemy import create_enemy, Enemy
from game.npc import create_npc, NPC

class Location:
    def __init__(self, name: str, description: str, area_type: str):
        self.name = name
        self.description = description
        self.area_type = area_type
        self.enemies: List[Enemy] = []
        self.npcs: List[NPC] = []
        self.items: List = []

class World:
    def __init__(self):
        self.current_location = "Whiterun"
        self.locations: Dict[str, Location] = {}
        self.initialize_locations()
    
    def initialize_locations(self):
        whiterun = Location("Whiterun", "The main city, bustling with activity", "city")
        whiterun.npcs = [
            create_npc("Jarl Balgruuf"),
            create_npc("Guard Captain"),
            create_npc("Merchant"),
            create_npc("Town Guard")
        ]
        self.locations["Whiterun"] = whiterun
        
        riverwood = Location("Riverwood", "A peaceful village by the river", "village")
        riverwood.npcs = [
            create_npc("Farmer"),
            create_npc("Innkeeper")
        ]
        riverwood.enemies = [
            create_enemy("Wolf", pygame.Vector2(300, 400)),
            create_enemy("Wolf", pygame.Vector2(500, 450))
        ]
        self.locations["Riverwood"] = riverwood
        
        bleak_falls = Location("Bleak Falls Barrow", "An ancient Nordic tomb", "dungeon")
        bleak_falls.enemies = [
            create_enemy("Draugr", pygame.Vector2(400, 300)),
            create_enemy("Draugr", pygame.Vector2(600, 350)),
            create_enemy("Draugr", pygame.Vector2(500, 500)),
            create_enemy("Draugr", pygame.Vector2(700, 400)),
            create_enemy("Draugr", pygame.Vector2(300, 450))
        ]
        self.locations["Bleak Falls Barrow"] = bleak_falls
        
        wilderness = Location("Wilderness", "Open plains and forests", "wilderness")
        wilderness.enemies = [
            create_enemy("Wolf", pygame.Vector2(400, 300)),
            create_enemy("Wolf", pygame.Vector2(600, 400)),
            create_enemy("Bandit", pygame.Vector2(800, 300)),
            create_enemy("Bandit", pygame.Vector2(700, 500)),
            create_enemy("Troll", pygame.Vector2(900, 400))
        ]
        self.locations["Wilderness"] = wilderness
        
        dragon_lair = Location("Dragon Lair", "A mountain peak where a dragon resides", "lair")
        dragon_lair.enemies = [
            create_enemy("Dragon", pygame.Vector2(640, 360))
        ]
        self.locations["Dragon Lair"] = dragon_lair
    
    def get_current_location(self) -> Location:
        return self.locations[self.current_location]
    
    def travel_to(self, location_name: str) -> bool:
        if location_name in self.locations:
            self.current_location = location_name
            return True
        return False
    
    def get_available_locations(self) -> List[str]:
        return list(self.locations.keys())
    
    def respawn_enemies(self, location_name: str):
        if location_name == "Bleak Falls Barrow":
            location = self.locations[location_name]
            location.enemies = [
                create_enemy("Draugr", pygame.Vector2(400, 300)),
                create_enemy("Draugr", pygame.Vector2(600, 350)),
                create_enemy("Draugr", pygame.Vector2(500, 500)),
                create_enemy("Draugr", pygame.Vector2(700, 400)),
                create_enemy("Draugr", pygame.Vector2(300, 450))
            ]
        elif location_name == "Wilderness":
            location = self.locations[location_name]
            location.enemies = [
                create_enemy("Wolf", pygame.Vector2(400, 300)),
                create_enemy("Wolf", pygame.Vector2(600, 400)),
                create_enemy("Bandit", pygame.Vector2(800, 300)),
                create_enemy("Bandit", pygame.Vector2(700, 500)),
                create_enemy("Troll", pygame.Vector2(900, 400))
            ]
        elif location_name == "Riverwood":
            location = self.locations[location_name]
            location.enemies = [
                create_enemy("Wolf", pygame.Vector2(300, 400)),
                create_enemy("Wolf", pygame.Vector2(500, 450))
            ]
