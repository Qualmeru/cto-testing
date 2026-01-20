from typing import List, Dict, Any

class Quest:
    def __init__(self, name: str, description: str, objectives: List[str],
                 rewards: Dict[str, Any], quest_giver: str):
        self.name = name
        self.description = description
        self.objectives = objectives
        self.current_objective = 0
        self.completed = False
        self.rewards = rewards
        self.quest_giver = quest_giver
        self.progress = {}
        
        for obj in objectives:
            self.progress[obj] = False
    
    def advance_objective(self):
        if self.current_objective < len(self.objectives):
            self.progress[self.objectives[self.current_objective]] = True
            self.current_objective += 1
            
            if self.current_objective >= len(self.objectives):
                self.completed = True
    
    def get_current_objective(self) -> str:
        if self.current_objective < len(self.objectives):
            return self.objectives[self.current_objective]
        return "Quest Complete - Return to quest giver"
    
    def is_completed(self) -> bool:
        return self.completed

QUESTS = {
    "The First Adventure": Quest(
        "The First Adventure",
        "Help the jarl of Whiterun by clearing out Bleak Falls Barrow",
        [
            "Travel to Bleak Falls Barrow",
            "Defeat 5 Draugr",
            "Find the Golden Claw",
            "Return to the Jarl"
        ],
        {
            "experience": 100,
            "gold": 250,
            "items": ["Steel Sword", "Health Potion"]
        },
        "Jarl Balgruuf"
    ),
    "Bandit Problems": Quest(
        "Bandit Problems",
        "Bandits have been harassing travelers on the road",
        [
            "Defeat 3 Bandits",
            "Report back to the guard"
        ],
        {
            "experience": 50,
            "gold": 100,
            "items": ["Minor Health Potion"]
        },
        "Guard Captain"
    ),
    "The Wolf Menace": Quest(
        "The Wolf Menace",
        "Wolves are attacking the livestock near Riverwood",
        [
            "Kill 5 Wolves",
            "Report to the farmer"
        ],
        {
            "experience": 40,
            "gold": 75,
            "items": ["Leather Helmet"]
        },
        "Farmer"
    ),
    "Dragon Rising": Quest(
        "Dragon Rising",
        "A dragon has been sighted near Whiterun! Defeat it to save the city",
        [
            "Find the Dragon",
            "Defeat the Dragon",
            "Absorb the Dragon Soul",
            "Report to the Jarl"
        ],
        {
            "experience": 500,
            "gold": 1000,
            "items": ["Daedric Sword", "Elven Armor"]
        },
        "Jarl Balgruuf"
    ),
    "Troll Trouble": Quest(
        "Troll Trouble",
        "A troll has taken residence in a nearby cave",
        [
            "Locate the troll cave",
            "Defeat the Troll",
            "Collect the reward"
        ],
        {
            "experience": 150,
            "gold": 300,
            "items": ["Steel Armor", "Health Potion"]
        },
        "Innkeeper"
    )
}

def create_quest(quest_name: str) -> Quest:
    if quest_name in QUESTS:
        quest = QUESTS[quest_name]
        return Quest(quest.name, quest.description, quest.objectives.copy(),
                    quest.rewards.copy(), quest.quest_giver)
    return None
