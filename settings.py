import pygame

pygame.init()

#Eventaully make as debug screen

WIDTH = 960
HEIGHT = 540
HUD_HEIGHT = 50

HAZARD_COUNT = 6
MERCH_COUNT = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (80,80,80)
#used for booths
LIGHT_GRAY = (150,150,150)
RED = (200,40,40)
GREEN = (40,200,40)
#BLUE
USER_COLOR = (40,40,200)
#Yellow
MERCH_COLOR = (240, 200, 100)
#Red
HAZARD_COLOR = (200, 80, 80)
#Dark Gray
HUD = (30, 30, 40)
#Tint, darker black tint kinda
OVERLAY = (0, 0, 0, 140)

FONT = pygame.font.SysFont(None, 24)

MOVE_KEYS = {
    "up":    [pygame.K_UP, pygame.K_w],
    "left":  [pygame.K_LEFT, pygame.K_a],
    "down":  [pygame.K_DOWN, pygame.K_s],
    "right": [pygame.K_RIGHT, pygame.K_d],
}
