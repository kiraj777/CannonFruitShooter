import pygame
import math
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 926
SCREEN_HEIGHT = 428

# Colors
BLACK = (0, 0, 0)
GRAY = (85, 85, 85)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)

# Fonts
font = pygame.font.SysFont('arial', 20)
large_font = pygame.font.SysFont('arial', 40)
medium_font = pygame.font.SysFont('arial', 30)
small_font = pygame.font.SysFont('arial', 16)

# Game constants
INITIAL_BASE_SPEED = 0.6
CANNON_SPEED = 5
BALL_SPEED = 10
BALL_RADIUS = 5
MAX_HEARTS_PER_LEVEL = 2
MAX_LIVES = 4
STARTING_LIVES = 2

fruit_types = [
    {"type": "grapes", "emoji": "🍇", "points": 40, "radius": 20, "is_heart": False, "is_special": False},
    {"type": "apple", "emoji": "🍎", "points": 30, "radius": 18, "is_heart": False, "is_special": False},
    {"type": "strawberry", "emoji": "🍓", "points": 20, "radius": 15, "is_heart": False, "is_special": False},
    {"type": "cherry", "emoji": "🍒", "points": 10, "radius": 12, "is_heart": False, "is_special": False},
    {"type": "heart", "emoji": "❤️", "points": 0, "radius": 15, "is_heart": True, "is_special": False},
    {"type": "mango", "emoji": "🥭", "points": 200, "radius": 40, "is_heart": False, "is_special": True}
]

