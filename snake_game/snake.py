import pygame
import random
import sys

pygame.init()

WIDTH = 600
HEIGHT = 400

CELL_SIZE = 40

GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

INITIAL_SPEED = 6
FOODS_PER_LEVEL = 3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 150, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game - Easy Version")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Arial", 24)
font_large = pygame.font.SysFont("Arial", 48)

class Snake:
    def __init__(self):
        center_x = GRID_WIDTH // 2
        center_y = GRID_HEIGHT // 2
        
        self.body = [
            [center_x, center_y],
            [center_x - 1, center_y],
            [center_x - 2, center_y]
        ]
        self.direction = "RIGHT"
        self.grow_flag = False
    
    def move(self):
        head = self.body[0].copy()
        
        if self.direction == "RIGHT":
            head[0] += 1
        elif self.direction == "LEFT":
            head[0] -= 1
        elif self.direction == "UP":
            head[1] -= 1
        elif self.direction == "DOWN":
            head[1] += 1
        
        self.body.insert(0, head)
        
        if not self.grow_flag:
            self.body.pop()
        else:
            self.grow_flag = False
    
    def grow(self):
        self.grow_flag = True
    
    def check_collision(self):
        head = self.body[0]
        
        if (head[0] < 0 or head[0] >= GRID_WIDTH or 
            head[1] < 0 or head[1] >= GRID_HEIGHT):
            return True
        
        for segment in self.body[1:]:
            if head == segment:
                return True
        
        return False
    
    def change_direction(self, new_dir):
        opposites = {"RIGHT": "LEFT", "LEFT": "RIGHT", "UP": "DOWN", "DOWN": "UP"}
        if new_dir != opposites.get(self.direction):
            self.direction = new_dir
    
    def draw(self, surface):
        for i, segment in enumerate(self.body):
            x = segment[0] * CELL_SIZE
            y = segment[1] * CELL_SIZE
            color = DARK_GREEN if i == 0 else GREEN
            
            pygame.draw.rect(surface, color, (x, y, CELL_SIZE - 2, CELL_SIZE - 2))
            pygame.draw.rect(surface, BLACK, (x, y, CELL_SIZE - 2, CELL_SIZE - 2), 2)
        
        head = self.body[0]
        head_x = head[0] * CELL_SIZE
        head_y = head[1] * CELL_SIZE
        eye_size = 5
        
        if self.direction == "RIGHT":
            pygame.draw.circle(surface, WHITE, (head_x + 30, head_y + 12), eye_size)
            pygame.draw.circle(surface, WHITE, (head_x + 30, head_y + 28), eye_size)
            pygame.draw.circle(surface, BLACK, (head_x + 32, head_y + 12), 2)
            pygame.draw.circle(surface, BLACK, (head_x + 32, head_y + 28), 2)
        elif self.direction == "LEFT":
            pygame.draw.circle(surface, WHITE, (head_x + 10, head_y + 12), eye_size)
            pygame.draw.circle(surface, WHITE, (head_x + 10, head_y + 28), eye_size)
            pygame.draw.circle(surface, BLACK, (head_x + 8, head_y + 12), 2)
            pygame.draw.circle(surface, BLACK, (head_x + 8, head_y + 28), 2)
        elif self.direction == "UP":
            pygame.draw.circle(surface, WHITE, (head_x + 12, head_y + 10), eye_size)
            pygame.draw.circle(surface, WHITE, (head_x + 28, head_y + 10), eye_size)
            pygame.draw.circle(surface, BLACK, (head_x + 12, head_y + 8), 2)
            pygame.draw.circle(surface, BLACK, (head_x + 28, head_y + 8), 2)
        elif self.direction == "DOWN":
            pygame.draw.circle(surface, WHITE, (head_x + 12, head_y + 30), eye_size)
            pygame.draw.circle(surface, WHITE, (head_x + 28, head_y + 30), eye_size)
            pygame.draw.circle(surface, BLACK, (head_x + 12, head_y + 32), 2)
            pygame.draw.circle(surface, BLACK, (head_x + 28, head_y + 32), 2)

class Food:
    def __init__(self, snake_body):
        self.position = [0, 0]
        self.randomize_position(snake_body)
    
    def randomize_position(self, snake_body):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, GRID_HEIGHT - 1)
            if [x, y] not in snake_body:
                self.position = [x, y]
                break
    
    def draw(self, surface):
        x = self.position[0] * CELL_SIZE
        y = self.position[1] * CELL_SIZE
        
        center_x = x + CELL_SIZE // 2
        center_y = y + CELL_SIZE // 2
        
        pygame.draw.circle(surface, RED, (center_x, center_y), 15)
        pygame.draw.circle(surface, (255, 100, 100), (center_x, center_y), 10)
        pygame.draw.circle(surface, (255, 150, 150), (center_x, center_y), 5)

def show_game_over(score, level):
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    
    game_over_text = font_large.render("GAME OVER!", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, GREEN)
    restart_text = font.render("Press SPACE to restart", True, LIGHT_GRAY)
    quit_text = font.render("Press ESC to quit", True, LIGHT_GRAY)
    
    screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 80))
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 20))
    screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, HEIGHT//2 + 10))
    screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 60))
    screen.blit(quit_text, (WIDTH//2 - quit_text.get_width()//2, HEIGHT//2 + 90))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                if event.key == pygame.K_ESCAPE:
                    return False
    return False

def reset_game():
    global snake, food, score, level, speed, foods_eaten
    snake = Snake()
    food = Food(snake.body)
    score = 0
    level = 1
    speed = INITIAL_SPEED
    foods_eaten = 0

snake = Snake()
food = Food(snake.body)
score = 0
level = 1
speed = INITIAL_SPEED
foods_eaten = 0
running = True
game_over = False

print("=== SNAKE GAME - EASY VERSION ===")
print(f"Поле: {GRID_WIDTH} x {GRID_HEIGHT} клеток")
print("Управление: стрелки ← ↑ ↓ →")
print("ESC - выход")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if not game_over:
                if event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
    
    if not game_over:
        snake.move()
        
        if snake.check_collision():
            game_over = True
        
        if snake.body[0] == food.position:
            snake.grow()
            score += 1
            foods_eaten += 1
            food.randomize_position(snake.body)
            
            if foods_eaten >= FOODS_PER_LEVEL:
                level += 1
                speed += 1
                foods_eaten = 0
                print(f"★ Level {level}! Speed: {speed}")
        
        screen.fill(BLACK)
        
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))
        
        snake.draw(screen)
        food.draw(screen)
        
        score_text = font.render(f"Score: {score}", True, WHITE)
        level_text = font.render(f"Level: {level}", True, GREEN)
        next_text = font.render(f"Next: {FOODS_PER_LEVEL - foods_eaten}", True, BLUE)
        
        pygame.draw.rect(screen, BLACK, (5, 5, 130, 80))
        pygame.draw.rect(screen, GRAY, (5, 5, 130, 80), 2)
        
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 35))
        screen.blit(next_text, (10, 60))
        
        pygame.draw.rect(screen, WHITE, (0, 0, WIDTH, HEIGHT), 3)
    
    else:
        if show_game_over(score, level):
            reset_game()
            game_over = False
        else:
            running = False
    
    pygame.display.update()
    clock.tick(speed)

pygame.quit()
sys.exit()