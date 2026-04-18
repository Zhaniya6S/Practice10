import pygame
from pygame.locals import *

pygame.init()

PLAYER_SIZE = (100, 100)
ENEMY_SIZE = (55, 55)
COIN_SIZE = (25, 25)
BACKGROUND_SIZE = (400, 600)

def resize_image(input_path, output_path, size):
    try:
        original = pygame.image.load(input_path)
        resized = pygame.transform.scale(original, size)
        pygame.image.save(resized, output_path)
        print(f"✓ {input_path} -> {output_path} ({size[0]}x{size[1]})")
        return True
    except Exception as e:
        print(f"✗ Ошибка с {input_path}: {e}")
        return False

print("Изменение размеров...")
print("-" * 40)

resize_image("Player.png", "Player_small.png", PLAYER_SIZE)
resize_image("Enemy.png", "Enemy_small.png", ENEMY_SIZE)
resize_image("Coin.png", "Coin_small.png", COIN_SIZE)
resize_image("AnimatedStreet.png", "AnimatedStreet_small.png", BACKGROUND_SIZE)

print("-" * 40)
print(f"Готово! Player теперь {PLAYER_SIZE[0]}x{PLAYER_SIZE[1]}")

pygame.quit()