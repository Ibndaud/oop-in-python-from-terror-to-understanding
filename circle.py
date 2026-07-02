import math
from random import randint, uniform


class Circle:
    def __init__(self, width: int, height: int, min_speed: float, max_speed: float):
        self.width = width
        self.height = height
        self.min_speed = min_speed
        self.max_speed = max_speed

        # Генерация параметров круга
        self.radius = randint(15, 35)
        self.color = (randint(100, 255), randint(100, 255), randint(100, 255))
        self.x = randint(self.radius, self.width - self.radius)
        self.y = randint(self.radius, self.height - self.radius)

        # Случайное направление и скорость
        angle = uniform(0, 2 * math.pi)
        speed = uniform(self.min_speed, self.max_speed)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed

        # Анимация лопания
        self.is_popping = False
        self.pop_progress = 0.0
        self.pop_speed = 0.2        

    def move(self, multiplier: float):
        if self.is_popping:
            return
        self.x += self.dx * multiplier
        self.y += self.dy * multiplier

        # Отражение от стен
        if self.x - self.radius < 0 or self.x + self.radius > self.width:
            self.x = min(max(self.x, self.radius), self.width - self.radius)
            self.dx = -self.dx
        if self.y - self.radius < 0 or self.y + self.radius > self.height:
            self.y = min(max(self.y, self.radius), self.height - self.radius)
            self.dy = -self.dy           

    def update(self) -> bool:
        if self.is_popping:
            self.pop_progress += self.pop_speed
            return self.pop_progress >= 1.0
        return False

    def is_clicked(self, pos: tuple) -> bool:
        _x, _y = pos
        # УЛУЧШЕНИЕ: math.hypot - стандартный способ вычисления расстояния
        return math.hypot(_x - self.x, _y - self.y) <= self.radius
        # return pow(_x - self.x, 2) + pow(_y - self.y, 2) <= self.radius ** 2

    def draw(self, screen):
        if not self.is_popping:
            screen.draw.filled_circle((self.x, self.y), self.radius, self.color)
            screen.draw.circle((self.x, self.y), self.radius, (255, 255, 255))
            return

        # Анимация: круг сжимается до точки
        current_radius = int(self.radius * (1 - self.pop_progress))
        if current_radius < 1:
            current_radius = 1
        screen.draw.filled_circle((self.x, self.y), current_radius, self.color)
