import pygame.time


class Settings():

    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 750
        self.bg_color = (0, 0, 200)

        self.ship_speed_factor = 1.5
        self.ship_limit = 3

        self.bullet_speed_factor = 2
        self.bullet_width = 300
        self.bullet_height = 15
        self.bullet_color = 230, 230, 230

        self.bullet_cooldown = 250
        self.bullet_last = pygame.time.get_ticks()
        self.bullet_allowed = 3

        self.alien_speed_factor = 2
        self.fleet_drop_speed = 10
        self.fleet_direction = 1


