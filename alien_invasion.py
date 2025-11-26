import sys
from time import sleep
import pygame
import random
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from powerup import Diamond, Shield


class AlienInvasion:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_width()
        self.settings.screen_height = self.screen.get_height()
        pygame.display.set_caption("Alien Invasion")
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self._create_fleet()
        self.game_active = False
        self.play_button = Button(self, "Play")

    def run_game(self):
        while True:
            self._check_events()

            dt = self.clock.tick(60)
            self._manage_powerups(dt)

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                self._check_powerup_collision()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.ship.blitme()
        self.aliens.draw(self.screen)

        self.powerups.draw(self.screen)

        self.sb.show_score()
        if not self.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_q:
            self.stats.save_high_score()
            sys.exit()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        self._check_bullet_alien_collisions()

    def _manage_powerups(self, dt):

        if not self.settings.is_powerup_active:
            self.settings.powerup_timer += dt
            if self.settings.powerup_timer >= self.settings.powerup_spawn_time:
                self._spawn_powerup()
                self.settings.powerup_timer = 0

        if self.ship.is_invulnerable:
            self.settings.invulnerable_timer += dt
            if self.settings.invulnerable_timer >= self.settings.invulnerable_time:
                self._deactivate_shield()

        if self.settings.is_diamond_active:
            self.settings.diamond_timer += dt
            if self.settings.diamond_timer >= self.settings.diamond_time:
                self._deactivate_diamond()

    def _spawn_powerup(self):
        if not self.powerups:
            powerup_type = random.choice(['diamond', 'shield'])

            if powerup_type == 'diamond':
                new_powerup = Diamond(self)
            else:
                new_powerup = Shield(self)

            self.powerups.add(new_powerup)
            self.settings.is_powerup_active = True

    def _check_powerup_collision(self):
        collisions = pygame.sprite.spritecollide(self.ship, self.powerups, True)
        if collisions:
            self.settings.is_powerup_active = False
            powerup = collisions[0]

            if powerup.type == 'diamond':
                self._activate_diamond()
            elif powerup.type == 'shield':
                self._activate_shield()

    def _activate_diamond(self):
        self.settings.bullet_width = self.settings.powerup_bullet_width
        self.settings.is_diamond_active = True
        self.settings.diamond_timer = 0

    def _deactivate_diamond(self):
        self.settings.bullet_width = self.settings.original_bullet_width
        self.settings.is_diamond_active = False
        self.settings.diamond_timer = 0

    def _activate_shield(self):
        self.ship.is_invulnerable = True
        self.settings.invulnerable_timer = 0

    def _deactivate_shield(self):
        self.ship.is_invulnerable = False
        self.settings.invulnerable_timer = 0

    def _create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        current_x, current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x, current_y)
                current_x += 2 * alien_width
            current_x = alien_width
            current_y += 2 * alien_height

    def _create_alien(self, x_position, y_position):
        new_alien = Alien(self)
        new_alien.x = x_position
        new_alien.rect.x = x_position
        new_alien.rect.y = y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        self._check_fleet_edges()
        self.aliens.update()
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_bullet_alien_collisions(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()
            self.stats.level += 1
            self.sb.prep_level()

    def _ship_hit(self):
        if self.ship.is_invulnerable:
            self.settings.invulnerable_timer = 0
            return

        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            self.sb.prep_ships()
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()

            self._deactivate_shield()
            self._deactivate_diamond()

            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                self._ship_hit()
                break

    def _check_play_button(self, mouse_pos):
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            self.stats.reset_stats()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()
            self.game_active = True
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            pygame.mouse.set_visible(False)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()