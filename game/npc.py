import pygame
from typing import List, Optional

class NPC:
    def __init__(self, name: str, dialogue: List[str], position: pygame.Vector2,
                 quest: Optional[str] = None, is_merchant: bool = False):
        self.name = name
        self.dialogue = dialogue
        self.position = position
        self.quest = quest
        self.is_merchant = is_merchant
        self.dialogue_index = 0
        self.quest_given = False
        self.interaction_radius = 60
    
    def get_dialogue(self) -> str:
        if self.dialogue_index < len(self.dialogue):
            text = self.dialogue[self.dialogue_index]
            self.dialogue_index = (self.dialogue_index + 1) % len(self.dialogue)
            return text
        return "..."
    
    def has_quest(self) -> bool:
        return self.quest is not None and not self.quest_given
    
    def give_quest(self):
        self.quest_given = True
        return self.quest
    
    def can_interact(self, player_pos: pygame.Vector2) -> bool:
        distance = self.position.distance_to(player_pos)
        return distance < self.interaction_radius

NPCS = {
    "Jarl Balgruuf": NPC(
        "Jarl Balgruuf",
        [
            "Greetings, traveler. Welcome to Whiterun.",
            "I could use someone of your skills. Interested in some work?",
            "Bleak Falls Barrow is dangerous, but I know you can handle it."
        ],
        pygame.Vector2(640, 200),
        quest="The First Adventure"
    ),
    "Guard Captain": NPC(
        "Guard Captain",
        [
            "Stay vigilant, citizen.",
            "Those bandits have been causing trouble. Can you help?",
            "Thank you for keeping the roads safe."
        ],
        pygame.Vector2(500, 300),
        quest="Bandit Problems"
    ),
    "Farmer": NPC(
        "Farmer",
        [
            "My crops won't grow with all these wolves around!",
            "Please, help me deal with these beasts!",
            "Thank you, kind stranger."
        ],
        pygame.Vector2(200, 500),
        quest="The Wolf Menace"
    ),
    "Innkeeper": NPC(
        "Innkeeper",
        [
            "Welcome to the inn! Rest and food available.",
            "There's a troll causing problems nearby...",
            "Safe travels, friend."
        ],
        pygame.Vector2(800, 400),
        quest="Troll Trouble",
        is_merchant=True
    ),
    "Merchant": NPC(
        "Merchant",
        [
            "Looking to buy or sell?",
            "I've got the finest wares in Skyrim!",
            "Come back anytime!"
        ],
        pygame.Vector2(300, 250),
        is_merchant=True
    ),
    "Town Guard": NPC(
        "Town Guard",
        [
            "No lollygaggin'.",
            "Keep your hands to yourself, sneak thief.",
            "Let me guess... someone stole your sweetroll?"
        ],
        pygame.Vector2(700, 350)
    )
}

def create_npc(npc_name: str) -> NPC:
    if npc_name in NPCS:
        npc = NPCS[npc_name]
        return NPC(npc.name, npc.dialogue.copy(), npc.position.copy(),
                  npc.quest, npc.is_merchant)
    return None
