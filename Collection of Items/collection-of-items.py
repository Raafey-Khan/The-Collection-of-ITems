import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Collect the Items")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (width // 2, height // 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5
        if keys[pygame.K_UP]:
            self.rect.y -= 5
        if keys[pygame.K_DOWN]:
            self.rect.y += 5

        # Keep the player within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, height - self.rect.height))

# Item class
class Item(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(0, height - self.rect.height)
        self.speed = random.randint(1, 3)
        self.direction = random.choice([-1, 1])

    def update(self):
        self.rect.x += self.speed * self.direction
        if self.rect.left < 0 or self.rect.right > width:
            self.direction *= -1

# Create game objects
player = Player()
items = pygame.sprite.Group()
enemies = pygame.sprite.Group()

# Create multiple items
for _ in range(10):
    item = Item()
    items.add(item)

# Create multiple enemies
for _ in range(5):
    enemy = Enemy()
    enemies.add(enemy)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    player.update()
    enemies.update()

    # Collision detection - player and items
    item_collisions = pygame.sprite.spritecollide(player, items, True)
    for item in item_collisions:
        items.add(Item())

    # Collision detection - player and enemies
    enemy_collisions = pygame.sprite.spritecollide(player, enemies, False)
    if enemy_collisions:
        running = False

    # Render
    screen.fill(WHITE)
    screen.blit(player.image, player.rect)
    items.draw(screen)
    enemies.draw(screen)

    # Refresh the display
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
