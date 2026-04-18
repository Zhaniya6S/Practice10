import pygame
import sys
import random
from pygame.locals import *

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60
INITIAL_SPEED = 5

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
        try:
            self.image = pygame.image.load("Player_small.png")
            self.image = pygame.transform.scale(self.image, (160, 95))
            print("Загружен Player, размер 160x95")
        except:
            self.image = pygame.Surface((160, 95), pygame.SRCALPHA)
            self.create_wide_car()
            print("Создана широкая машина 160x95")
        
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 20
        self.speed = 7
        self.collision_rect = pygame.Rect(0, 0, 40, 30)
    
    def create_wide_car(self):
        pygame.draw.rect(self.image, (0, 180, 0), (15, 18, 130, 62))
        pygame.draw.rect(self.image, (0, 210, 0), (15, 18, 130, 32))
        pygame.draw.rect(self.image, (0, 150, 0), (45, 10, 70, 22))
        pygame.draw.rect(self.image, (135, 206, 235), (50, 14, 14, 14))
        pygame.draw.rect(self.image, (135, 206, 235), (68, 14, 14, 14))
        pygame.draw.rect(self.image, (135, 206, 235), (86, 14, 14, 14))
        pygame.draw.rect(self.image, (135, 206, 235), (104, 14, 14, 14))
        pygame.draw.circle(self.image, (30, 30, 30), (28, 78), 16)
        pygame.draw.circle(self.image, (30, 30, 30), (132, 78), 16)
        pygame.draw.circle(self.image, (80, 80, 80), (28, 78), 10)
        pygame.draw.circle(self.image, (80, 80, 80), (132, 78), 10)
        pygame.draw.circle(self.image, (255, 255, 100), (148, 28), 8)
        pygame.draw.circle(self.image, (255, 255, 100), (148, 48), 8)
        pygame.draw.circle(self.image, (255, 255, 150), (148, 28), 4)
        pygame.draw.circle(self.image, (255, 255, 150), (148, 48), 4)
        pygame.draw.circle(self.image, (255, 50, 50), (12, 28), 7)
        pygame.draw.circle(self.image, (255, 50, 50), (12, 48), 7)
        pygame.draw.line(self.image, GOLD, (25, 45), (135, 45), 5)
        pygame.draw.line(self.image, GOLD, (25, 55), (135, 55), 5)
        pygame.draw.rect(self.image, WHITE, (65, 65, 30, 12))
        font = pygame.font.SysFont("Arial", 12, bold=True)
        num = font.render("V8", True, BLACK)
        self.image.blit(num, (72, 67))
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > -30:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < SCREEN_WIDTH + 30:
            self.rect.x += self.speed
        
        if self.rect.left < -30:
            self.rect.left = -30
        if self.rect.right > SCREEN_WIDTH + 30:
            self.rect.right = SCREEN_WIDTH + 30
        
        self.collision_rect.center = self.rect.center
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if debug_mode:
            pygame.draw.rect(surface, RED, self.rect, 2)
            pygame.draw.rect(surface, (255, 255, 0), self.collision_rect, 2)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("Enemy_small.png")
            self.image = pygame.transform.scale(self.image, (55, 55))
        except:
            self.image = pygame.Surface((55, 55))
            self.image.fill(RED)
            pygame.draw.rect(self.image, DARK_GRAY, (10, 10, 35, 35))
        
        self.rect = self.image.get_rect()
        self.reset_position()
        self.collision_rect = pygame.Rect(0, 0, 25, 25)
    
    def reset_position(self):
        self.rect.x = random.randint(20, SCREEN_WIDTH - 20 - self.rect.width)
        self.rect.y = -self.rect.height - random.randint(100, 400)
    
    def move(self):
        global score
        self.rect.y += speed
        if self.rect.top > SCREEN_HEIGHT:
            score += 1
            self.reset_position()
        self.collision_rect.center = self.rect.center
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if debug_mode:
            pygame.draw.rect(surface, BLUE, self.rect, 2)
            pygame.draw.rect(surface, (255, 100, 100), self.collision_rect, 2)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        try:
            self.image = pygame.image.load("Coin_small.png")
            self.image = pygame.transform.scale(self.image, (25, 25))
        except:
            self.image = pygame.Surface((22, 22))
            self.image.fill(YELLOW)
            pygame.draw.circle(self.image, GOLD, (11, 11), 9)
        
        self.rect = self.image.get_rect()
        self.value = 1
        self.reset_position()
    
    def reset_position(self):
        self.rect.x = random.randint(15, SCREEN_WIDTH - 15)
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
        try:
            self.image = pygame.image.load("AnimatedStreet.png")
            self.image = pygame.transform.scale(self.image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.create_road()
        
        self.y1 = 0
        self.y2 = -SCREEN_HEIGHT
        self.speed = 3
    
    def create_road(self):
        self.image.fill((50, 50, 60))
        for y in range(0, SCREEN_HEIGHT, 50):
            pygame.draw.rect(self.image, (255, 255, 200), (SCREEN_WIDTH//2 - 5, y, 10, 30))
        pygame.draw.rect(self.image, DARK_GRAY, (0, 0, 40, SCREEN_HEIGHT))
        pygame.draw.rect(self.image, DARK_GRAY, (SCREEN_WIDTH-40, 0, 40, SCREEN_HEIGHT))
        pygame.draw.line(self.image, LIGHT_GRAY, (40, 0), (40, SCREEN_HEIGHT), 2)
        pygame.draw.line(self.image, LIGHT_GRAY, (SCREEN_WIDTH-40, 0), (SCREEN_WIDTH-40, SCREEN_HEIGHT), 2)
    
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
    stats_surface = pygame.Surface((130, 80))
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
    screen.blit(speed_text, (SCREEN_WIDTH - 75, 15))
    
    coins_needed = 5 - (coins_collected % 5)
    if coins_needed == 0:
        coins_needed = 5
    progress = (coins_collected % 5) / 5 * 100
    pygame.draw.rect(screen, DARK_GRAY, (SCREEN_WIDTH - 100, 50, 90, 8))
    pygame.draw.rect(screen, GOLD, (SCREEN_WIDTH - 100, 50, progress, 8))
    next_text = font_small.render(f"Next: {coins_needed}", True, WHITE)
    screen.blit(next_text, (SCREEN_WIDTH - 95, 35))

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

reset_game()
running = True
game_over = False

print("=== RACER GAME ===")
print("Стрелки ← → - движение")
print("D - режим отладки")
print("ESC - выход")

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_d:
                debug_mode = not debug_mode
    
    if not game_over:
        background.update()
        player.move()
        enemy.move()
        coin.move()
        
        if invincible_frames > 0:
            invincible_frames -= 1
        
        if invincible_frames <= 0:
            if player.collision_rect.colliderect(enemy.collision_rect):
                game_over = True
        
        if pygame.sprite.collide_rect(player, coin):
            coins_collected += 1
            coin.reset_position()
            invincible_frames = 60
            
            if coins_collected % 5 == 0:
                level += 1
                speed += 1.5
        
        background.draw(screen)
        player.draw(screen)
        enemy.draw(screen)
        coin.draw(screen)
        draw_ui()
        
        if debug_mode:
            fps_text = font_small.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
            screen.blit(fps_text, (SCREEN_WIDTH - 70, SCREEN_HEIGHT - 25))
    
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