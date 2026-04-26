import pygame, sys, random, time
from settings import *
# from level import Level
from engine import Player, Enemy

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

    def run(self):
        self.screen.fill(BLACK)
        self.display()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gameStateManager.set_state('LEVEL1')

class Level:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.level_data()

    def level_data(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        #  groups, pos, size=32, speed=5, gravity= 0.1, color=(255, 255, 255), health=100
        self.player = Player(groups=[self.all_sprites], pos=(700, 340))

        self.enemy1 = Enemy(groups=[self.all_sprites, self.enemy_group], pos=(200, screen_height - 32), speed=4)
        self.enemy1 = Enemy(groups=[self.all_sprites, self.enemy_group], pos=(100, screen_height - 32), speed=2)
        self.enemy1 = Enemy(groups=[self.all_sprites, self.enemy_group], pos=(400, screen_height - 32), speed=6)

    def update_sprites(self):
        self.all_sprites.update()
        self.all_sprites.draw(screen)

    def check_collision(self):
        if pygame.sprite.spritecollide(self.player, self.enemy_group, False):
            self.player.take_damage(1)
        self.player.display_health(screen)

    def check_game_over(self):
        if self.player.is_dead:
            self.gameStateManager.set_state('GAME_OVER')

    def run(self):
        self.update_sprites()
        self.check_collision()
        self.check_game_over()

class GameOver:
    def __init__(self, screen, gameStateManager):
        self.screen = screen
        self.gameStateManager = gameStateManager
        self.time_elapsed = 0

    def display(self):
        title_text = font.render(f"GAME OVER", True, WHITE)
        self.screen.blit(title_text, (screen_width//2 - 100, 200))

    def run(self):
        self.time_elapsed += 0.0167
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
    screen.fill('black')
    states[gameStartManager.get_state()].run()

    _check_events()

    pygame.display.update()
    clock.tick(FPS)



