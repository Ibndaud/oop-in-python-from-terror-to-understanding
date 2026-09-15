import pygame
import random

from bird import Bird


GREEN = (0, 200, 0)


class Pipe:
    """Пара труб — верхняя и нижняя — с проёмом для пролёта птицы."""

    def __init__(self, x: float, pipe_width: int, pipe_gap: int, screen_height: int, pipe_velocity: float) -> None:
        self.x = x
        self.width = pipe_width
        self.top_height = random.randint(100, screen_height - pipe_gap - 100)
        self.bottom_y = self.top_height + pipe_gap
        self.top_rect = pygame.Rect(self.x, 0, pipe_width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, pipe_width, screen_height - self.bottom_y)
        self.pipe_velocity = pipe_velocity
        self.passed = False
        
    def update(self, dt: float) -> None:
        """Перемещает трубы влево с заданной скоростью скоростью."""
        self.x += self.pipe_velocity * dt
        self.top_rect.x = int(self.x)
        self.bottom_rect.x = int(self.x)
        
    def off_screen(self) -> bool:
        """Проверка, что пара труб полностью ушла за левый край экрана."""
        return self.x + self.width < 0
    
    def draw(self, screen: pygame.Surface) -> None:
        """Отрисовка труб."""
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

    def circle_rect_collision(self, bird: Bird, rect: pygame.Rect) -> bool:
        """Проверка коллизии птицы и трубы."""
        # быстрое приближенное сравнение (Rect vs Rect)
        overlap = bird.get_rect().clip(rect)

        if not overlap:
            return False
        
        # точное сравнение (Circle vs Rect)
        closest_x = max(rect.left, min(bird.x, rect.right))
        closest_y = max(rect.top, min(bird.y, rect.bottom))

        dx = bird.x - closest_x
        dy = bird.y - closest_y

        return dx ** 2 + dy ** 2 <= bird.radius ** 2

    def collide(self, bird: Bird) -> bool:
        """Проверка, задела ли птица одну из труб."""
        return (
            self.circle_rect_collision(bird, self.top_rect) or 
            self.circle_rect_collision(bird, self.bottom_rect)
            )
