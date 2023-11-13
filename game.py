import pygame
import sys

from AshipthatfiresBullets.gameStats import GameStats
from alien import Alien
from pygame.sprite import Group

from settings import Settings
from ship import Ship
import game_functions as gf


def run_game():
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Allien invasion")
    ship = Ship(ai_settings, screen)
    alien = Alien(ai_settings, screen)
    aliens = Group()
    bullets = Group()
    gf.create_fleet(ai_settings, screen,ship, aliens)
    stats = GameStats(ai_settings)
    while True:
        gf.check_event(ai_settings, screen, ship, bullets)
        bullets.update()
        alien.blitme()
        ship.blitme()
        screen.fill(ai_settings.bg_color)
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, ship, aliens, bullets)
            gf.update_aliens(ai_settings, stats, screen, ship, aliens, bullets)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


run_game()
