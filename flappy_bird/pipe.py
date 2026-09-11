import pygame
import random


GREEN = (0, 200, 0)


class Pipe:
    def __init__(self, x, pipe_width, pipe_gap, screen_height):
        self.x = x
        self.width = pipe_width
        self.top_height = random.randint(100, screen_height - pipe_gap - 100)
        self.bottom_y = self.top_height + pipe_gap
        self.top_rect = pygame.Rect(self.x, 0, pipe_width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, pipe_width, screen_height - self.bottom_y)
        self.passed = False
        
    def update(self, dt, pipe_velocity, fps):
        self.x += int(pipe_velocity * fps * dt)
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        
    def off_screen(self):
        return self.x + self.width < 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

    def circle_rect_collision(self, bird, rect):
        # приближенное сравнение
        overlap = bird.get_rect().clip(rect)

        if overlap.width or overlap.height:
            # точное сравнение
            closest_x = max(rect.left, min(bird.x, rect.right))
            closest_y = max(rect.top, min(bird.y, rect.bottom))

            dx = bird.x - closest_x
            dy = bird.y - closest_y

            return dx ** 2 + dy ** 2 <= bird.radius ** 2

        return False

    def collide(self, bird):
        return (
            self.circle_rect_collision(bird, self.top_rect) or 
            self.circle_rect_collision(bird, self.bottom_rect)
            )
