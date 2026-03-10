import pygame

def get_booth_rects():
    booth_rects = []
    for x in range(100, 900, 200):
        booth_rects.append(pygame.Rect(x, 150, 100, 60))
        booth_rects.append(pygame.Rect(x, 350, 100, 60))
    return booth_rects