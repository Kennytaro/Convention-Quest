import pygame

from settings import USER_COLOR, HUD_HEIGHT, WIDTH, HEIGHT, MOVE_KEYS
from entities.booths import get_booth_rects

class Player:
    def __init__(self, x, y): #move to global variable
        self.speed = 200
        self.size = 40
        self.hp = 100
        self.max_hp = 100
        self.score = 0
        self.rect = pygame.Rect(x, y, self.size, self.size)
        self.invincible_for = 0.0

    @property
    def is_invincible(self):
        return self.invincible_for > 0

    def update(self, dt):
        if self.invincible_for > 0:
            self.invincible_for = max(0.0, self.invincible_for - dt)

        keys = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if any(keys[k] for k in MOVE_KEYS["left"]):
            dx -= 1
        if any(keys[k] for k in MOVE_KEYS["right"]):
            dx += 1
        if any(keys[k] for k in MOVE_KEYS["up"]):
            dy -= 1
        if any(keys[k] for k in MOVE_KEYS["down"]):
            dy += 1

        if dx != 0 or dy != 0:
            length = (dx**2 + dy**2)**0.5
            dx /= length
            dy /= length

        booths = get_booth_rects()

        if dx != 0:
            self.rect.x += dx * self.speed * dt
            for booth in booths:
                if self.rect.colliderect(booth):
                    if dx > 0:
                        self.rect.right = booth.left
                    elif dx < 0:
                        self.rect.left = booth.right

        if dy != 0:
            self.rect.y += dy * self.speed * dt
            for booth in booths:
                if self.rect.colliderect(booth):
                    if dy > 0:
                        self.rect.bottom = booth.top
                    elif dy < 0:
                        self.rect.top = booth.bottom

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(WIDTH, self.rect.right)
        self.rect.top = max(HUD_HEIGHT, self.rect.top)
        self.rect.bottom = min(HEIGHT, self.rect.bottom)

        self.rect.x += dx * self.speed * dt
        self.rect.y += dy * self.speed * dt

    def draw(self, screen):
        pygame.draw.rect(screen, USER_COLOR, self.rect)    
