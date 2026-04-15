import pygame
import random

from settings import HAZARD_COLOR, WIDTH, HUD_HEIGHT, HEIGHT, HAZARD_COUNT
from entities.booths import get_booth_rects

class Hazard:#creates hazard
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        
    def draw(self, screen):
        pygame.draw.rect(screen, HAZARD_COLOR, self.rect)
    
def spawn_hazards(merchs, player_rect): #sapwn hazards
    # Build booth rects to match exactly what draw_world() renders
        booth_rects = get_booth_rects()
        
        hazards = []
        for _ in range(HAZARD_COUNT):
            attempts = 0
            while True:
                x = random.randint(100, WIDTH - 100)
                y = random.randint(HUD_HEIGHT + 100, HEIGHT - 100)
                new_hazard = Hazard(x, y)

                #   Check collision with booths AND merchs AND player AND hazards
                booth_collision = any(new_hazard.rect.colliderect(r) for r in booth_rects)
                merch_collision = any(new_hazard.rect.colliderect(m.rect) for m in merchs)
                player_collision = new_hazard.rect.colliderect(player_rect)
                hazard_collision = any(new_hazard.rect.colliderect(h.rect) for h in hazards)


                attempts += 1
                if not (booth_collision or merch_collision or player_collision or hazard_collision) or attempts > 50:
                    hazards.append(new_hazard)
                    break

        return hazards


