class GameStats:
    def __init__(self, ai_game):
        self.settings = ai_game.settings
        self.reset_stats()
        self.high_score = self.load_high_score()
        self.level=1

    def reset_stats(self):
        self.ships_left = self.settings.ship_limit
        self.score=0

    def load_high_score(self):
        filename = 'high_score.txt'
        try:
            with open(filename) as f:
                content = f.read()
                return int(content)
        except FileNotFoundError:
            return 0
        except ValueError:
            return 0

    def save_high_score(self):
        filename = 'high_score.txt'
        with open(filename, 'w') as f:
            f.write(str(self.high_score))