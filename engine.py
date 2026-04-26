import pygame
from os import walk
from settings import screen_height, screen_width

class Entity():
    def __init__(self, pos, size, speed, gravity, color, health):
        # Physics 
        self.pos = pos
        self.size = size
        self.direction = pygame.math.Vector2(0,0)
        self.speed = speed
        self.gravity = gravity
        self.jump_momentum = -7
        self.is_grounded = False

        # State and Health
        self.health = health
        self.is_dead = False

        # Aniamtion and Graphics 
        self.animations = {'idle': [], 'run': [], 'jump': [], 'fall': []}
        self.frame_index = 0
        self.status = 'idle'
        self.animation_speed = 0.15
        self.facing_right = True

        # Placeholder image and rect
        self.image = pygame.Surface((self.size, self.size))
        self.color = color
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft = self.pos)

    def take_damage(self, amt):
        if self.health > 0: self.health -= amt
        else: # Dead
            self.is_dead = True
            self.color = (0,0,0)
            self.image.fill(self.color)

    def check_death(self):
        if self.is_dead:
            self.color = (0, 0, 0)

    def get_status(self):
        if self.direction.y < 0: self.status = 'jump'
        elif self.direction.y > 1: self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

class Enemy(pygame.sprite.Sprite, Entity): # Inherit from Sprite!
    def __init__(self, groups, pos, size=32, speed=5, gravity= 0.1, color=(255, 0, 0), health=100):
        pygame.sprite.Sprite.__init__(self, groups)
        Entity.__init__(self, pos, size, speed, gravity, color, health) 
        self.direction.x = 1
        
    def motion(self):
        self.rect.x += self.direction.x * self.speed

    def set_bounds(self):
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
            self.direction.x -= 1
        elif self.rect.left <= 0:
            self.rect.left = 0
            self.direction.x = 1
    
    def update(self):
        self.motion()
        self.set_bounds()


class Player(pygame.sprite.Sprite, Entity): # Inherit from Sprite!
    def __init__(self, groups, pos, size=32, speed=4, gravity= 0.3, color=(255, 255, 255), health=100):
        pygame.sprite.Sprite.__init__(self, groups)
        Entity.__init__(self, pos, size, speed, gravity, color, health) 

        self.font = pygame.font.SysFont('Arial', 36)

    def apply_motion(self):
        # Horizontal movement
        self.rect.x += self.direction.x * self.speed

        # Verical movement
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
        self.is_grounded = False

    def get_input(self):
       
        keys = pygame.key.get_pressed()
        if self.is_grounded:
            if keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.facing_right = False
            elif keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.facing_right = True
            else:
                self.direction.x = 0
        if keys[pygame.K_SPACE] and self.is_grounded:
            self.direction.y = self.jump_momentum

    def set_boundary(self):
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.direction.y = 0
            self.is_grounded = True
        elif self.rect.top <= 0:
            self.rect.top = 0
            self.direction.y = 1
        else:
            self.is_grounded = False

        if self.rect.right >= screen_width:
            self.rect.right = screen_width
        elif self.rect.left <= 0:
            self.rect.left = 0

    def display_health(self, screen):
        player_health = self.font.render(f"Health: {self.health}", True, self.color)
        screen.blit(player_health, (screen_width - 200, 0))

    def update(self):
        self.get_input() # Player can get input
        self.apply_motion()
        self.set_boundary()
        self.get_status()
        



        # self.animate()
        
    # def import_assests(self, path):
    #     # character_path = "./assests/animation/"
    #     self.animations = {'idle':'', 'run':'', 'jump':'', 'fall':''}

    #     for animation in self.animations.keys():
    #         full_path = path + animation + ".png"
    #         sprite_sheet = pygame.image.load(full_path).convert_alpha()
    #         self.animations[animation] = sprite_sheet 

    # def get_image(self, sheet, width, height, frame):   
    #     image = pygame.Surface((width, height)).convert_alpha()
    #     image.blit(sheet, (0, 0), (frame * width, 0, width, height)) 
    #     image = pygame.transform.scale(image, (width, height))
    #     image.set_colorkey((0, 0, 0)) 
    #     self.image = image
    #     self.rect = self.image.get_rect(topleft = self.pos)
    
    # def animate(self):
    #     spritesheet_width = len(self.animations[self.status])

    #     # Loop through the frame index and update the image
    #     self.frame_index += self.animation_speed
    #     if self.frame_index >= spritesheet_width / self.image.get_width(): 
    #         self.frame_index = 0

    #     if self.facing_right:
    #         self.image = self.get_image(self.animations[self.status], 32, 32, int(self.frame_index))
    #     else:
    #         self.image = pygame.transform.flip(self.get_image(self.animations[self.status], 32, 32, int(self.frame_index)), True, False)