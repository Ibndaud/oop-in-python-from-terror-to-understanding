import pygame


YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)


class Bird:
    def __init__(self, x, y, gravity, jump_velocity):
        self.x = x
        self.y = y
        self.gravity = gravity
        self.jump_velocity = jump_velocity
        self.velocity = 0
        self.radius = 15
        self.angle = 0
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA) # Создаём прозрачную картинку птицы
        pygame.draw.circle(self.image, YELLOW, (20, 20), self.radius) # Создаём тело птицы
        pygame.draw.circle(self.image, BLACK, (25, 15), 3) # Создаём глаз птицы
        pygame.draw.polygon(self.image, RED, [(34, 16), (48, 20), (34, 24)]) # Создаём клюв птицы
        
    def update(self, dt):
        self.velocity += self.gravity * dt
        self.y += self.velocity * dt
        self.rect.center = (int(self.x), int(self.y))
        target_angle = max(-45, min(45, -self.velocity * .05))
        rotation_speed = 200  # градусов в секунду
        if self.angle < target_angle:
            self.angle = min(self.angle + rotation_speed * dt, target_angle)
        elif self.angle > target_angle:
            self.angle = max(self.angle - rotation_speed * dt, target_angle)

    def jump(self):
        self.velocity = self.jump_velocity

    def get_rect(self):
        return self.rect
        
    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_image, rotated_rect)
