import pygame

from settings import WHITE, FONT, WIDTH, HUD_HEIGHT, RED, GRAY, HUD

def draw_hud(screen, player):
      # HUD
    pygame.draw.rect(screen, HUD,(0, 0, WIDTH, HUD_HEIGHT))
        
    title_text = FONT.render("Convention Quest", True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH // 2, HUD_HEIGHT // 2))   
    screen.blit(title_text, title_rect)
    draw_health_bar(screen, 20, 200, 30, player.hp, player.max_hp)

    merch_text = FONT.render(f"Merch: {player.score}", True, WHITE)
    merch_rect = merch_text.get_rect(topright=(screen.get_width() - 20, 20))
        
    screen.blit(merch_text, merch_rect)
    

def draw_health_bar(screen, x, width, height, hp, max_hp):

    y = (HUD_HEIGHT - height) // 2

    # background (empty health)
    pygame.draw.rect(screen, GRAY, (x, y, width, height))

    # health amount
    health_width = int((hp / max_hp) * width)
    pygame.draw.rect(screen, RED, (x, y, health_width, height))

    # outline
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)

    # HP text
    hp_text = FONT.render(f"HP: {hp}", True, WHITE)
    hp_rect = hp_text.get_rect(center=(x + width//2, y + height//2))

    screen.blit(hp_text, hp_rect)
