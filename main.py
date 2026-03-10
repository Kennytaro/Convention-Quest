import pygame
import sys

from systems.game import Game
from settings import clock

game = Game()
clock = pygame.time.Clock()
pygame.display.set_caption("Convention Quest")

running = True

while running:

    dt = clock.tick(game.fps) / 1000.0
    dt = min(dt, 0.05)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game.state in ("title","gameover", "win"):
                    game = Game()
                    game.state = "play"
            if event.key == pygame.K_ESCAPE:
                if game.state == "play":
                    game.state = "paused"
                elif game.state == "paused":
                    game.state = "play"
            if event.key == pygame.K_q:
                running = False
    
    game.update(dt)
    game.draw()

    pygame.display.flip() 

pygame.quit()

sys.exit()
