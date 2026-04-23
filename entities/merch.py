import pygame
import random

from settings import MERCH_COLOR, MERCH_COUNT, WIDTH, HUD_HEIGHT, HEIGHT
from entities.booths import get_booth_rects

def load_merch():
    img_path = [
        "assets/merch1.png",
        "assets/merch2.png",
        "assets/merch3.png"
    ]

    images = []
    for path in img_path:
        img = pygame.image.load(path).convert_alpha()
        img = pygame.transform.scale(img, (60, 60))
        images.append(img)
    return images
MERCH_IMAGES = load_merch()

class Merch: #Creates Merch
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.image = random.choice(MERCH_IMAGES)

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

def spawn_merchs(player_rect, count, level): #spawn Merch
    booth_rects = get_booth_rects(level)
    
    merchs = []
    for _ in range(count):
        attempts = 0
        while attempts < 50:
            x = random.randint(50, WIDTH - 50)
            y = random.randint(HUD_HEIGHT + 50, HEIGHT - 50)
            new_merch = Merch(x, y)

            booth_collision = any(new_merch.rect.colliderect(r) for r in booth_rects)
            player_collision = new_merch.rect.colliderect(player_rect)
            merch_collision = any(new_merch.rect.colliderect(h.rect) for h in merchs)
            
            if not (booth_collision or player_collision or merch_collision):
                merchs.append(new_merch)
                break

            attempts += 1

            if attempts > 50:
                break

    return merchs
