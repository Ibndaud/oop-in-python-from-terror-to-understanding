import pgzrun
from random import randint, uniform
import math


# ------------------------------------------------------------
# Константы (настройки игры)
# ------------------------------------------------------------
TITLE = "Тык-тык"

BACKGROUND_COLOR = (20, 30, 40)
TEXT_COLOR = (220, 220, 220)
SECONDARY_TEXT_COLOR = (200, 200, 200)
HINT_TEXT_COLOR = (180, 180, 200)
HELP_TEXT_COLOR = (160, 160, 180)

WIDTH, HEIGHT = 1200, 768


class Circle:
    def __init__(self):
        self.radius = 5
        self.color = (132, 255, 24)
        self.x = 100
        self.y = 150
        self.dx = 2.0
        self.dy = 1.5
        self.is_popping = False
        self.pop_progress = 0.0
        self.pop_speed = 0.2
        
    def move(self, multiplier):
        if self.is_popping:
            return
        self.x += self.dx * multiplier
        self.y += self.dy * multiplier
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.x = min(max(self.x, self.radius), WIDTH - self.radius)
            self.dx = -self.dx
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.y = min(max(self.y, self.radius), HEIGHT - self.radius)
            self.dy = -self.dy
                
    def update(self):
        if self.is_popping:
            self.pop_progress += self.pop_speed
            return True if self.pop_progress >= 1 else False
        return False
    
    def is_clicked(self, pos):
        _x, _y = pos
        return (pow(_x - self.x, 2) + pow(_y - self.y, 2)) ** 0.5 <= self.radius
    
    # def draw(self):
    #     return f'Circle: ({self.x}, {self.y}), r={self.radius}, color={self.color}'
    def draw(self):
        if not self.is_popping:
            screen.draw.filled_circle((self.x, self.y), self.radius, self.color)
            screen.draw.circle((self.x, self.y), self.radius, (255, 255, 255))
            return

        current_radius = int(self.radius * (1 - self.pop_progress))
        if current_radius < 1:
            current_radius = 1

        screen.draw.filled_circle((self.x, self.y), current_radius, self.color)


class Game:
    _CIRCLE_NUMBER = 5
    
    def __init__(self):
        self.setup_game()
        
    def setup_game(self):
        self.circles = [self.spawn_circle() for _ in range(self._CIRCLE_NUMBER)]
        self.score = 0
        self.speed_multiplier = 1.0
        
    def spawn_circle(self):
        return Circle()
    
    def handle_click(self, pos):
        for circle in self.circles:
            if circle.is_clicked(pos):
                circle.is_popping = True
                self.score += 1
                self.speed_multiplier = 1 + self.score * 0.1
                break
                
    def update(self):
        self.circles = [circle if not circle.update() else self.spawn_circle() for circle in self.circles]
        for circle in self.circles:
            circle.move(self.speed_multiplier)
            
    # def draw(self):
    #     return self.score, [circle.draw() for circle in self.circles]
    def draw(self):
        screen.fill(BACKGROUND_COLOR)

        for circle in self.circles:
            circle.draw()

        screen.draw.text(
            f"Счет: {self.score}",
            topleft=(20, 20),
            fontsize=30,
            color=TEXT_COLOR,
        )

        screen.draw.text(
            f"Скорость: x{self.speed_multiplier:.1f}",
            topright=(WIDTH - 20, 20),
            fontsize=30,
            color=SECONDARY_TEXT_COLOR,
        )

        screen.draw.text(
            "Нажимай левой кнопкой мыши на шарики, чтобы лопать их",
            center=(WIDTH // 2, HEIGHT - 40),
            fontsize=24,
            color=HINT_TEXT_COLOR,
        )

        screen.draw.text(
            "R - новая игра | ESC - выход",
            center=(WIDTH // 2, HEIGHT - 15),
            fontsize=20,
            color=HELP_TEXT_COLOR,
        )
    

# ------------------------------------------------------------
# Pygame Zero hooks (функции, которые вызывает движок)
# ------------------------------------------------------------
game = Game()


def update():
    """Pygame Zero вызывает эту функцию каждый кадр."""
    game.update()


def draw():
    """Pygame Zero вызывает эту функцию для отрисовки кадра."""
    game.draw()


def on_mouse_down(pos, button):
    """
    Pygame Zero вызывает эту функцию при клике мышью.

    pos — координаты клика (x, y)
    button — кнопка мыши
    """
    if button == mouse.LEFT:
        game.handle_click(pos)


def on_key_down(key):
    """
    Pygame Zero вызывает эту функцию при нажатии клавиши.

    R — перезапуск
    ESC — выход из игры
    """
    if key == keys.R:
        game.setup_game()
    elif key == keys.ESCAPE:
        exit()


pgzrun.go()