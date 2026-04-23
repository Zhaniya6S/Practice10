import pygame
import sys
import random
import os
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
INITIAL_SPEED = 5

ROAD_LEFT = 50
ROAD_RIGHT = 350

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 200, 50)
YELLOW = (255, 220, 50)
GOLD = (255, 200, 0)
BLUE = (50, 150, 255)
ORANGE = (255, 140, 0)
LIGHT_GRAY = (180, 180, 190)
DARK_GRAY = (60, 60, 70)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RACER GAME - Collect Coins!")
clock = pygame.time.Clock()

font_small = pygame.font.SysFont("Arial", 18)
font_medium = pygame.font.SysFont("Arial", 28)
font_large = pygame.font.SysFont("Arial", 48)

speed = INITIAL_SPEED
score = 0
coins_collected = 0
level = 1
debug_mode = False
invincible_frames = 0

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        player_width = 220
        player_height = 150
        
        image_path = os.path.join(os.path.dirname(__file__), "Player.png")
        if os.path.exists(image_path):
            self.original_image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.original_image, (player_width, player_height))
            print(f"Player.png loaded, size {player_width}x{player_height}")
        else:
            print(f"File not found: {image_path}")
            self.image = pygame.Surface((player_width, player_height), pygame.SRCALPHA)
            self.image.fill((0, 180, 0))
        
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 8
        
        self.mask = pygame.mask.from_surface(self.image)
    
    def move(self):
        keys = pygame.key.get_pressed()
        
        if keys[K_LEFT]:
            new_x = self.rect.x - self.speed
            if new_x >= ROAD_LEFT - (self.rect.width // 2):
                self.rect.x = new_x
        
        if keys[K_RIGHT]:
            new_x = self.rect.x + self.speed
            if new_x + self.rect.width <= ROAD_RIGHT + (self.rect.width // 2):
                self.rect.x = new_x
        
        min_x = ROAD_LEFT - (self.rect.width // 2)
        max_x = ROAD_RIGHT - (self.rect.width // 2)
        
        if self.rect.x < min_x:
            self.rect.x = min_x
        if self.rect.x > max_x:
            self.rect.x = max_x
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if debug_mode:
            pygame.draw.rect(surface, RED, self.rect, 3)
            pygame.draw.line(surface, (255, 255, 0), (ROAD_LEFT, 0), (ROAD_LEFT, SCREEN_HEIGHT), 2)
            pygame.draw.line(surface, (255, 255, 0), (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_HEIGHT), 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        enemy_width = 80
        enemy_height = 100
        
        image_path = os.path.join(os.path.dirname(__file__), "Enemy.png")
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (enemy_width, enemy_height))
            print("Enemy.png loaded")
        else:
            print(f"File not found: {image_path}")
            self.image = pygame.Surface((enemy_width, enemy_height))
            self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        self.reset_position()
        self.mask = pygame.mask.from_surface(self.image)
    
    def reset_position(self):
        min_x = ROAD_LEFT
        max_x = ROAD_RIGHT - self.rect.width
        if max_x < min_x:
            max_x = min_x
        self.rect.x = random.randint(min_x, max_x)
        self.rect.y = -self.rect.height - random.randint(100, 400)
    
    def move(self):
        global score
        self.rect.y += speed
        if self.rect.top > SCREEN_HEIGHT:
            score += 1
            self.reset_position()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if debug_mode:
            pygame.draw.rect(surface, BLUE, self.rect, 3)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        image_path = os.path.join(os.path.dirname(__file__), "Coin.png")
        if os.path.exists(image_path):
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (45, 45))
            print("Coin.png loaded")
        else:
            print(f"File not found: {image_path}")
            self.image = pygame.Surface((45, 45))
            self.image.fill(YELLOW)
            pygame.draw.circle(self.image, GOLD, (22, 22), 20)
        
        self.rect = self.image.get_rect()
        self.value = 1
        self.reset_position()
    
    def reset_position(self):
        min_x = ROAD_LEFT
        max_x = ROAD_RIGHT - self.rect.width
        if max_x < min_x:
            max_x = min_x
        self.rect.x = random.randint(min_x, max_x)
        self.rect.y = random.randint(-500, -50)
    
    def move(self):
        self.rect.y += speed
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if debug_mode:
            pygame.draw.rect(surface, GREEN, self.rect, 2)

class Background:
    def __init__(self):
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.create_road()
        self.y1 = 0
        self.y2 = -SCREEN_HEIGHT
        self.speed = 3
    
    def create_road(self):
        self.image.fill((40, 40, 50))
        
        pygame.draw.rect(self.image, DARK_GRAY, (0, 0, ROAD_LEFT, SCREEN_HEIGHT))
        pygame.draw.rect(self.image, DARK_GRAY, (ROAD_RIGHT, 0, SCREEN_WIDTH - ROAD_RIGHT, SCREEN_HEIGHT))
        
        pygame.draw.line(self.image, LIGHT_GRAY, (ROAD_LEFT, 0), (ROAD_LEFT, SCREEN_HEIGHT), 3)
        pygame.draw.line(self.image, LIGHT_GRAY, (ROAD_RIGHT, 0), (ROAD_RIGHT, SCREEN_HEIGHT), 3)
        
        road_center = (ROAD_LEFT + ROAD_RIGHT) // 2
        for y in range(0, SCREEN_HEIGHT, 40):
            pygame.draw.rect(self.image, (255, 255, 200), (road_center - 5, y, 10, 25))
        
        for y in range(0, SCREEN_HEIGHT, 60):
            pygame.draw.rect(self.image, (255, 255, 150), (ROAD_LEFT + 20, y, 5, 30))
            pygame.draw.rect(self.image, (255, 255, 150), (ROAD_RIGHT - 25, y, 5, 30))
    
    def update(self):
        self.y1 += self.speed
        self.y2 += self.speed
        if self.y1 >= SCREEN_HEIGHT:
            self.y1 = -SCREEN_HEIGHT
        if self.y2 >= SCREEN_HEIGHT:
            self.y2 = -SCREEN_HEIGHT
    
    def draw(self, surface):
        surface.blit(self.image, (0, self.y1))
        surface.blit(self.image, (0, self.y2))

def draw_ui():
    stats_surface = pygame.Surface((160, 100))
    stats_surface.set_alpha(200)
    stats_surface.fill(BLACK)
    screen.blit(stats_surface, (5, 5))
    
    score_text = font_small.render(f"Score: {score}", True, GOLD)
    coins_text = font_small.render(f"Coins: {coins_collected}", True, YELLOW)
    level_text = font_small.render(f"Level: {level}", True, BLUE)
    speed_text = font_small.render(f"Speed: {int(speed)}", True, ORANGE)
    
    screen.blit(score_text, (15, 12))
    screen.blit(coins_text, (15, 32))
    screen.blit(level_text, (15, 52))
    screen.blit(speed_text, (15, 72))
    
    coins_needed = 5 - (coins_collected % 5)
    if coins_needed == 0:
        coins_needed = 5
    progress = (coins_collected % 5) / 5 * 100
    pygame.draw.rect(screen, DARK_GRAY, (SCREEN_WIDTH - 115, 15, 105, 12))
    pygame.draw.rect(screen, GOLD, (SCREEN_WIDTH - 115, 15, progress * 1.05, 12))
    next_text = font_small.render(f"Next lvl: {coins_needed}", True, WHITE)
    screen.blit(next_text, (SCREEN_WIDTH - 110, 30))

def show_game_over():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(RED)
    screen.blit(overlay, (0, 0))
    
    texts = [
        (font_large.render("GAME OVER!", True, WHITE), SCREEN_HEIGHT // 2 - 100),
        (font_medium.render(f"Final Score: {score}", True, GOLD), SCREEN_HEIGHT // 2 - 30),
        (font_medium.render(f"Coins: {coins_collected}", True, YELLOW), SCREEN_HEIGHT // 2 + 10),
        (font_small.render(f"Level: {level}", True, WHITE), SCREEN_HEIGHT // 2 + 50),
        (font_small.render("Press SPACE to restart | ESC to quit", True, LIGHT_GRAY), SCREEN_HEIGHT // 2 + 120)
    ]
    
    for text, y_pos in texts:
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_pos))
        screen.blit(text, text_rect)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                return False
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return True
                if event.key == K_ESCAPE:
                    return False
    return False

def reset_game():
    global speed, score, coins_collected, level, player, enemy, coin, background, invincible_frames
    speed = INITIAL_SPEED
    score = 0
    coins_collected = 0
    level = 1
    invincible_frames = 0
    player = Player()
    enemy = Enemy()
    coin = Coin()
    background = Background()
    print("\n" + "="*40)
    print("GAME RESTARTED!")
    print("="*40 + "\n")

reset_game()
running = True
game_over = False

print("=" * 50)
print("RACER GAME - ROAD BOUNDARIES")
print("=" * 50)
print("Arrow keys ← → - movement")
print("D - debug mode")
print("ESC - exit")
print("=" * 50)
print("Car does not go beyond road edges!")
print("Any contact = GAME OVER!")
print("=" * 50)
print("\nLoading images...")

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_d:
                debug_mode = not debug_mode
                if debug_mode:
                    print("Debug mode ON - yellow lines = road boundaries")
                else:
                    print("Debug mode OFF")
    
    if not game_over:
        background.update()
        player.move()
        enemy.move()
        coin.move()
        
        offset_x = enemy.rect.x - player.rect.x
        offset_y = enemy.rect.y - player.rect.y
        
        if player.mask.overlap(enemy.mask, (offset_x, offset_y)):
            game_over = True
            print("\n" + "="*40)
            print("COLLISION! GAME OVER")
            print(f"Coins collected: {coins_collected}")
            print(f"Level: {level}")
            print("="*40 + "\n")
        
        if player.rect.colliderect(coin.rect):
            coins_collected += 1
            coin.reset_position()
            invincible_frames = 30
            print(f"Coin collected! Total: {coins_collected}")
            
            if coins_collected % 5 == 0:
                level += 1
                speed += 1.5
                print(f"LEVEL {level}! Speed increased to {speed:.1f}")
        
        background.draw(screen)
        player.draw(screen)
        enemy.draw(screen)
        coin.draw(screen)
        draw_ui()
        
        if debug_mode:
            fps_text = font_small.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
            screen.blit(fps_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 25))
            inv_text = font_small.render(f"Inv: {invincible_frames}", True, WHITE)
            screen.blit(inv_text, (SCREEN_WIDTH - 100, SCREEN_HEIGHT - 45))
    
    else:
        if show_game_over():
            reset_game()
            game_over = False
        else:
            running = False
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()