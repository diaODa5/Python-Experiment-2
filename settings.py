class Settings():
    def __init__(self):
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        self.fleet_direction = 1
        self.ship_limit = 3

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.powerup_spawn_time = 10000
        self.powerup_timer = 0
        self.is_powerup_active = False

        self.invulnerable_time = 3000
        self.invulnerable_timer = 0

        self.diamond_time = 3000
        self.diamond_timer = 0
        self.is_diamond_active = False

        self.original_bullet_width = 3
        self.powerup_bullet_width = 10

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed = 1.5
        self.bullet_speed = 2.5
        self.alien_speed = 1.0
        self.fleet_direction = 1
        self.alien_points = 50

    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)