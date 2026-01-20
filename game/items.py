from typing import Dict, Any

class Item:
    def __init__(self, name: str, value: int, weight: float, description: str):
        self.name = name
        self.value = value
        self.weight = weight
        self.description = description

class Weapon(Item):
    def __init__(self, name: str, value: int, weight: float, damage: int, 
                 weapon_type: str, description: str):
        super().__init__(name, value, weight, description)
        self.damage = damage
        self.weapon_type = weapon_type
        self.slot = "weapon"

class Armor(Item):
    def __init__(self, name: str, value: int, weight: float, armor: int, 
                 slot: str, description: str):
        super().__init__(name, value, weight, description)
        self.armor = armor
        self.slot = slot

class Potion(Item):
    def __init__(self, name: str, value: int, weight: float, effect: str, 
                 magnitude: int, description: str):
        super().__init__(name, value, weight, description)
        self.effect = effect
        self.magnitude = magnitude
    
    def use(self, character):
        if self.effect == "restore_health":
            character.heal(self.magnitude)
        elif self.effect == "restore_magicka":
            character.magicka = min(character.max_magicka, 
                                   character.magicka + self.magnitude)
        elif self.effect == "restore_stamina":
            character.stamina = min(character.max_stamina, 
                                   character.stamina + self.magnitude)

WEAPONS = {
    "Iron Sword": Weapon("Iron Sword", 25, 5, 15, "one-handed", 
                         "A basic iron sword"),
    "Steel Sword": Weapon("Steel Sword", 50, 6, 22, "one-handed", 
                          "A durable steel blade"),
    "Elven Bow": Weapon("Elven Bow", 150, 4, 18, "bow", 
                        "A finely crafted elven bow"),
    "Iron Battleaxe": Weapon("Iron Battleaxe", 40, 12, 28, "two-handed", 
                             "A heavy iron battleaxe"),
    "Orcish Greatsword": Weapon("Orcish Greatsword", 125, 15, 35, "two-handed",
                                "A powerful orcish greatsword"),
    "Daedric Sword": Weapon("Daedric Sword", 500, 8, 50, "one-handed",
                            "A legendary daedric blade"),
}

ARMOR = {
    "Iron Armor": Armor("Iron Armor", 75, 25, 20, "armor", 
                        "Basic iron armor"),
    "Steel Armor": Armor("Steel Armor", 150, 28, 30, "armor",
                         "Sturdy steel armor"),
    "Leather Helmet": Armor("Leather Helmet", 20, 2, 5, "helmet",
                            "Light leather helmet"),
    "Iron Boots": Armor("Iron Boots", 25, 5, 8, "boots",
                        "Heavy iron boots"),
    "Steel Gauntlets": Armor("Steel Gauntlets", 30, 4, 10, "gloves",
                             "Steel gauntlets for protection"),
    "Elven Armor": Armor("Elven Armor", 300, 20, 40, "armor",
                         "Beautiful elven crafted armor"),
}

POTIONS = {
    "Minor Health Potion": Potion("Minor Health Potion", 15, 0.5, 
                                  "restore_health", 30,
                                  "Restores 30 health"),
    "Health Potion": Potion("Health Potion", 50, 0.5, 
                            "restore_health", 60,
                            "Restores 60 health"),
    "Minor Magicka Potion": Potion("Minor Magicka Potion", 20, 0.5,
                                   "restore_magicka", 40,
                                   "Restores 40 magicka"),
    "Magicka Potion": Potion("Magicka Potion", 60, 0.5,
                             "restore_magicka", 80,
                             "Restores 80 magicka"),
    "Stamina Potion": Potion("Stamina Potion", 40, 0.5,
                             "restore_stamina", 70,
                             "Restores 70 stamina"),
}

def create_item(item_name: str):
    if item_name in WEAPONS:
        weapon = WEAPONS[item_name]
        return Weapon(weapon.name, weapon.value, weapon.weight, 
                     weapon.damage, weapon.weapon_type, weapon.description)
    elif item_name in ARMOR:
        armor = ARMOR[item_name]
        return Armor(armor.name, armor.value, armor.weight,
                    armor.armor, armor.slot, armor.description)
    elif item_name in POTIONS:
        potion = POTIONS[item_name]
        return Potion(potion.name, potion.value, potion.weight,
                     potion.effect, potion.magnitude, potion.description)
    return None
