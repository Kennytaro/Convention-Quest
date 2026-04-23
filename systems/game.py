import random
import pygame

from settings import WIDTH, HEIGHT, WHITE, GRAY, FONT, screen
from entities.player import Player
from entities.enemy import spawn_hazards
from entities.merch import spawn_merchs
from systems.world import draw_world, draw_pause
from systems.hud import draw_hud
from systems.levels import get_level
from entities.booths import get_booth_rects
from systems.audio import AudioBank

bg_img = pygame.image.load("assets/bgfloor.png").convert()
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

class SparkleParticle:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-120, 120)
        self.vy = random.uniform(-120, 120)
        self.life = random.uniform(0.3, 0.6)
        self.size = random.randint(2, 4)

    def update(self, dt):
        self.life -= dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= 0.92
        self.vy *= 0.92

    def draw(self, screen):
        if self.life <= 0:
            return

        points = [
            (self.x, self.y - self.size),
            (self.x + self.size, self.y),
            (self.x, self.y + self.size),
            (self.x - self.size, self.y),
        ]
        pygame.draw.polygon(screen, WHITE, points)

def draw_text_with_outline(screen, text, font, color, outline_color, center):
    base = font.render(text, True, color)
    outline = font.render(text, True, outline_color)

    r = base.get_rect(center=center)

    # 8-direction outline (better than 4)
    for dx in [-2, 0, 2]:
        for dy in [-2, 0, 2]:
            if dx != 0 or dy != 0:
                screen.blit(outline, (r.x + dx, r.y + dy))

    screen.blit(base, r)

class Game:
    fps = 60

    def __init__(self):
        self.player = Player(WIDTH // 2, HEIGHT // 2)

        self.merchs = []
        self.hazards = []
        self.sparkles = []

        self.level = 0
        self.level_data = get_level(self.level)

        self.audio = AudioBank()
        self.music_started = False
        self.audio_enabled = True

        self.state = "title"
        self.show_particles = True
        self.show_flashing = True
        self.spawn_level()

    def spawn_level(self):
        self.merchs.clear()
        self.hazards.clear()
        self.sparkles.clear()

        self.player.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.player.score = 0

        self.level_data = get_level(self.level)
        self.booths = get_booth_rects(self.level)

        self.merchs = spawn_merchs(
            player_rect=self.player.rect,
            count=self.level_data["merch_count"],
            level=self.level
        )
        self.hazards = spawn_hazards(
            self.merchs,
            player_rect=self.player.rect,
            count=self.level_data["hazard_count"],
            speed=self.level_data["hazard_speed"],
            booths=self.booths
        )

    def spawn_sparkles(self, x, y, amount=10):
        for _ in range(amount):
            self.sparkles.append(SparkleParticle(x, y))

    def update(self, dt):
        if self.state != "play":
            return

        self.player.update(dt, self.booths)

        for hz in self.hazards:
            hz.update(dt, self.hazards, self.booths)

        if self.show_particles:
            for sparkle in self.sparkles[:]:
                sparkle.update(dt)
                if sparkle.life <= 0:
                    self.sparkles.remove(sparkle)
            

        # Merch collection
        for merch in self.merchs[:]:
            if self.player.rect.colliderect(merch.rect):
                self.merchs.remove(merch)
                self.player.score += 1
                self.audio.play("ui_confirm")
                
                if self.show_particles:
                    self.spawn_sparkles(merch.rect.centerx, merch.rect.centery, 12)

                if self.player.score >= self.level_data["merch_count"]:
                    self.level += 1
                    if self.level > 1:
                        self.state = "win"
                        pygame.mixer.music.stop()
                    else:
                        self.spawn_level()

        # Hazard damage + i-frame
        for hz in self.hazards:
            if self.player.rect.colliderect(hz.rect) and not self.player.is_invincible:
                self.player.hp -= 10
                self.player.invincible_for = 1.0
                self.audio.play("hurt")

                if self.player.hp <= 0:
                    self.state = "gameover"
                    pygame.mixer.music.stop()

    def draw(self):
        screen.blit(bg_img, (0, 0))

        draw_hud(screen, self.player)
        draw_world(screen, self.level)

        for merch in self.merchs:
            merch.draw(screen)

        for hz in self.hazards:
            hz.draw(screen)

        if self.show_particles:
            for sparkle in self.sparkles:
                sparkle.draw(screen)

        self.player.draw(screen, self.show_flashing)

        if self.state == "title":
            draw_text_with_outline(
                screen,
                "Press SPACE to Start, Press Q to Quit",
                FONT,
                WHITE,
                (0, 0, 0),
                (WIDTH // 2, HEIGHT // 2)
            )

        if self.state == "gameover":
            draw_text_with_outline(
                screen,
                "Game Over - Press SPACE to restart",
                FONT,
                WHITE,
                (0, 0, 0),
                (WIDTH // 2, HEIGHT // 2)
            )

        if self.state == "paused":
            draw_pause(screen)

        if self.state == "win":
            draw_text_with_outline(
                screen,
                "You Win, Press Q to Quit or SPACE to restart",
                FONT,
                WHITE,
                (0, 0, 0),
                (WIDTH // 2, HEIGHT // 2)
            )
    def toggle_audio(self):
        self.audio_enabled = not self.audio_enabled

        # mute/unmute SFX system
        self.audio.set_mute(not self.audio_enabled)

        # control music system
        if self.audio_enabled:
            pygame.mixer.music.set_volume(0.4)
        else:
            pygame.mixer.music.set_volume(0)
