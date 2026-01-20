import pygame
from typing import Dict, List

class Race:
    def __init__(self, name: str, health_bonus: int, magicka_bonus: int, 
                 stamina_bonus: int, abilities: List[str]):
        self.name = name
        self.health_bonus = health_bonus
        self.magicka_bonus = magicka_bonus
        self.stamina_bonus = stamina_bonus
        self.abilities = abilities

RACES = {
    "Nord": Race("Nord", 20, 0, 10, ["Frost Resistance", "Battle Cry"]),
    "Imperial": Race("Imperial", 10, 20, 0, ["Voice of the Emperor", "Better Prices"]),
    "Khajiit": Race("Khajiit", 0, 0, 15, ["Night Eye", "Claw Damage"]),
    "Argonian": Race("Argonian", 10, 0, 10, ["Waterbreathing", "Disease Resistance"]),
    "Dark Elf": Race("Dark Elf", 0, 20, 0, ["Fire Resistance", "Ancestor's Wrath"])
}

class Character:
    def __init__(self, name: str, race: str):
        self.name = name
        self.race = RACES[race]
        
        self.level = 1
        self.experience = 0
        self.exp_to_level = 100
        
        base_health = 100
        base_magicka = 100
        base_stamina = 100
        
        self.max_health = base_health + self.race.health_bonus
        self.max_magicka = base_magicka + self.race.magicka_bonus
        self.max_stamina = base_stamina + self.race.stamina_bonus
        
        self.health = self.max_health
        self.magicka = self.max_magicka
        self.stamina = self.max_stamina
        
        self.skills = {
            "One-Handed": 15,
            "Two-Handed": 15,
            "Archery": 15,
            "Block": 15,
            "Destruction": 15,
            "Restoration": 15,
            "Conjuration": 15,
            "Illusion": 15,
            "Sneak": 15,
            "Lockpicking": 15,
            "Pickpocket": 15,
            "Speech": 15
        }
        
        self.inventory = []
        self.equipped = {
            "weapon": None,
            "armor": None,
            "helmet": None,
            "boots": None,
            "gloves": None
        }
        
        self.gold = 100
        self.quests = []
        self.completed_quests = []
        
        self.position = pygame.Vector2(640, 360)
        self.velocity = pygame.Vector2(0, 0)
        self.speed = 200
        
    def add_experience(self, amount: int):
        self.experience += amount
        while self.experience >= self.exp_to_level:
            self.level_up()
    
    def level_up(self):
        self.experience -= self.exp_to_level
        self.level += 1
        self.exp_to_level = int(self.exp_to_level * 1.5)
        
        self.max_health += 10
        self.max_magicka += 10
        self.max_stamina += 10
        
        self.health = self.max_health
        self.magicka = self.max_magicka
        self.stamina = self.max_stamina
    
    def increase_skill(self, skill: str, amount: int):
        if skill in self.skills:
            self.skills[skill] = min(100, self.skills[skill] + amount)
            self.add_experience(amount * 2)
    
    def take_damage(self, amount: int):
        armor_reduction = self.get_armor_value() * 0.5
        actual_damage = max(1, amount - armor_reduction)
        self.health = max(0, self.health - actual_damage)
        return self.health <= 0
    
    def heal(self, amount: int):
        self.health = min(self.max_health, self.health + amount)
    
    def use_magicka(self, amount: int) -> bool:
        if self.magicka >= amount:
            self.magicka -= amount
            return True
        return False
    
    def use_stamina(self, amount: int) -> bool:
        if self.stamina >= amount:
            self.stamina -= amount
            return True
        return False
    
    def regenerate(self, dt: float):
        self.health = min(self.max_health, self.health + 5 * dt)
        self.magicka = min(self.max_magicka, self.magicka + 10 * dt)
        self.stamina = min(self.max_stamina, self.stamina + 15 * dt)
    
    def get_armor_value(self) -> int:
        armor = 0
        for slot, item in self.equipped.items():
            if item and hasattr(item, 'armor'):
                armor += item.armor
        return armor
    
    def get_damage(self) -> int:
        base_damage = 10
        if self.equipped["weapon"]:
            return self.equipped["weapon"].damage
        return base_damage
    
    def add_item(self, item):
        self.inventory.append(item)
    
    def remove_item(self, item):
        if item in self.inventory:
            self.inventory.remove(item)
    
    def equip_item(self, item):
        if hasattr(item, 'slot'):
            if self.equipped[item.slot]:
                self.inventory.append(self.equipped[item.slot])
            self.equipped[item.slot] = item
            self.remove_item(item)
    
    def unequip_item(self, slot: str):
        if self.equipped[slot]:
            self.inventory.append(self.equipped[slot])
            self.equipped[slot] = None
    
    def update(self, dt: float):
        self.position += self.velocity * dt
        self.regenerate(dt)
        
        self.position.x = max(0, min(1280, self.position.x))
        self.position.y = max(0, min(720, self.position.y))