veggie_types = [
    {"type": "onion", "emoji": "🧅", "points": 40, "radius": 20, "is_heart": False, "is_special": False},
    {"type": "tomato", "emoji": "🍅", "points": 30, "radius": 18, "is_heart": False, "is_special": False},
    {"type": "potato", "emoji": "🥔", "points": 20, "radius": 15, "is_heart": False, "is_special": False},
    {"type": "cucumber", "emoji": "🥒", "points": 10, "radius": 12, "is_heart": False, "is_special": False},
    {"type": "heart", "emoji": "❤️", "points": 0, "radius": 15, "is_heart": True, "is_special": False},
    {"type": "carrot", "emoji": "🥕", "points": 200, "radius": 40, "is_heart": False, "is_special": True}
]

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Cannon Fruit Shooter')
        self.clock = pygame.time.Clock()
        self.keys = {}
        self.reset_game()

    def reset_game(self):
        self.cannon = {"x": SCREEN_WIDTH / 2, "y": SCREEN_HEIGHT - 30, "width": 40, "height": 20, "speed": 5}
        self.balls = []
        self.fruits = []
        self.score = 0
        self.fruits_missed = 0
        self.game_state = 'playing'
        self.last_spawn_time = time.time()
        self.base_fruit_speed = INITIAL_BASE_SPEED
        self.speed_multiplier = 1.0
        self.level = 1
        self.hearts_spawned = 0
        self.special_spawned = False
        self.lives = STARTING_LIVES
        self.clouds = []
        self.init_clouds()

    def init_clouds(self):
        for i in range(5):
            self.clouds.append({
                "x": random.random() * SCREEN_WIDTH,
                "y": random.random() * (SCREEN_HEIGHT - 100),
                "radius_x": 15 + random.random() * 25,
                "radius_y": 10 + random.random() * 15,
                "opacity": 0.5 + random.random() * 0.3
            })

    def spawn_fruit(self):
        current_level = math.floor(self.score / 1000) + 1
        available_types = [t for t in fruit_types if not t["is_heart"] and not t["is_special"]]
        if current_level >= 3:
            available_types = [t for t in veggie_types if not t["is_heart"] and not t["is_special"]]
        if self.hearts_spawned < MAX_HEARTS_PER_LEVEL and random.random() < 0.05:
            available_types = [t for t in fruit_types if t["is_heart"]] if current_level < 3 else [t for t in veggie_types if t["is_heart"]]
        elif current_level >= 2 and not self.special_spawned and random.random() < 0.05:
            available_types = [t for t in fruit_types if t["is_special"]] if current_level < 3 else [t for t in veggie_types if t["is_special"]]
        fruit = random.choice(available_types)
        self.fruits.append({
            "x": random.random() * (SCREEN_WIDTH - 40) + 20,
            "y": 0,
            "type": fruit["type"],
            "emoji": fruit["emoji"],
            "points": fruit["points"],
            "radius": fruit["radius"],
            "speed": self.base_fruit_speed * self.speed_multiplier,
            "is_heart": fruit["is_heart"],
            "is_special": fruit["is_special"]
        })
        if fruit["is_heart"]:
            self.hearts_spawned += 1
        if fruit["is_special"]:
            self.special_spawned = True

    def get_gradient(self):
        if self.level == 1:
            return (210, 10, 90), (210, 5, 85)
        elif self.level == 2:
            return (150, 10, 85), (150, 5, 80)
        elif self.level == 3:
            return (270, 10, 85), (270, 5, 80)
        else:
            return (300, 10, 85), (300, 5, 80)

    def draw_background(self):
        (top_h, top_s, top_l), (bottom_h, bottom_s, bottom_l) = self.get_gradient()
        top_color = self.hsl_to_rgb(top_h / 360, top_s / 100, top_l / 100)
        bottom_color = self.hsl_to_rgb(bottom_h / 360, bottom_s / 100, bottom_l / 100)
        for i in range(SCREEN_HEIGHT):
            color = [
                int(top_color[0] + (bottom_color[0] - top_color[0]) * i / SCREEN_HEIGHT),
                int(top_color[1] + (bottom_color[1] - top_color[1]) * i / SCREEN_HEIGHT),
                int(top_color[2] + (bottom_color[2] - top_color[2]) * i / SCREEN_HEIGHT)
            ]
            pygame.draw.line(self.screen, color, (0, i), (SCREEN_WIDTH, i))

    def hsl_to_rgb(self, h, s, l):
        if s == 0:
            r = g = b = l
        else:
            q = l * (1 + s) if l < 0.5 else l + s - l * s
            p = 2 * l - q
            r = self.hue_to_rgb(p, q, h + 1/3)
            g = self.hue_to_rgb(p, q, h)
            b = self.hue_to_rgb(p, q, h - 1/3)
        return (int(r * 255), int(g * 255), int(b * 255))

    def hue_to_rgb(self, p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1/6:
            return p + (q - p) * 6 * t
        if t < 1/2:
            return q
        if t < 2/3:
            return p + (q - p) * (2/3 - t) * 6
        return p

    def draw_clouds(self):
        for cloud in self.clouds:
            pygame.draw.ellipse(self.screen, (255, 255, 255, int(cloud["opacity"] * 255)), (cloud["x"] - cloud["radius_x"], cloud["y"] - cloud["radius_y"], cloud["radius_x"] * 2, cloud["radius_y"] * 2))

    def draw_cannon(self):
        pygame.draw.rect(self.screen, GRAY, (self.cannon["x"] - self.cannon["width"] / 2, self.cannon["y"] - self.cannon["height"], self.cannon["width"], self.cannon["height"]))
        pygame.draw.rect(self.screen, GRAY, (self.cannon["x"] - 5, self.cannon["y"] - self.cannon["height"] - 20, 10, 20))

    def draw_balls(self):
        for ball in self.balls:
            pygame.draw.circle(self.screen, BLACK, (int(ball["x"]), int(ball["y"])), BALL_RADIUS)

    def draw_fruits(self):
        for fruit in self.fruits:
            color = GOLD if fruit["is_special"] else BLACK
            text = font.render(fruit["emoji"], True, color)
            self.screen.blit(text, (fruit["x"] - fruit["radius"], fruit["y"] - fruit["radius"]))

    def draw_paused(self):
        text = large_font.render(f"Level {self.level}", True, BLACK)
        self.screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - text.get_height() / 2))
        text = small_font.render("Press any key to continue", True, BLACK)
        self.screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 + 20))

    def draw_game_over(self):
        text = large_font.render("Game Over", True, BLACK)
        self.screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - 60))
        text = medium_font.render(f"Level: {self.level}", True, BLACK)
        self.screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 - 20))
        text = medium_font.render(f"Final Score: {self.score}", True, BLACK)
        self.screen.blit(text, (SCREEN_WIDTH / 2 - text.get_width() / 2, SCREEN_HEIGHT / 2 + 20))

    def update_status(self):
        text = small_font.render(f"Level: {self.level} | Score: {self.score} | Lives: {self.lives}", True, BLACK)
        self.screen.blit(text, (10, 10))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    self.keys[event.key] = True
                    if self.game_state == 'paused':
                        self.game_state = 'playing'
                    if event.key == pygame.K_SPACE and self.game_state == 'playing':
                        self.balls.append({"x": self.cannon["x"], "y": self.cannon["y"] - self.cannon["height"] - 20, "speed": BALL_SPEED})
                elif event.type == pygame.KEYUP:
                    self.keys[event.key] = False

            if self.game_state == 'playing':
                self.speed_multiplier = 1.0 + math.floor(self.score / 100) * 0.1

                if self.keys.get(pygame.K_LEFT, False) and self.cannon["x"] > self.cannon["width"] / 2:
                    self.cannon["x"] -= self.cannon["speed"]
                if self.keys.get(pygame.K_RIGHT, False) and self.cannon["x"] < SCREEN_WIDTH - self.cannon["width"] / 2:
                    self.cannon["x"] += self.cannon["speed"]

                for ball in self.balls[:]:
                    ball["y"] -= ball["speed"]
                    if ball["y"] < 0:
                        self.balls.remove(ball)

                for fruit in self.fruits[:]:
                    fruit["y"] += fruit["speed"]
                    if fruit["y"] + fruit["radius"] >= SCREEN_HEIGHT:
                        if not fruit["is_heart"]:
                            self.lives -= 1
                            if self.lives <= 0:
                                self.game_state = 'over'
                                self.stop_audio()
                        self.fruits.remove(fruit)

                for ball in self.balls:
                    for fruit in self.fruits[:]:
                        dx = ball["x"] - fruit["x"]
                        dy = ball["y"] - fruit["y"]
                        distance = math.sqrt(dx * dx + dy * dy)
                        if distance < BALL_RADIUS + fruit["radius"]:
                            if fruit["is_heart"]:
                                self.lives = min(MAX_LIVES, self.lives + 1)
                            else:
                                self.score += fruit["points"]
                            self.fruits.remove(fruit)
                            self.update_status()

                current_time = time.time()
                if current_time - self.last_spawn_time > random.uniform(1, 2) and self.game_state == 'playing':
                    self.spawn_fruit()
                    self.last_spawn_time = current_time

                current_level = math.floor(self.score / 1000) + 1
                if current_level > self.level and self.game_state == 'playing':
                    self.level = current_level
                    if self.lives < MAX_LIVES:
                        self.lives += 1
                    self.game_state = 'paused'
                    if self.level == 2:
                        self.base_fruit_speed = INITIAL_BASE_SPEED * 1.2
                    elif self.level >= 3:
                        self.base_fruit_speed *= 1.1
                    self.hearts_spawned = 0
                    self.special_spawned = False
                    self.update_status()

            self.draw_background()
            self.draw_clouds()
            if self.game_state == 'playing' or self.game_state == 'paused':
                self.draw_cannon()
                self.draw_balls()
                self.draw_fruits()
            if self.game_state == 'paused':
                self.draw_paused()
            if self.game_state == 'over':
                self.draw_game_over()
            self.update_status()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()