import pygame
import random
from game.character import Character, RACES
from game.world import World
from game.ui import UI
from game.items import create_item, Potion
from game.quest import create_quest
from game.enemy import Enemy

class GameState:
    MENU = "menu"
    CHARACTER_CREATION = "character_creation"
    PLAYING = "playing"
    INVENTORY = "inventory"
    QUEST_LOG = "quest_log"
    DIALOGUE = "dialogue"
    LOCATION_SELECT = "location_select"
    GAME_OVER = "game_over"

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.ui = UI(screen)
        self.state = GameState.MENU
        self.character = None
        self.world = World()
        
        self.menu_options = ["New Game", "Quit"]
        self.selected_option = 0
        
        self.race_options = list(RACES.keys())
        self.selected_race = 0
        self.character_name = ""
        self.name_input_active = True
        
        self.notification = ""
        self.notification_timer = 0
        
        self.current_dialogue_npc = None
        self.current_dialogue = ""
        
        self.combat_cooldown = 0
        self.enemy_kill_counts = {}
        
        self.location_options = []
        self.selected_location = 0
    
    def handle_event(self, event):
        if self.state == GameState.MENU:
            self.handle_menu_event(event)
        elif self.state == GameState.CHARACTER_CREATION:
            self.handle_character_creation_event(event)
        elif self.state == GameState.PLAYING:
            self.handle_playing_event(event)
        elif self.state == GameState.INVENTORY:
            self.handle_inventory_event(event)
        elif self.state == GameState.QUEST_LOG:
            self.handle_quest_log_event(event)
        elif self.state == GameState.DIALOGUE:
            self.handle_dialogue_event(event)
        elif self.state == GameState.LOCATION_SELECT:
            self.handle_location_select_event(event)
        elif self.state == GameState.GAME_OVER:
            self.handle_game_over_event(event)
    
    def handle_menu_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.menu_options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.menu_options)
            elif event.key == pygame.K_RETURN:
                if self.selected_option == 0:
                    self.state = GameState.CHARACTER_CREATION
                elif self.selected_option == 1:
                    pygame.quit()
                    exit()
    
    def handle_character_creation_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.name_input_active:
                if event.key == pygame.K_RETURN and len(self.character_name) > 0:
                    self.name_input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    self.character_name = self.character_name[:-1]
                elif event.unicode.isprintable() and len(self.character_name) < 20:
                    self.character_name += event.unicode
            else:
                if event.key == pygame.K_LEFT:
                    self.selected_race = (self.selected_race - 1) % len(self.race_options)
                elif event.key == pygame.K_RIGHT:
                    self.selected_race = (self.selected_race + 1) % len(self.race_options)
                elif event.key == pygame.K_RETURN:
                    race = self.race_options[self.selected_race]
                    self.character = Character(self.character_name, race)
                    self.character.add_item(create_item("Iron Sword"))
                    self.character.equip_item(self.character.inventory[0])
                    self.character.add_item(create_item("Minor Health Potion"))
                    self.character.add_item(create_item("Minor Health Potion"))
                    self.state = GameState.PLAYING
                    self.show_notification("Welcome to Skyrim!")
    
    def handle_playing_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.state = GameState.INVENTORY
            elif event.key == pygame.K_q:
                self.state = GameState.QUEST_LOG
            elif event.key == pygame.K_TAB:
                self.location_options = self.world.get_available_locations()
                self.state = GameState.LOCATION_SELECT
            elif event.key == pygame.K_e:
                self.interact_with_npc()
            elif event.key == pygame.K_1:
                self.use_item_from_inventory(0)
            elif event.key == pygame.K_2:
                self.use_item_from_inventory(1)
            elif event.key == pygame.K_3:
                self.use_item_from_inventory(2)
    
    def handle_inventory_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i or event.key == pygame.K_ESCAPE:
                self.state = GameState.PLAYING
    
    def handle_quest_log_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                self.state = GameState.PLAYING
    
    def handle_dialogue_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e or event.key == pygame.K_RETURN:
                if self.current_dialogue_npc.has_quest():
                    quest_name = self.current_dialogue_npc.give_quest()
                    quest = create_quest(quest_name)
                    if quest:
                        self.character.quests.append(quest)
                        self.show_notification(f"New Quest: {quest.name}")
                self.state = GameState.PLAYING
            elif event.key == pygame.K_ESCAPE:
                self.state = GameState.PLAYING
    
    def handle_location_select_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_location = (self.selected_location - 1) % len(self.location_options)
            elif event.key == pygame.K_DOWN:
                self.selected_location = (self.selected_location + 1) % len(self.location_options)
            elif event.key == pygame.K_RETURN:
                location_name = self.location_options[self.selected_location]
                self.world.travel_to(location_name)
                self.character.position = pygame.Vector2(640, 360)
                self.show_notification(f"Traveled to {location_name}")
                self.state = GameState.PLAYING
            elif event.key == pygame.K_ESCAPE or event.key == pygame.K_TAB:
                self.state = GameState.PLAYING
    
    def handle_game_over_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.state = GameState.MENU
                self.character = None
    
    def update(self, dt):
        if self.state == GameState.PLAYING:
            self.update_playing(dt)
        
        if self.notification_timer > 0:
            self.notification_timer -= dt
    
    def update_playing(self, dt):
        keys = pygame.key.get_pressed()
        
        velocity = pygame.Vector2(0, 0)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            velocity.y = -1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            velocity.y = 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            velocity.x = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            velocity.x = 1
        
        if velocity.length() > 0:
            velocity = velocity.normalize()
        
        self.character.velocity = velocity * self.character.speed
        self.character.update(dt)
        
        location = self.world.get_current_location()
        
        for enemy in location.enemies:
            if enemy.alive:
                enemy.update(dt, self.character.position)
                
                distance = enemy.position.distance_to(self.character.position)
                if distance < 50 and enemy.can_attack():
                    damage = enemy.attack()
                    if self.character.take_damage(damage):
                        self.state = GameState.GAME_OVER
                        return
        
        self.combat_cooldown = max(0, self.combat_cooldown - dt)
        
        if keys[pygame.K_SPACE] and self.combat_cooldown <= 0:
            self.perform_attack()
            self.combat_cooldown = 0.5
        
        self.update_quests()
    
    def perform_attack(self):
        location = self.world.get_current_location()
        damage = self.character.get_damage()
        
        for enemy in location.enemies:
            if enemy.alive:
                distance = enemy.position.distance_to(self.character.position)
                if distance < 80:
                    if enemy.take_damage(damage):
                        self.show_notification(f"Defeated {enemy.name}!")
                        self.character.add_experience(enemy.experience)
                        
                        if enemy.name not in self.enemy_kill_counts:
                            self.enemy_kill_counts[enemy.name] = 0
                        self.enemy_kill_counts[enemy.name] += 1
                        
                        for item_name in enemy.get_loot():
                            item = create_item(item_name)
                            if item:
                                self.character.add_item(item)
                                self.show_notification(f"Looted: {item_name}")
                        
                        if hasattr(enemy, 'weapon_type'):
                            skill = self.get_weapon_skill(self.character.equipped["weapon"])
                            if skill:
                                self.character.increase_skill(skill, 1)
                    break
    
    def get_weapon_skill(self, weapon):
        if weapon is None:
            return "One-Handed"
        if weapon.weapon_type == "one-handed":
            return "One-Handed"
        elif weapon.weapon_type == "two-handed":
            return "Two-Handed"
        elif weapon.weapon_type == "bow":
            return "Archery"
        return None
    
    def interact_with_npc(self):
        location = self.world.get_current_location()
        
        for npc in location.npcs:
            if npc.can_interact(self.character.position):
                self.current_dialogue_npc = npc
                self.current_dialogue = npc.get_dialogue()
                self.state = GameState.DIALOGUE
                return
    
    def use_item_from_inventory(self, index):
        if index < len(self.character.inventory):
            item = self.character.inventory[index]
            if isinstance(item, Potion):
                item.use(self.character)
                self.character.remove_item(item)
                self.show_notification(f"Used {item.name}")
    
    def update_quests(self):
        for quest in self.character.quests:
            if not quest.is_completed():
                current_obj = quest.get_current_objective()
                
                if "Defeat" in current_obj or "Kill" in current_obj:
                    parts = current_obj.split()
                    count_needed = int(parts[1])
                    enemy_type = parts[2]
                    
                    if enemy_type in self.enemy_kill_counts:
                        if self.enemy_kill_counts[enemy_type] >= count_needed:
                            quest.advance_objective()
                            self.show_notification(f"Quest Updated: {quest.name}")
                
                elif "Travel to" in current_obj:
                    if self.world.current_location in current_obj:
                        quest.advance_objective()
                        self.show_notification(f"Quest Updated: {quest.name}")
                
                if quest.is_completed() and quest.name not in self.character.completed_quests:
                    self.complete_quest(quest)
    
    def complete_quest(self, quest):
        self.character.add_experience(quest.rewards.get("experience", 0))
        self.character.gold += quest.rewards.get("gold", 0)
        
        for item_name in quest.rewards.get("items", []):
            item = create_item(item_name)
            if item:
                self.character.add_item(item)
        
        self.character.completed_quests.append(quest.name)
        self.character.quests.remove(quest)
        self.show_notification(f"Quest Complete: {quest.name}!")
    
    def show_notification(self, message):
        self.notification = message
        self.notification_timer = 3.0
    
    def render(self):
        self.screen.fill((30, 50, 30))
        
        if self.state == GameState.MENU:
            self.render_menu()
        elif self.state == GameState.CHARACTER_CREATION:
            self.render_character_creation()
        elif self.state == GameState.PLAYING:
            self.render_playing()
        elif self.state == GameState.INVENTORY:
            self.render_playing()
            self.ui.draw_inventory(self.character)
        elif self.state == GameState.QUEST_LOG:
            self.render_playing()
            self.ui.draw_quest_log(self.character)
        elif self.state == GameState.DIALOGUE:
            self.render_playing()
            self.ui.draw_dialogue(self.current_dialogue_npc.name, self.current_dialogue)
        elif self.state == GameState.LOCATION_SELECT:
            self.render_location_select()
        elif self.state == GameState.GAME_OVER:
            self.render_game_over()
    
    def render_menu(self):
        title = "SKYRIM-LIKE RPG"
        self.ui.draw_text(title, (640, 200), font=self.ui.large_font, 
                         color=(255, 215, 0), center=True)
        
        for i, option in enumerate(self.menu_options):
            color = (255, 255, 100) if i == self.selected_option else (200, 200, 200)
            self.ui.draw_text(option, (640, 300 + i * 50), 
                             color=color, center=True)
    
    def render_character_creation(self):
        self.ui.draw_text("CHARACTER CREATION", (640, 100), 
                         font=self.ui.large_font, color=(255, 215, 0), center=True)
        
        if self.name_input_active:
            self.ui.draw_text("Enter your name:", (640, 250), center=True)
            self.ui.draw_text(self.character_name + "_", (640, 300), 
                             font=self.ui.large_font, color=(255, 255, 100), center=True)
            self.ui.draw_text("Press ENTER to continue", (640, 400), 
                             color=(150, 150, 150), center=True)
        else:
            self.ui.draw_text("Choose your race:", (640, 200), center=True)
            
            race_name = self.race_options[self.selected_race]
            race = RACES[race_name]
            
            self.ui.draw_text(race.name, (640, 280), font=self.ui.large_font,
                             color=(255, 255, 100), center=True)
            
            y_offset = 340
            self.ui.draw_text(f"Health: +{race.health_bonus}", (640, y_offset), 
                             color=(255, 100, 100), center=True)
            y_offset += 30
            self.ui.draw_text(f"Magicka: +{race.magicka_bonus}", (640, y_offset),
                             color=(100, 100, 255), center=True)
            y_offset += 30
            self.ui.draw_text(f"Stamina: +{race.stamina_bonus}", (640, y_offset),
                             color=(100, 255, 100), center=True)
            y_offset += 40
            
            abilities_text = "Abilities: " + ", ".join(race.abilities)
            self.ui.draw_text(abilities_text, (640, y_offset), 
                             color=(255, 215, 0), center=True)
            
            self.ui.draw_text("< Arrow Keys to change | ENTER to confirm >", 
                             (640, 550), color=(150, 150, 150), center=True)
    
    def render_playing(self):
        location = self.world.get_current_location()
        
        if location.area_type == "city":
            self.screen.fill((60, 60, 80))
        elif location.area_type == "dungeon":
            self.screen.fill((20, 20, 20))
        elif location.area_type == "wilderness":
            self.screen.fill((30, 50, 30))
        elif location.area_type == "village":
            self.screen.fill((50, 60, 50))
        else:
            self.screen.fill((40, 40, 40))
        
        for npc in location.npcs:
            color = (100, 100, 255)
            if npc.has_quest():
                color = (255, 215, 0)
            pygame.draw.circle(self.screen, color, 
                             (int(npc.position.x), int(npc.position.y)), 15)
            self.ui.draw_text(npc.name, (npc.position.x - 30, npc.position.y - 30),
                             font=self.ui.small_font, color=(255, 255, 255))
        
        for enemy in location.enemies:
            if enemy.alive:
                color = (255, 50, 50)
                pygame.draw.circle(self.screen, color,
                                 (int(enemy.position.x), int(enemy.position.y)), 12)
                self.ui.draw_text(enemy.name, 
                                 (enemy.position.x - 25, enemy.position.y - 30),
                                 font=self.ui.small_font, color=(255, 100, 100))
                
                self.ui.draw_bar((enemy.position.x - 20, enemy.position.y + 20),
                               (40, 4), enemy.health, enemy.max_health,
                               (200, 50, 50))
        
        pygame.draw.circle(self.screen, (100, 255, 100),
                         (int(self.character.position.x), 
                          int(self.character.position.y)), 15)
        
        self.ui.draw_character_hud(self.character)
        self.ui.draw_location_info(location)
        
        if self.notification_timer > 0:
            self.ui.draw_notification(self.notification)
        
        controls_y = 680
        self.ui.draw_text("WASD:Move | SPACE:Attack | E:Interact | I:Inventory | Q:Quests | TAB:Travel",
                         (640, controls_y), font=self.ui.small_font, 
                         color=(150, 150, 150), center=True)
    
    def render_location_select(self):
        self.screen.fill((20, 30, 40))
        
        self.ui.draw_text("FAST TRAVEL", (640, 100), font=self.ui.large_font,
                         color=(255, 215, 0), center=True)
        
        for i, location_name in enumerate(self.location_options):
            color = (255, 255, 100) if i == self.selected_location else (200, 200, 200)
            self.ui.draw_text(location_name, (640, 200 + i * 50),
                             color=color, center=True)
        
        self.ui.draw_text("Arrow Keys to select | ENTER to travel | ESC to cancel",
                         (640, 600), color=(150, 150, 150), center=True)
    
    def render_game_over(self):
        self.screen.fill((20, 0, 0))
        
        self.ui.draw_text("YOU DIED", (640, 300), font=self.ui.large_font,
                         color=(255, 50, 50), center=True)
        
        self.ui.draw_text("Press ENTER to return to menu", (640, 400),
                         color=(200, 200, 200), center=True)
