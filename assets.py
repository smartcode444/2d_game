import pygame
from settings import screen_width, screen_height

class Assests:
    def __init__(self):
        pass

class Weapon:
    def __init__(self, groups, length, breadth, damage, fire_rate, range, bullet_speed, ammo_capacity, color):
        # Size
        self.length = length
        self.breadth = breadth
        
        self.damage = damage
        self.fire_rate = fire_rate
        self.range = range
        self.bullet_speed = bullet_speed
        self.ammo_capacity = ammo_capacity

        # Placeholder image and rect
        self.image = pygame.Surface((self.length, self.breadth))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft = self.pos)

class Gun(pygame.sprite.Sprite, Weapon):
    def __init__(self, groups, length=7, breadth=20, damage=4, fire_rate=0.02, range=200, bullet_speed = 4, ammo_capacity=20, color=(0,255,255)):
        Weapon.__init__(self, self.groups, self.length, self.breadth, self.damage, self.fire_rate, self.range, self.bullet_speed, self.ammo_capacity, self.color)
        pygame.sprite.Sprite.__init__(self, groups)

    def update(self):
        pass

    def draw(self):
        pass
        
class Bullets(pygame.sprite.Sprite):
    def __init__(self, mouse_pos, pos, groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.mouse_pos = mouse_pos
        self.pos = pos
        self.image = pygame.Surface((10, 10))
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(pos.x, pos.y))

        self.speed = 5
        self.get_direction()

    def get_direction(self):
        vec = self.mouse_pos - self.pos
        if vec.length() > 0:
            self.velocity = vec.normalize() * self.speed
        else:
            self.velocity = pygame.Vector2(0, 0)
        # print(self.unit_vec)

    def update(self):
        self.pos += self.velocity
        self.rect.center = self.pos

        if not(0 <= self.rect.x <= screen_width or 0 <= self.rect.y <= screen_height):
            self.kill()
    
