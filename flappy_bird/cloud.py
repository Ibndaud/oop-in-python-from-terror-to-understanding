import pygame
import random

from utils import percent_range


X_SHIFT_RANGE = (4, 40) # диапазон в % для сдвига х-координат облаков


class Cloud:
    def __init__(self, x, y, speed, scale=1.0, alpha=255, screen_width=400, screen_height=600, y_range=(7, 55)): # y_range в % от screen_height
        self.x = float(x)
        self.y = float(y)
        self.speed = speed
        self.scale = scale
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.y_range = y_range

        width = int(100 * scale)
        height = int(50 * scale)

        self.x_shift = percent_range(screen_width, X_SHIFT_RANGE)

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        color = (255, 255, 255, alpha)

        pygame.draw.circle(self.image, color, (int(30 * scale), int(28 * scale)), int(18 * scale))
        pygame.draw.circle(self.image, color, (int(50 * scale), int(20 * scale)), int(23 * scale))
        pygame.draw.circle(self.image, color, (int(72 * scale), int(30 * scale)), int(16 * scale))
        pygame.draw.ellipse(self.image, color, (int(20 * scale), int(25 * scale), int(65 * scale), int(20 * scale)))

    def update(self, dt):
        self.x -= self.speed * dt

        if self.x + self.image.get_width() < 0:
            self.x = self.screen_width + random.randint(*self.x_shift)
            self.y = random.randint(*self.y_range)

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))
