from scene import *
import random
import math
import time

class CannonFruitShooter(Scene):
    def setup(self):
        self.initial_base_speed = 0.6
        self.cannon_speed = 5
        self.ball_speed = 10
        self.ball_radius = 5
        self.max_hearts_per_level = 2
        self.max_lives = 4
        self.starting_lives = 2

        self.fruit_types = [
            {"type": "grapes", "emoji": "🍇", "points": 40, "radius": 20, "is_heart": False, "is_special": False},
            {"type": "apple", "emoji": "🍎", "points": 30, "radius": 18, "is_heart": False, "is_special": False},
            {"type": "strawberry", "emoji": "🍓", "points": 20, "radius": 15, "is_heart": False, "is_special": False},
            {"type": "cherry", "emoji": "🍒", "points": 10, "radius": 12, "is_heart": False, "is_special": False},
            {"type": "heart", "emoji": "❤️", "points": 0, "radius": 15, "is_heart": True, "is_special": False},
            {"type": "mango", "emoji": "🥭", "points": 200, "radius": 40, "is_heart": False, "is_special": True}
        ]

        self.veggie_types = [
            {"type": "onion", "emoji": "🧅", "points": 40, "radius": 20, "is_heart": False, "is_special": False},
            {"type": "tomato", "emoji": "🍅", "points": 30, "radius": 18, "is_heart": False, "is_special": False},
            {"type": "potato", "emoji": "🥔", "points": 20, "radius": 15, "is_heart": False, "is_special": False},
            {"type": "cucumber", "emoji": "🥒", "points": 10, "radius": 12, "is_heart": False, "is_special": False},
            {"type": "heart", "emoji": "❤️", "points": 0, "radius": 15, "is_heart": True, "is_special": False},
            {"type": "carrot", "emoji": "🥕", "points": 200, "radius": 40, "is_heart": False, "is_special": True}
        ]

        self.reset_game()

    def reset_game(self):
        self.cannon = {'x': self.size.w / 2, 'y': self.size.h - 30, 'width': 40, 'height': 20, 'speed': self.cannon_speed}
        self.balls = []
        self.fruits = []
        self.score = 0
        self.fruits_missed = 0
        self.game_state = 'playing'
        self.last_spawn_time = time.time()
        self.base_fruit_speed = self.initial_base_speed
        self.speed_multiplier = 1.0
        self.level = 1
        self.hearts_spawned = 0
        self.special_spawned = False
        self.lives = self.starting_lives
        self.clouds = []
        self.init_clouds()
        self.touch_x = None

    def init_clouds(self):
        for i in range(5):
            self.clouds.append({
                'x': random.random() * self.size.w,
                'y': random.random() * (self.size.h - 100),
                'radius_x': 15 + random.random() * 25,
                'radius_y': 10 + random.random() * 15,
                'opacity': 0.5 + random.random() * 0.3
            })

    def spawn_fruit(self):
        current_level = math.floor(self.score / 1000) + 1
        available_types = [t for t in self.fruit_types if not t["is_heart"] and not t["is_special"]]
        if current_level >= 3:
            available_types = [t for t in self.veggie_types if not t["is_heart"] and not t["is_special"]]
        if self.hearts_spawned < self.max_hearts_per_level and random.random() < 0.05:
            available_types = [t for t in self.fruit_types if t["is_heart"]] if current_level < 3 else [t for t in self.veggie_types if t["is_heart"]]
        elif current_level >= 2 and not self.special_spawned and random.random() < 0.05:
            available_types = [t for t in self.fruit_types if t["is_special"]] if current_level < 3 else [t for t in self.veggie_types if t["is_special"]]
        fruit = random.choice(available_types)
        self.fruits.append({
            'x': random.random() * (self.size.w - 40) + 20,
            'y': 0,
            'type': fruit["type"],
            'emoji': fruit["emoji"],
            'points': fruit["points"],
            'radius': fruit["radius"],
            'speed': self.base_fruit_speed * self.speed_multiplier,
            'is_heart': fruit["is_heart"],
            'is_special': fruit["is_special"]
        })
        if fruit["is_heart"]:
            self.hearts_spawned += 1
        if fruit["is_special"]:
            self.special_spawned = True

    def draw_background(self):
        if self.level == 1:
            top_color = Color(0.9, 0.92, 0.94)
            bottom_color = Color(0.83, 0.85, 0.86)
        elif self.level == 2:
            top_color = Color(0.85, 0.9, 0.85)
            bottom_color = Color(0.8, 0.85, 0.8)
        elif self.level == 3:
            top_color = Color(0.85, 0.85, 0.9)
            bottom_color = Color(0.8, 0.8, 0.85)
        else:
            top_color = Color(0.88, 0.85, 0.9)
            bottom_color = Color(0.83, 0.8, 0.85)

        self.fill_color = top_color
        self.fill_rect(0, 0, self.size.w, self.size.h)

    def draw_clouds(self):
        for cloud in self.clouds:
            self.fill_color = Color(1, 1, 1, cloud["opacity"])
            self.draw_ellipse(cloud["x"] - cloud["radius_x"], cloud["y"] - cloud["radius_y"], cloud["radius_x"] * 2, cloud["radius_y"] * 2)

    def draw_cannon(self):
        self.fill_color = Color(0.33, 0.33, 0.33)
        self.fill_rect(self.cannon["x"] - self.cannon["width"] / 2, self.cannon["y"] - self.cannon["height"], self.cannon["width"], self.cannon["height"])
        self.fill_rect(self.cannon["x"] - 5, self.cannon["y"] - self.cannon["height"] - 20, 10, 20)

    def draw_balls(self):
        self.fill_color = Color(0, 0, 0)
        for ball in self.balls:
            self.fill_ellipse(ball["x"] - self.ball_radius, ball["y"] - self.ball_radius, self.ball_radius * 2, self.ball_radius * 2)

    def draw_fruits(self):
        for fruit in self.fruits:
            self.fill_color = Color(1, 0.84, 0, 1) if fruit["is_special"] else Color(0, 0, 0)
            self.draw_text(fruit["emoji"], fruit["x"] - fruit["radius"], fruit["y"] - fruit["radius"], font_size=fruit["radius"] * 2)

    def draw_paused(self):
        self.fill_color = Color(0, 0, 0)
        self.draw_text(f"Level {self.level}", self.size.w / 2, self.size.h / 2 - 20, font_size=24, alignment='center')
        self.draw_text("Tap to Continue", self.size.w / 2, self.size.h / 2 + 10, font_size=16, alignment='center')

    def draw_game_over(self):
        self.fill_color = Color(0, 0, 0)
        self.draw_text("Game Over", self.size.w / 2, self.size.h / 2 - 50, font_size=40, alignment='center')
        self.draw_text(f"Level: {self.level}", self.size.w / 2, self.size.h / 2 - 10, font_size=30, alignment='center')
        self.draw_text(f"Final Score: {self.score}", self.size.w / 2, self.size.h / 2 + 30, font_size=30, alignment='center')

    def update(self):
        current_level = math.floor(self.score / 1000) + 1
        if current_level > self.level and self.game_state == 'playing':
            self.level = current_level
            if self.lives < self.max_lives:
                self.lives += 1
            self.game_state = 'paused'
            if self.level == 2:
                self.base_fruit_speed = self.initial_base_speed * 1.2
            elif self.level >= 3:
                self.base_fruit_speed *= 1.1
            self.hearts_spawned = 0
            self.special_spawned = False

        if self.game_state != 'playing':
            return

        self.speed_multiplier = 1.0 + math.floor(self.score / 100) * 0.1

        for ball in self.balls[:]:
            ball['y'] -= ball['speed']
            if ball['y'] < 0:
                self.balls.remove(ball)

        for fruit in self.fruits[:]:
            fruit['y'] += fruit['speed']
            if fruit['y'] + fruit['radius'] >= self.size.h:
                if not fruit['is_heart']:
                    self.lives -= 1
                    if self.lives <= 0:
                        self.game_state = 'over'
                self.fruits.remove(fruit)

        for ball in self.balls:
            for fruit in self.fruits[:]:
                dx = ball['x'] - fruit['x']
                dy = ball['y'] - fruit['y']
                distance = math.sqrt(dx * dx + dy * dy)
                if distance < self.ball_radius + fruit['radius']:
                    if fruit['is_heart']:
                        self.lives = min(self.max_lives, self.lives + 1)
                    else:
                        self.score += fruit['points']
                    self.fruits.remove(fruit)

        current_time = time.time()
        if current_time - self.last_spawn_time > random.uniform(1, 2):
            self.spawn_fruit()
            self.last_spawn_time = current_time

    def draw(self):
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

    def touch_began(self, touch):
        if self.game_state == 'paused':
            self.game_state = 'playing'
        elif self.game_state == 'playing':
            self.balls.append({'x': self.cannon["x"], 'y': self.cannon["y"] - self.cannon["height"] - 20, 'speed': self.ball_speed})

    def touch_moved(self, touch):
        if touch.location.y > self.size.h - 100:
            new_x = touch.location.x
            if new_x < self.cannon["width"] / 2:
                new_x = self.cannon["width"] / 2
            if new_x > self.size.w - self.cannon["width"] / 2:
                new_x = self.size.w - self.cannon["width"] / 2
            self.cannon["x"] = new_x

run(CannonFruitShooter)