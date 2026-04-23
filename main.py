import pygame
import sys

from systems.game import Game
from settings import clock
from systems.audio import AudioBank

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
                    pygame.mixer.music.load("assets/323Beat.wav")
                    pygame.mixer.music.set_volume(0.7)
                    pygame.mixer.music.play(-1)
            if event.key == pygame.K_ESCAPE:
                if game.state == "play":
                    game.state = "paused"
                elif game.state == "paused":
                    game.state = "play"
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_p:
                game.show_particles = not game.show_particles
            if event.key == pygame.K_f:
                game.show_flashing = not game.show_flashing
            if event.key == pygame.K_m: 
                game.toggle_audio()
    game.update(dt)
    game.draw()

    pygame.display.flip() 

pygame.quit()

sys.exit()
