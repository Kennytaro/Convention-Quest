from settings import WIDTH, HEIGHT, WHITE, GRAY, FONT, screen
from entities.player import Player
from entities.enemy import spawn_hazards
from entities.merch import spawn_merchs
from systems.world import draw_world, draw_pause
from systems.hud import draw_hud

class Game:
    fps = 60

    def __init__(self):

        self.player = Player(WIDTH//2,HEIGHT//2)

        self.merchs = []
        self.hazards = []

        self.spawn_level()

        self.state = "title"

    def spawn_level(self):

        self.merchs.clear()
        self.hazards.clear()

        self.merchs = spawn_merchs(player_rect=self.player.rect)
        self.hazards = spawn_hazards(self.merchs, player_rect=self.player.rect)
    
    def update(self,dt):

        if self.state not in ("play",):
            return

        self.player.update(dt)

        #Merch collection
        for merch in self.merchs[:]:
            if self.player.rect.colliderect(merch.rect):
                self.merchs.remove(merch)
                self.player.score += 1
                if self.player.score >= 10:
                    self.state = "win"

        #Hazard damage + i-frame
        for hz in self.hazards:
            if self.player.rect.colliderect(hz.rect) and not self.player.is_invincible:
                self.player.hp -= 10
                self.player.invincible_for = 1.0

                if self.player.hp <= 0:
                    self.state = "gameover"

    def draw(self):

        screen.fill(GRAY)

        draw_hud(screen, self.player)
        draw_world(screen)

        # world
        for merch in self.merchs:
            merch.draw(screen)

        for hz in self.hazards:
            hz.draw(screen)

        self.player.draw(screen)

        # title screen
        if self.state == "title":
            t = FONT.render("Press SPACE to Start, Press Q to Quit", True, WHITE)
            r = t.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(t, r)

        if self.state == "gameover":
            t = FONT.render("Game Over - Press SPACE", True, WHITE)
            r = t.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(t, r)

        if self.state == "paused":
            draw_pause(screen)

        if self.state == "win":
            t = FONT.render("You Win! Press SPACE to Play Again, or Q to Quit", True, WHITE)
            r = t.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(t, r)
   
