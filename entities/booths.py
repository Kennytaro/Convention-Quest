import pygame

from settings import WIDTH, HEIGHT, HUD_HEIGHT

def get_booth_rects(level = 0):
    booth_rects = []
    
    if level == 0:
        for x in range(100, 900, 200):
            booth_rects.append(pygame.Rect(x, 150, 100, 60))
            booth_rects.append(pygame.Rect(x, 350, 100, 60))
    elif level == 1:
        rows_y = [HUD_HEIGHT + 80, HEIGHT // 2, HEIGHT - 100]  # 3 evenly spaced lines
        for y in rows_y:
            for x in range(100, WIDTH - 100, 140):
                booth_rects.append(pygame.Rect(x, y, 80, 60))
    return booth_rects
