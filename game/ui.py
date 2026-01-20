import pygame
from typing import List, Optional

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 20)
    
    def draw_text(self, text: str, position: tuple, color=(255, 255, 255), 
                  font=None, center=False):
        if font is None:
            font = self.font
        
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        
        if center:
            text_rect.center = position
        else:
            text_rect.topleft = position
        
        self.screen.blit(text_surface, text_rect)
        return text_rect
    
    def draw_bar(self, position: tuple, size: tuple, current: float, 
                 maximum: float, color: tuple, bg_color=(50, 50, 50)):
        bg_rect = pygame.Rect(position[0], position[1], size[0], size[1])
        pygame.draw.rect(self.screen, bg_color, bg_rect)
        
        if maximum > 0:
            fill_width = int((current / maximum) * size[0])
            fill_rect = pygame.Rect(position[0], position[1], fill_width, size[1])
            pygame.draw.rect(self.screen, color, fill_rect)
        
        pygame.draw.rect(self.screen, (255, 255, 255), bg_rect, 2)
    
    def draw_character_hud(self, character):
        hud_bg = pygame.Surface((400, 120))
        hud_bg.set_alpha(200)
        hud_bg.fill((20, 20, 20))
        self.screen.blit(hud_bg, (10, 10))
        
        self.draw_text(f"Level {character.level} {character.race.name}", 
                      (20, 15), font=self.large_font)
        self.draw_text(character.name, (20, 50), color=(200, 200, 100))
        
        self.draw_text("Health:", (20, 75), color=(255, 100, 100))
        self.draw_bar((90, 75), (200, 15), character.health, 
                     character.max_health, (200, 50, 50))
        self.draw_text(f"{int(character.health)}/{character.max_health}", 
                      (300, 75), color=(255, 255, 255), font=self.small_font)
        
        self.draw_text("Magicka:", (20, 95), color=(100, 100, 255))
        self.draw_bar((90, 95), (200, 15), character.magicka, 
                     character.max_magicka, (50, 50, 200))
        self.draw_text(f"{int(character.magicka)}/{character.max_magicka}", 
                      (300, 95), color=(255, 255, 255), font=self.small_font)
        
        self.draw_text("Stamina:", (20, 115), color=(100, 255, 100))
        self.draw_bar((90, 115), (200, 15), character.stamina, 
                     character.max_stamina, (50, 200, 50))
        self.draw_text(f"{int(character.stamina)}/{character.max_stamina}", 
                      (300, 115), color=(255, 255, 255), font=self.small_font)
        
        exp_text = f"XP: {character.experience}/{character.exp_to_level}"
        self.draw_text(exp_text, (20, 140), color=(255, 215, 0))
        
        gold_text = f"Gold: {character.gold}"
        self.draw_text(gold_text, (200, 140), color=(255, 215, 0))
    
    def draw_inventory(self, character):
        panel = pygame.Surface((600, 500))
        panel.set_alpha(230)
        panel.fill((30, 30, 30))
        self.screen.blit(panel, (340, 110))
        
        self.draw_text("INVENTORY", (500, 120), font=self.large_font, 
                      color=(255, 215, 0))
        
        y_offset = 160
        self.draw_text("Equipped:", (360, y_offset), color=(200, 200, 100))
        y_offset += 30
        
        for slot, item in character.equipped.items():
            if item:
                self.draw_text(f"{slot.capitalize()}: {item.name}", 
                             (380, y_offset), color=(150, 255, 150))
            else:
                self.draw_text(f"{slot.capitalize()}: Empty", 
                             (380, y_offset), color=(100, 100, 100))
            y_offset += 25
        
        y_offset += 20
        self.draw_text("Inventory:", (360, y_offset), color=(200, 200, 100))
        y_offset += 30
        
        if not character.inventory:
            self.draw_text("Empty", (380, y_offset), color=(100, 100, 100))
        else:
            for i, item in enumerate(character.inventory[:10]):
                item_text = f"{item.name} (Value: {item.value}g)"
                self.draw_text(item_text, (380, y_offset), color=(200, 200, 200))
                y_offset += 25
        
        self.draw_text("Press I to close", (500, 580), 
                      color=(150, 150, 150), font=self.small_font)
    
    def draw_quest_log(self, character):
        panel = pygame.Surface((600, 500))
        panel.set_alpha(230)
        panel.fill((30, 30, 30))
        self.screen.blit(panel, (340, 110))
        
        self.draw_text("QUEST LOG", (520, 120), font=self.large_font, 
                      color=(255, 215, 0))
        
        y_offset = 160
        
        if not character.quests:
            self.draw_text("No active quests", (360, y_offset), 
                          color=(100, 100, 100))
        else:
            for quest in character.quests:
                self.draw_text(quest.name, (360, y_offset), 
                             color=(255, 200, 100), font=self.font)
                y_offset += 30
                
                objective = quest.get_current_objective()
                self.draw_text(f"  - {objective}", (380, y_offset), 
                             color=(200, 200, 200), font=self.small_font)
                y_offset += 25
                
                if quest.is_completed():
                    self.draw_text("  [COMPLETE]", (380, y_offset), 
                                 color=(100, 255, 100))
                    y_offset += 25
                
                y_offset += 15
        
        y_offset += 30
        self.draw_text("Completed Quests:", (360, y_offset), 
                      color=(100, 200, 100))
        y_offset += 30
        
        if not character.completed_quests:
            self.draw_text("None", (380, y_offset), color=(100, 100, 100))
        else:
            for quest_name in character.completed_quests[:5]:
                self.draw_text(f"  {quest_name}", (380, y_offset), 
                             color=(150, 150, 150))
                y_offset += 25
        
        self.draw_text("Press Q to close", (520, 580), 
                      color=(150, 150, 150), font=self.small_font)
    
    def draw_location_info(self, location):
        panel = pygame.Surface((300, 60))
        panel.set_alpha(200)
        panel.fill((20, 20, 20))
        self.screen.blit(panel, (980, 10))
        
        self.draw_text(location.name, (990, 20), color=(255, 215, 0))
        self.draw_text(location.description, (990, 45), 
                      font=self.small_font, color=(200, 200, 200))
    
    def draw_notification(self, message: str):
        panel = pygame.Surface((600, 60))
        panel.set_alpha(220)
        panel.fill((40, 40, 40))
        self.screen.blit(panel, (340, 640))
        
        self.draw_text(message, (640, 670), color=(255, 255, 100), 
                      font=self.font, center=True)
    
    def draw_dialogue(self, npc_name: str, dialogue: str):
        panel = pygame.Surface((800, 100))
        panel.set_alpha(230)
        panel.fill((20, 20, 40))
        self.screen.blit(panel, (240, 580))
        
        self.draw_text(f"{npc_name}:", (260, 590), 
                      color=(255, 215, 0), font=self.large_font)
        
        words = dialogue.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            if self.font.size(test_line)[0] > 750:
                current_line.pop()
                lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        y_offset = 630
        for line in lines[:2]:
            self.draw_text(line, (260, y_offset), color=(220, 220, 220))
            y_offset += 25
