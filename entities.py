import pygame
from os import walk
from settings import screen_height, screen_width

class Entity(pygame.sprite.Sprite):
    def __init__(self, groups, pos, size, speed, gravity, color, health):
        super().__init__(groups)
        # Physics 
        self.initial_pos = pos # A copy of self.pos for resetting
        self.pos = pygame.Vector2(pos[0], pos[1])
        self.size = size
        self.direction = pygame.Vector2(0,0)
        self.speed = speed
        self.gravity = pygame.Vector2(0,gravity)
        self.jump_momentum = -7
        self.is_grounded = False

        # State and Health
        self.initial_health = health # A copy of self.pos for resetting
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

        

    def reset(self):
        # Reset all variables/attributes
        self.rect.topleft = self.initial_pos
        self.health = self.initial_health
        self.is_dead = False

    def take_damage(self, amt):
        if self.health > 0: self.health -= amt

    def check_death(self):
        if self.health > 0:
            self.is_dead = False
        else:
            self.is_dead = True

        if self.is_dead:
            self.kill()

    def get_status(self):
        if self.direction.y < 0: self.status = 'jump'
        elif self.direction.y > 1: self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

class Enemy(Entity):
    def __init__(self, screen, groups, pos, size=32, speed=5, gravity= 0.1, color=(255, 0, 0), health=100):
        super().__init__(groups, pos, size, speed, gravity, color, health)
        self.direction.x = 1
        self.screen = screen
        
        self.font = pygame.font.SysFont('Arial', 36)
        self._last_health = None
        self._rendered_health = None

    def motion(self):
        self.rect.x += self.direction.x * self.speed

    def display_health(self):
        if self.health != self._last_health:
            self._rendered_health = self.font.render(f"Health: {self.health}", True, self.color)
            self._last_health = self.health
        self.screen.blit(self._rendered_health, (self.rect.centerx, self.rect.centery-70))

    def set_bounds(self):
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
            self.direction.x -= 1
        elif self.rect.left <= 0:
            self.rect.left = 0
            self.direction.x = 1
    
    def update(self):
        self.display_health()
        self.motion()
        self.set_bounds()

    

class Player(Entity):
    def __init__(self, screen, groups, pos, size=32, speed=4, gravity=0.8, color=(255, 255, 255), health=100):
        super().__init__(groups, pos, size, speed, gravity, color, health)
        self.screen = screen
        self.jump_momentum = -12 # Give the player a stronger jump height

        self.font = pygame.font.SysFont('Arial', 36)
        self._last_health = None
        self._rendered_health = None
        
        self.vel = pygame.Vector2(0,0)
        self.acc = pygame.Vector2(0,0)

        self.ACC_SPEED = 0.5 # How fast I spped up
        self.FRICTION = 0.9 # Drag


    def apply_motion(self):
        # Apply Horizontal velocity and friction
        self.vel.x += self.acc.x * self.ACC_SPEED  # Add acceleration
        self.vel.x *= self.FRICTION               # Apply drag
        
        # Apply Gravity
        self.vel.y += self.gravity.y
        
        # Update Position and Rect
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.rect.center = self.pos

    def get_input(self, keys):
       
        # keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.acc.x = -1
            self.facing_right = False
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.acc.x = 1
            self.facing_right = True
        else:   
            self.acc.x = 0

        # Only jump if grounded
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.is_grounded:
            self.vel.y = self.jump_momentum
            self.is_grounded = False

    def set_boundary(self):
        # Bottom Boundary (Floor)
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.pos.y = self.rect.centery # Sync pos with rect!
            self.vel.y = 0                 # Stop falling
            self.is_grounded = True
        elif self.rect.top <= 0:
            self.rect.top = 0
            self.pos.y = self.rect.centery
            self.vel.y = 0

        # Horizontal Boundaries
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
            self.pos.x = self.rect.centerx
            self.vel.x = 0
        elif self.rect.left <= 0:
            self.rect.left = 0
            self.pos.x = self.rect.centerx
            self.vel.x = 1

    def display_health(self):
        if self.health != self._last_health:
            self._rendered_health = self.font.render(f"Health: {self.health}", True, self.color)
            self._last_health = self.health
        self.screen.blit(self._rendered_health, (screen_width - 200, 0))

    def update(self):
        self.display_health()
        self.check_death()
        # self.get_input() # Player can get input
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