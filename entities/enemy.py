import pygame
import random

from settings import HAZARD_COLOR, WIDTH, HUD_HEIGHT, HEIGHT, HAZARD_COUNT
from entities.booths import get_booth_rects
from systems.levels import get_level
class Hazard:#creates hazard
    def __init__(self, x, y, speed = 120):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.speed = speed
        
        self.dx = random.choice([-1, 1])
        self.dy = random.choice([-1, 1])


    def draw(self, screen):
        pygame.draw.rect(screen, HAZARD_COLOR, self.rect)

    def update(self, dt, hazards, booths):
        # Move X
        self.rect.x += self.dx * self.speed * dt

        # screen bounce X
        if self.rect.left <= 0:
            self.rect.left = 0
            self.dx *= -1
        elif self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            self.dx *= -1

        # booth bounce X
        for booth in booths:
            if self.rect.colliderect(booth):
                if self.dx > 0:
                    self.rect.right = booth.left
                else:
                    self.rect.left = booth.right
                self.dx *= -1
                break  

        # Move Y
        self.rect.y += self.dy * self.speed * dt

        # screen bounce Y
        if self.rect.top <= HUD_HEIGHT:
            self.rect.top = HUD_HEIGHT
            self.dy *= -1
        elif self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.dy *= -1

        # booth bounce Y
        for booth in booths:
            if self.rect.colliderect(booth):
                if self.dy > 0:
                    self.rect.bottom = booth.top
                else:
                    self.rect.top = booth.bottom
                self.dy *= -1
                break
        for other in hazards:
            if other is self:
                continue

            if self.rect.colliderect(other.rect):

                # simple horizontal resolution
                if abs(self.rect.centerx - other.rect.centerx) > abs(self.rect.centery - other.rect.centery):
                    # X collision
                    if self.rect.centerx < other.rect.centerx:
                        self.rect.right = other.rect.left
                    else:
                        self.rect.left = other.rect.right

                    self.dx *= -1
                    other.dx *= -1

                else:
                    # Y collision
                    if self.rect.centery < other.rect.centery:
                        self.rect.bottom = other.rect.top
                    else:
                        self.rect.top = other.rect.bottom

                    self.dy *= -1
                    other.dy *= -1 

def spawn_hazards(merchs, player_rect, count, speed, booths): #sapwn hazards
    # Build booth rects to match exactly what draw_world() renders        
        hazards = []
        for _ in range(count):
            attempts = 0
            while True:
                x = random.randint(100, WIDTH - 100)
                y = random.randint(HUD_HEIGHT + 100, HEIGHT - 100)
                new_hazard = Hazard(x, y, speed)

                #   Check collision with booths AND merchs AND player AND hazards
                booth_collision = any(new_hazard.rect.colliderect(r) for r in booths)
                merch_collision = any(new_hazard.rect.colliderect(m.rect) for m in merchs)
                player_collision = new_hazard.rect.colliderect(player_rect)
                hazard_collision = any(new_hazard.rect.colliderect(h.rect) for h in hazards)


                attempts += 1
                if not (booth_collision or merch_collision or player_collision or hazard_collision) or attempts > 50:
                    hazards.append(new_hazard)
                    break

        return hazards


