import pygame
import random

WIDTH = 800
HEIGHT = 600
FPS = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DODGE THE DOTS")
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.score = 0  # Score based on time alive
        self.armor = 0  # Armor hits

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 2
        if keys[pygame.K_RIGHT]:
            self.rect.x += 2
        if keys[pygame.K_UP]:
            self.rect.y -= 2
        if keys[pygame.K_DOWN]:
            self.rect.y += 2

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.speedx = random.randrange(-2, 2)
        self.speedy = random.randrange(-2, 2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speedx = -self.speedx
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.speedy = -self.speedy

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    screen.blit(text_surface, text_rect)

def show_score(player):
    score_text = "Score: " + str(player.score)
    armor_text = "Armor: " + str(player.armor)
    draw_text(score_text, pygame.font.Font(None, 36), WHITE, 70, 10)
    draw_text(armor_text, pygame.font.Font(None, 36), WHITE, WIDTH - 70, 10)

def create_powerup():
    powerup = Enemy()
    powerup.image.fill((0, 0, 255))
    return powerup

all_sprites = pygame.sprite.Group()
player = Player()
enemies = pygame.sprite.Group()
powerups = pygame.sprite.Group()
for i in range(10):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)
all_sprites.add(player)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # collision between player and enemies
    enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
    if enemy_hits:
        if player.armor > 0:
            player.armor -= 1
        else:
            running = False

    # collision between player and powerups
    powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
    if powerup_hits:
        player.armor += 1
        player.score += 1

    # Spawn powerups randomly
    if len(powerups) == 0:
        powerup = create_powerup()
        all_sprites.add(powerup)
        powerups.add(powerup)

    # Draw graphics
    screen.fill(BLACK)
    all_sprites.draw(screen)
    draw_text("Dodge the Dots with the Arrow Keys", pygame.font.Font(None, 36), WHITE, WIDTH / 2, 10)
    show_score(player)
    pygame.display.flip()