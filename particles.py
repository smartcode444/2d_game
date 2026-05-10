import pygame, sys, random

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Platformer")

BLACK = (0,0,0)
WHITE = (255,255,255)
FPS = 60

# Spawn a bunch of rectangles in one position
#  Make them scatter in random directions
# Make their size decrease with time
class Particle:
    def __init__(self, pos):
        self.x, self.y = pos
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-3, 3)

        self.size = random.randint(10, 25)
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.size -= 0.3

    def draw(self, surface):
        if self.size > 0:
            rect = pygame.Rect(self.x, self.y, self.size, self.size)
            pygame.draw.rect(surface, self.color, rect)

particles = []
running = True
while running:
    screen.fill('black')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN: 
            for _ in range(30):
                particles.append(Particle(event.pos))
            
    for p in particles[:]:
        p.update()
        p.draw(screen)

        if p.size <= 0:
            particles.remove(p)

    pygame.display.update()
    clock.tick(FPS)