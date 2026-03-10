import pygame

from settings import GRAY, LIGHT_GRAY, HUD_HEIGHT, WIDTH, HEIGHT, WHITE, FONT
from entities.booths import get_booth_rects

def draw_world(screen):
    pygame.draw.rect(screen, GRAY, (0, HUD_HEIGHT, WIDTH, HEIGHT - HUD_HEIGHT))
    
    #Booths
    for rect in get_booth_rects():
        pygame.draw.rect(screen, LIGHT_GRAY, rect)

def draw_pause(screen):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 140))
    screen.blit(overlay, (0, 0))

    t = FONT.render("PAUSED", True, WHITE)
    r = t.get_rect(center=(WIDTH//2, HEIGHT//2 - 20))
    screen.blit(t, r)

    t2 = FONT.render("Press Q to Quit", True, WHITE)
    r2 = t2.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(t2, r2)

    t3 = FONT.render("Press ESC to Resume", True, WHITE)
    r3 = t3.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
    screen.blit(t3, r3)

    