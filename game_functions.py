import sys
import pygame
from pygame.time import get_ticks
from time import sleep

from alien import Alien
from AshipthatfiresBullets.bullet import Bullet


# code given from the book but
# def check_event(ship):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()
#         elif event.type == pygame.KEYDOWN:
#             check_keydown_events(event, ship)
#
#         elif event.type == pygame.KEYUP:
#             check_keyup_events(event, ship)


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
        print('right')
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
        print("left")
    # elif event.key == pygame.K_SPACE:
    #     new_bullet = Bullet(ai_settings,screen,ship)
    #     bullets.add(new_bullet)


def check_event(ai_settings, screen, ship, bullets):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        ship.moving_right = True
        print('right')
    else:
        ship.moving_right = False

    if keys[pygame.K_LEFT]:
        ship.moving_left = True
        print('left')
    else:
        ship.moving_left = False

    cooldown = ai_settings.bullet_cooldown
    now = get_ticks()
    # print(str(cooldown)+" the now "+str(now))
    if keys[pygame.K_SPACE] and (now - ai_settings.bullet_last >= cooldown):
        if len(bullets) < 3.0:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)
            ai_settings.bullet_last = now
            print("shoot")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings, screen, ship, aliens, bullets):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()

    aliens.draw(screen)
    pygame.display.flip()


def create_fleet(ai_settings, screen, ship, aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    available_space_x = (ai_settings.screen_width - 2 * alien_width)
    number_of_aliens_x = get_number_aliens(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    for row in range(number_rows):
        for alien_number in range(number_of_aliens_x):
            create_aliens(ai_settings, screen, aliens, alien_number, row)
            # create_aliens(ai_settings, screen, aliens, alien_width)
            alien = Alien(ai_settings, screen)
            alien.x = (alien_width + 2 * alien_width * alien_number)
            alien.rect.x = alien.x
            aliens.add(alien)


def update_aliens(ai_settings,stats, screen, ship, alien, bullets):
    alien.update()
    check_fleet_edges(ai_settings, alien)
    if pygame.sprite.spritecollideany(ship, alien):
        ship_hit(ai_settings, stats, screen, ship, alien, bullets)
        print("ship hit")
    check_aliens_bottom(ai_settings, stats, screen, ship, alien, bullets)


def get_number_aliens(ai_settings, alien_width):
    available_space_x = (ai_settings.screen_width - 2 * alien_width)
    number_of_aliens_x = int(available_space_x / (2 * alien_width))
    return number_of_aliens_x


def create_aliens(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = (alien_width + 2 * alien_width * alien_number)
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_of_rows = int(available_space_y / (2 * alien_height))
    return number_of_rows


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def update_bullets(ai_settings, screen, ship, aliens, bullets):
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # print(len(bullets))
    check_bullet_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_collisions(ai_settings, screen, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(aliens, bullets, True, True)
    if len(aliens) == 0:
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)


def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    if stats.ship_left > 0:
        stats.ship_left = -1
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings,screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
    print(stats.game_active)


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


