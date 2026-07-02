import math
from random import randint
from circle import Circle


class Game:
    def __init__(
            self,
            width: int,
            height: int,
            min_circles: int,
            max_circles: int,
            min_speed: float,
            max_speed: float,
            bg_color: tuple,
            text_color: tuple,
            secondary_color: tuple,
            hint_color: tuple,
            help_color: tuple
            ):
        # Сохраняем настройки
        self.width = width
        self.height = height
        self.min_circles = min_circles
        self.max_circles = max_circles
        self.min_speed = min_speed
        self.max_speed = max_speed
        self.bg_color = bg_color
        self.text_color = text_color
        self.secondary_color = secondary_color
        self.hint_color = hint_color
        self.help_color = help_color

        # Инициализируем состояние игры
        self.setup_game()
        
    def setup_game(self):
        self.circles = [self.spawn_circle() for _ in range(randint(self.min_circles, self.max_circles))]
        self.score = 0
        self.speed_multiplier = 1.0
        
    def spawn_circle(self):
        return Circle(
            self.width,
            self.height,
            self.min_speed,
            self.max_speed
            )
    
    def handle_click(self, pos: tuple):
        for circle in self.circles:
            if circle.is_clicked(pos) and not circle.is_popping:
                circle.is_popping = True
                self.score += 1
                self.speed_multiplier = 1 + self.score * 0.1
                break
                
    def update(self):
        for i, circle in enumerate(self.circles):
            if circle.update():
                self.circles[i] = self.spawn_circle()
            else:
                circle.move(self.speed_multiplier)

        # Проверяем столкновения между кругами
        self.circle_collision()

    def circle_collision(self):
        circles = self.circles
        n = len(circles)

        for i in range(n):
            for j in range(i + 1, n):
                a = circles[i]
                b = circles[j]
                
                if a.is_popping or b.is_popping:
                    continue

                self.collide(a, b)

    def collide(self, a, b):
        # Вектор от центра a до центра b
        dx = b.x - a.x
        dy = b.y - a.y
        distance = math.hypot(dx, dy)
        min_distance = a.radius + b.radius

        if distance >= min_distance or distance == 0:
            return
        
        # --- Шаг 1: раздвигаем круги, чтобы они не перекрывались ---
        overlap = min_distance - distance
        # Нормализованный вектор направления (единичный вектор)
        nx = dx / distance
        ny = dy / distance

        # Каждый круг отодвигается на половину перекрытия
        a.x -= nx * overlap / 2
        a.y -= ny * overlap / 2
        b.x += nx * overlap / 2
        b.y += ny * overlap / 2

        # --- Шаг 2: обмениваем проекции скоростей на ось столкновения ---
        # Проекция скорости a на ось nx, ny
        a_proj = a.dx * nx + a.dy * ny
        # Проекция скорости b на ось nx, ny
        b_proj = b.dx * nx + b.dy * ny

        # Меняем только проекции на ось столкновения (равные массы)
        a.dx += (b_proj - a_proj) * nx
        a.dy += (b_proj - a_proj) * ny
        b.dx += (a_proj - b_proj) * nx
        b.dy += (a_proj - b_proj) * ny
            
    def draw(self, screen):
        screen.fill(self.bg_color)

        for circle in self.circles:
            circle.draw(screen)

        screen.draw.text(
            f"Счет: {self.score}",
            topleft=(20, 20),
            fontsize=30,
            color=self.text_color,
        )

        screen.draw.text(
            f"Скорость: x{self.speed_multiplier:.1f}",
            topright=(self.width - 20, 20),
            fontsize=30,
            color=self.secondary_color,
        )

        screen.draw.text(
            "Нажимай левой кнопкой мыши на шарики, чтобы лопать их",
            center=(self.width // 2, self.height - 40),
            fontsize=24,
            color=self.hint_color,
        )

        screen.draw.text(
            "R - новая игра | ESC - выход",
            center=(self.width // 2, self.height - 15),
            fontsize=20,
            color=self.help_color,
        )
