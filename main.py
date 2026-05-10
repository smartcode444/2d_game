import pygame, sys, random, time
from settings import *
# from level import Level
from entities import Player, Enemy
from assets import Bullets

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Platformer")
font = pygame.font.SysFont('Arial', 36)

BLACK = (0,0,0)
WHITE = (255,255,255)

class GameStartManager:
    def __init__(self, current_state):
        self.current_state = current_state

    def get_state(self):
        return self.current_state
    
    def set_state(self, state):
        self.current_state = state

class StartMenu:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.text_color = WHITE

    def display(self):
        title_text = font.render(f"MY AWESOME GAME", True, WHITE)
        start_text = font.render(f"Click Space to Start", True, WHITE)
        self.screen.blit(title_text, (screen_width//2 - 140, 200))
        self.screen.blit(start_text, (screen_width//2 - 120, 300))

    def run(self, dt):
        self.screen.fill(BLACK)
        self.display()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gameStateManager.set_state('LEVEL1')
            states[gameStartManager.get_state()].restart() # Restart level

class Level:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.level_data()   
        self.bullet_wait_time = 0

    def level_data(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        #  groups, pos, size=32, speed=5, gravity= 0.1, color=(255, 255, 255), health=100
        self.player = Player(screen, groups=[self.all_sprites], pos=[700, 340])

        self.enemy1 = Enemy(screen, groups=[self.all_sprites, self.enemy_group], pos=[200, screen_height - 32], speed=4)
        self.enemy2 = Enemy(screen,groups=[self.all_sprites, self.enemy_group], pos=[100, screen_height - 32], speed=2)
        self.enemy3 = Enemy(screen, groups=[self.all_sprites, self.enemy_group], pos=[400, screen_height - 32], speed=6)
        
        # self.bullets = Bullets(groups=[self.all_sprites, self.bullet_group])
        

    def parse_input(self, keys, mouse_buttons, dt):
        self.player.get_input(keys)
        self.bullet_wait_time += dt
        if self.bullet_wait_time >= 0.2:
            if mouse_buttons[0]:                
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse_pos = pygame.Vector2(mouse_x, mouse_y)

                self.bullets = Bullets(mouse_pos, self.player.pos.copy(), groups=[self.all_sprites, self.bullet_group])
                self.bullet_wait_time = 0
            

    def update_sprites(self):
        self.all_sprites.update()
        self.all_sprites.draw(screen)

    def check_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_group, False):
            self.player.take_damage(1)

        for bullet in self.bullet_group:
            for enemy in self.enemy_group:
                if bullet.rect.colliderect(enemy):
                    enemy.take_damage(4)
                    bullet.kill()

    def check_game_over(self):
        if self.player.is_dead:
            self.gameStateManager.set_state('GAME_OVER')
            states[gameStartManager.get_state()].reset()
            

    def restart(self):
        self.level_data()
        self.bullet_wait_time = 0

    def run(self, dt):
        self.update_sprites()
        self.check_collision()
        self.check_game_over()
        # print(self.player.health)

class GameOver:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.time_elapsed = 0

    def reset(self):
        self.time_elapsed = 0

    def display(self):
        title_text = font.render(f"GAME OVER", True, WHITE)
        self.screen.blit(title_text, (screen_width//2 - 100, 200))

    def run(self, dt):
        self.time_elapsed += dt
        self.screen.fill(BLACK)
        self.display()
        if self.time_elapsed >= 2:
            self.gameStateManager.set_state('START_MENU')

gameStartManager = GameStartManager('START_MENU')
start = StartMenu(screen, gameStartManager)
level1 = Level(screen, gameStartManager)
game_over = GameOver(screen, gameStartManager)

states = {
    "START_MENU": start,
    "LEVEL1": level1,
    "GAME_OVER": game_over
}

def _check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

while True:
    dt = clock.tick(FPS) / 1000.0  # Calculate delta time
    screen.fill('black')
    
    _check_events()
    
    # Handle inputs for active state
    if gameStartManager.get_state() == 'LEVEL1':
        mouse_buttons = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        level1.parse_input(keys, mouse_buttons, dt)

    states[gameStartManager.get_state()].run(dt)

    pygame.display.update()



# Game continues when restarting, instead of resetting