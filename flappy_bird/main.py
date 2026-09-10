import pygame
import sys
import random


# ------------------------------------------------------------
# Константы (настройки игры)
# ------------------------------------------------------------
FPS = 60
GRAVITY = 0.5
JUMP_VELOCITY = -10

PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_VELOCITY = -3
PIPE_SPAWN_INTERVAL = 1500

BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.radius = 15
        self.angle = 0
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        self.image = pygame.Surface((50, 40), pygame.SRCALPHA) # Создаём прозрачную картинку птицы
        pygame.draw.circle(self.image, YELLOW, (20, 20), self.radius) # Создаём тело птицы
        pygame.draw.circle(self.image, BLACK, (25, 15), 3) # Создаём глаз птицы
        pygame.draw.polygon(self.image, RED, [(34, 16), (48, 20), (34, 24)]) # Создаём клюв птицы
        
    def update(self, dt):
        self.velocity += GRAVITY * FPS ** 2 * dt
        self.y += self.velocity * dt
        self.rect.center = (int(self.x), int(self.y))

        target_angle = max(-45, min(45, -self.velocity * .05))
        rotation_speed = 200  # градусов в секунду
        if self.angle < target_angle:
            self.angle = min(self.angle + rotation_speed * dt, target_angle)
        elif self.angle > target_angle:
            self.angle = max(self.angle - rotation_speed * dt, target_angle)

    def jump(self):
        self.velocity = JUMP_VELOCITY * FPS

    def get_rect(self):
        return self.rect
        
    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        rotated_rect = rotated_image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(rotated_image, rotated_rect)


class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.gap = PIPE_GAP
        self.top_height = random.randint(100, SCREEN_HEIGHT - self.gap - 100)
        self.bottom_y = self.top_height + self.gap
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y)
        self.passed = False
        
    def update(self, dt):
        self.x += int(PIPE_VELOCITY * FPS * dt)
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        
    def off_screen(self):
        return self.x + PIPE_WIDTH < 0
    
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

    
    
class Game:
    def __init__(self):
        pygame.init()

        self.best_score = 0

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 25)
        self.big_font = pygame.font.SysFont("Arial", 50)

        self.reset()
        
    def reset(self):
        self.bird = Bird(SCREEN_WIDTH // 5, SCREEN_HEIGHT // 2 - int(SCREEN_HEIGHT * .05))
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.start_screen = True
        self.last_pipe_spawn = pygame.time.get_ticks()

    def draw_start_screen(self):
        title = self.big_font.render("Flappy Bird", True, WHITE)
        instruction = self.font.render("Нажмите ПРОБЕЛ для старта", True, WHITE)

        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        self.screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 300))

    def draw_game_over_screen(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.big_font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Ваш счёт: {self.score}", True, WHITE)
        best_score_text = self.font.render(f"Ваш лучший счёт: {self.best_score}", True, WHITE)
        restart_text = self.font.render("Нажмите ПРОБЕЛ для рестарта", True, WHITE)

        self.screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        self.screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 300))
        self.screen.blit(best_score_text, (SCREEN_WIDTH // 2 - best_score_text.get_width() // 2, 350))
        self.screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400))
        
    def update(self, dt):
        if self.start_screen or self.game_over:
            return
        
        self.bird.update(dt)

        if self.bird.y - self.bird.radius <= 0 or self.bird.y + self.bird.radius >= SCREEN_HEIGHT:
            self.game_over = True
            self.best_score = max(self.best_score, self.score)
            return

        now = pygame.time.get_ticks()

        if now - self.last_pipe_spawn > PIPE_SPAWN_INTERVAL:
            self.pipes.append(Pipe(SCREEN_WIDTH))
            self.last_pipe_spawn = now

        for pipe in self.pipes[:]:
            pipe.update(dt)

            if pipe.collide(self.bird):
                self.game_over = True
                self.best_score = max(self.best_score, self.score)
            if pipe.off_screen():
                self.pipes.remove(pipe)
            if not pipe.passed and pipe.x + pipe.width < self.bird.x:
                pipe.passed = True
                self.score += 1

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                if self.start_screen:
                    self.start_screen = False
                    self.last_pipe_spawn = pygame.time.get_ticks()
                    self.bird.jump()
                elif not self.game_over:
                    self.bird.jump()
                else:
                    self.reset()

    def draw(self):
        self.screen.fill(BLUE)
        self.bird.draw(self.screen)

        for pipe in self.pipes:
            pipe.draw(self.screen)

        score_text = self.font.render(f"Счёт: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.start_screen:
            self.draw_start_screen()

        if self.game_over:
            self.draw_game_over_screen()

        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(FPS) / 1000.0   # в секундах с прошлого кадра
            dt = min(dt, 0.05)  # защита от лагов/сворачивании окна
            self.handle_events()
            self.update(dt)
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()