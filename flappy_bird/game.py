import pygame
import sys
from cloud import Cloud
from bird import Bird
from pipe import Pipe


BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


class Game:
    def __init__(
            self, 
            screen_width, 
            screen_height, 
            fps, 
            pipe_spawn_interval, 
            gravity, 
            jump_velocity, 
            pipe_width, 
            pipe_gap, 
            pipe_velocity
            ):
        pygame.init()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = fps
        self.pipe_spawn_interval = pipe_spawn_interval
        self.gravity = gravity
        self.jump_velocity = jump_velocity
        self.pipe_width = pipe_width
        self.pipe_gap = pipe_gap
        self.pipe_velocity = pipe_velocity

        self.best_score = 0

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.background = self.create_background()

        # Дальний слой облаков
        self.far_clouds = [
            Cloud(40, 80, 15, 0.6, 130),
            Cloud(200, 170, 15, 0.7, 130),
            Cloud(350, 60, 15, 0.5, 130),
        ]

        # Ближний слой облаков
        self.near_clouds = [
            Cloud(100, 250, 40, 1.0, 220),
            Cloud(300, 130, 40, 1.2, 220),
            Cloud(480, 320, 40, 0.9, 220),
        ]

        pygame.display.set_caption("Flappy Bird")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 25)
        self.big_font = pygame.font.SysFont("Arial", 50)

        self.reset()
        
    def reset(self):
        self.bird = Bird(self.screen_width // 5, self.screen_height // 2 - int(self.screen_height * .05))
        self.pipes = []
        self.score = 0
        self.game_over = False
        self.start_screen = True
        self.last_pipe_spawn = pygame.time.get_ticks()

    def draw_start_screen(self):
        title = self.big_font.render("Flappy Bird", True, WHITE)
        instruction = self.font.render("Нажмите ПРОБЕЛ для старта", True, WHITE)

        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 150))
        self.screen.blit(instruction, (self.screen_width // 2 - instruction.get_width() // 2, 300))

    def draw_game_over_screen(self):
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(100)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.big_font.render("GAME OVER", True, RED)
        score_text = self.font.render(f"Ваш счёт: {self.score}", True, WHITE)
        best_score_text = self.font.render(f"Ваш лучший счёт: {self.best_score}", True, WHITE)
        restart_text = self.font.render("Нажмите ПРОБЕЛ для рестарта", True, WHITE)

        self.screen.blit(game_over_text, (self.screen_width // 2 - game_over_text.get_width() // 2, 200))
        self.screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, 300))
        self.screen.blit(best_score_text, (self.screen_width // 2 - best_score_text.get_width() // 2, 350))
        self.screen.blit(restart_text, (self.screen_width // 2 - restart_text.get_width() // 2, 400))
        
    def update(self, dt):
        # Фон обновляется всегда
        for cloud in self.far_clouds:
            cloud.update(dt, self.screen_width)

        for cloud in self.near_clouds:
            cloud.update(dt, self.screen_width)
        
        if self.start_screen or self.game_over:
            return
        
        self.bird.update(dt, self.gravity, self.fps)

        if self.bird.y - self.bird.radius <= 0 or self.bird.y + self.bird.radius >= self.screen_height:
            self.game_over = True
            self.best_score = max(self.best_score, self.score)
            return

        now = pygame.time.get_ticks()

        if now - self.last_pipe_spawn > self.pipe_spawn_interval:
            self.pipes.append(Pipe(self.screen_width, self.pipe_width, self.pipe_gap, self.screen_height))
            self.last_pipe_spawn = now

        for pipe in self.pipes[:]:
            pipe.update(dt, self.pipe_velocity, self.fps)

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
                    self.bird.jump(self.jump_velocity, self.fps)
                elif not self.game_over:
                    self.bird.jump(self.jump_velocity, self.fps)
                else:
                    self.reset()

    def draw_sky(self):
        top_color = (50, 150, 255)
        bottom_color = (170, 220, 255)

        for y in range(self.screen_height):
            t = y / self.screen_height

            r = int(top_color[0] * (1 - t) + bottom_color[0] * t)
            g = int(top_color[1] * (1 - t) + bottom_color[1] * t)
            b = int(top_color[2] * (1 - t) + bottom_color[2] * t)

            pygame.draw.line(self.screen, (r, g, b), (0, y), (self.screen_width, y))

    def create_background(self):
        surface = pygame.Surface((self.screen_width, self.screen_height))

        top_color = (50, 150, 255)
        bottom_color = (170, 220, 255)

        for y in range(self.screen_height):
            t = y / (self.screen_height - 1)

            r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
            g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
            b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)

            pygame.draw.line(surface, (r, g, b), (0, y), (self.screen_width, y))

        return surface

    def draw(self):
        # 1. Небо
        self.screen.blit(self.background, (0, 0))

        # 2. Дальние облака
        for cloud in self.far_clouds:
            cloud.draw(self.screen)

        # 3. Ближние облака
        for cloud in self.near_clouds:
            cloud.draw(self.screen)

        # 4. Трубы
        for pipe in self.pipes:
            pipe.draw(self.screen)

        # 5. Птица
        self.bird.draw(self.screen)

        # 6. Интерфейс
        score_text = self.font.render(f"Счёт: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.start_screen:
            self.draw_start_screen()

        if self.game_over:
            self.draw_game_over_screen()

        pygame.display.flip()

    def run(self):
        while True:
            dt = self.clock.tick(self.fps) / 1000.0   # в секундах с прошлого кадра
            dt = min(dt, 0.05)  # защита от лагов/сворачивании окна
            self.handle_events()
            self.update(dt)
            self.draw()
