from settings import WIDTH, HEIGHT, WHITE, GRAY, FONT, screen
from entities.player import Player
from entities.enemy import spawn_hazards
from entities.merch import spawn_merchs
from systems.world import draw_world, draw_pause
from systems.hud import draw_hud
from systems.levels import get_level
from entities.booths import get_booth_rects
from systems.audio import AudioBank


class Game:
    fps = 60

    def __init__(self):

        self.player = Player(WIDTH//2,HEIGHT//2)

        self.merchs = []
        self.hazards = []

        self.level = 0
        self.level_data = get_level(self.level)

        self.audio = AudioBank()

        self.state = "title"

        self.spawn_level()


    def spawn_level(self):

        self.merchs.clear()
        self.hazards.clear()

        self.player.rect.center = (WIDTH//2, HEIGHT//2)
        self.player.score = 0  # reset score each level

        self.level_data = get_level(self.level)
        self.booths = get_booth_rects(self.level)

        self.merchs = spawn_merchs(player_rect = self.player.rect, count = self.level_data["merch_count"], level = self.level)
        self.hazards = spawn_hazards(self.merchs, player_rect=self.player.rect, count = self.level_data["hazard_count"],  speed = self.level_data["hazard_speed"], booths = self.booths)
    
    def update(self, dt):

        if self.state not in ("play",):
            return

        self.player.update(dt, self.booths)

        for hz in self.hazards:
            hz.update(dt, self.hazards, self.booths)

        #Merch collection
        for merch in self.merchs[:]:
            if self.player.rect.colliderect(merch.rect):
                self.merchs.remove(merch)
                self.player.score += 1
                self.audio.play("ui_confirm")

                if self.player.score >= self.level_data["merch_count"]:
                    self.level += 1
                        # STOP AFTER LEVEL 2 (index 1)
                    if self.level > 1:
                        self.state = "win"
                    else:
                        self.spawn_level()

        #Hazard damage + i-frame
        for hz in self.hazards:
            if self.player.rect.colliderect(hz.rect) and not self.player.is_invincible:
                self.player.hp -= 10
                self.player.invincible_for = 1.0
                self.audio.play("hurt")

                if self.player.hp <= 0:
                    self.state = "gameover"

    def draw(self):

        screen.fill(GRAY)

        draw_hud(screen, self.player)
        draw_world(screen, self.level)

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
            t = FONT.render("You Win", True, WHITE)
            r = t.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(t, r)
   
