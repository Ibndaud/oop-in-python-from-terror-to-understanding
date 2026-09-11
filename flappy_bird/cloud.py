import pygame
import random


class Cloud:
    def __init__(self, x, y, speed, scale=1.0, alpha=255):
        self.x = float(x)
        self.y = float(y)
        self.speed = speed
        self.scale = scale

        width = int(100 * scale)
        height = int(50 * scale)

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)

        color = (255, 255, 255, alpha)

        pygame.draw.circle(self.image, color, (int(30 * scale), int(28 * scale)), int(18 * scale))
        pygame.draw.circle(self.image, color, (int(50 * scale), int(20 * scale)), int(23 * scale))
        pygame.draw.circle(self.image, color, (int(72 * scale), int(30 * scale)), int(16 * scale))
        pygame.draw.ellipse(self.image, color, (int(20 * scale), int(25 * scale), int(65 * scale), int(20 * scale)))

    def update(self, dt, screen_width):
        self.x -= self.speed * dt

        if self.x + self.image.get_width() < 0:
            self.x = screen_width + random.randint(20, 150)
            self.y = random.randint(40, 350)

    def draw(self, screen):
        screen.blit(self.image, (int(self.x), int(self.y)))
