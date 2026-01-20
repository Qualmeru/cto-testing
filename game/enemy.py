import pygame
import random
from typing import List

class Enemy:
    def __init__(self, name: str, health: int, damage: int, 
                 experience: int, loot: List[str], position: pygame.Vector2):
        self.name = name
        self.max_health = health
        self.health = health
        self.damage = damage
        self.experience = experience
        self.loot = loot
        self.position = position
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 100
        self.alive = True
        self.combat_radius = 150
        self.attack_cooldown = 0
        self.attack_delay = 1.5
    
    def update(self, dt: float, player_pos: pygame.Vector2):
        if not self.alive:
            return
        
        self.attack_cooldown = max(0, self.attack_cooldown - dt)
        
        distance = self.position.distance_to(player_pos)
        
        if distance < self.combat_radius:
            direction = player_pos - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                
                if distance > 50:
                    self.velocity = direction * self.speed
                else:
                    self.velocity = pygame.Vector2(0, 0)
        else:
            self.velocity *= 0.9
        
        self.position += self.velocity * dt
    
    def take_damage(self, amount: int) -> bool:
        self.health -= amount
        if self.health <= 0:
            self.alive = False
            return True
        return False
    
    def can_attack(self) -> bool:
        return self.attack_cooldown <= 0
    
    def attack(self) -> int:
        self.attack_cooldown = self.attack_delay
        return self.damage
    
    def get_loot(self) -> List[str]:
        return [item for item in self.loot if random.random() < 0.5]

ENEMY_TYPES = {
    "Bandit": {
        "health": 50,
        "damage": 10,
        "experience": 25,
        "loot": ["Iron Sword", "Minor Health Potion", "Leather Helmet"]
    },
    "Draugr": {
        "health": 75,
        "damage": 15,
        "experience": 40,
        "loot": ["Iron Battleaxe", "Health Potion", "Iron Armor"]
    },
    "Wolf": {
        "health": 30,
        "damage": 8,
        "experience": 15,
        "loot": ["Minor Health Potion"]
    },
    "Troll": {
        "health": 150,
        "damage": 25,
        "experience": 75,
        "loot": ["Steel Sword", "Health Potion", "Steel Armor"]
    },
    "Dragon": {
        "health": 500,
        "damage": 50,
        "experience": 300,
        "loot": ["Daedric Sword", "Elven Armor", "Magicka Potion", "Health Potion"]
    }
}

def create_enemy(enemy_type: str, position: pygame.Vector2) -> Enemy:
    if enemy_type in ENEMY_TYPES:
        data = ENEMY_TYPES[enemy_type]
        return Enemy(enemy_type, data["health"], data["damage"],
                    data["experience"], data["loot"], position)
    return None
