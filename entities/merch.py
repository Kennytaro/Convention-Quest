import pygame
import random

from settings import MERCH_COLOR, MERCH_COUNT, WIDTH, HUD_HEIGHT, HEIGHT
from entities.booths import get_booth_rects
class Merch: #Creates Merch
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 20)

    def draw(self, screen):
        pygame.draw.circle(screen, MERCH_COLOR, self.rect.center, 10)

def spawn_merchs(player_rect, count, level): #spawn Merch
    booth_rects = get_booth_rects(level)
    
    merchs = []
    for _ in range(count):
        attempts = 0
        while True:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(HUD_HEIGHT + 50, HEIGHT - 50)
            new_merch = Merch(x, y)

            booth_collision = any(new_merch.rect.colliderect(r) for r in booth_rects)
            player_collision = new_merch.rect.colliderect(player_rect)
            merch_collision = any(new_merch.rect.colliderect(h.rect) for h in merchs)

            attempts += 1
            if not (booth_collision or player_collision or merch_collision) or attempts > 50:
                merchs.append(new_merch)
                break

    return merchs
