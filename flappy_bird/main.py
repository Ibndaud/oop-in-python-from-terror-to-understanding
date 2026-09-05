import pygame
import sys


# ------------------------------------------------------------
# Константы (настройки игры)
# ------------------------------------------------------------
FPS = 60
GRAVITY = 0.5
JUMP_VELOCITY = -10

PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_VELOCITY = -3

BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 200, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0
        self.radius = 15
        
    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        
    def jump(self):
        self.velocity = JUMP_VELOCITY
        
    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, BLACK, (int(self.x) + 5, int(self.y) - 5), 3)
        font = pygame.font.SysFont("Arial", 22)
        beak = font.render(">", True, RED)
        screen.blit(beak, (int(self.x) + self.radius - 2, int(self.y) - 14))


class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.gap = PIPE_GAP
        self.top_height = 100
        self.bottom_y = self.top_height + self.gap
        self.top_rect = pygame.Rect(self.x, 0, self.width, self.top_height)
        self.bottom_rect = pygame.Rect(self.x, self.bottom_y, self.width, SCREEN_HEIGHT - self.bottom_y)
        self.passed = False
        
    def update(self):
        self.x += PIPE_VELOCITY
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x
        
    def off_screen(self):
        return self.x + PIPE_WIDTH < 0
    
    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.top_rect)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)
    
    def collide(self, bird):
        horizontal = bird.x + bird.radius > self.x and bird.x - bird.radius < self.x + self.width
        vertical =  self.top_height > bird.y - bird.radius or self.bottom_y < bird.y + bird.radius
        return horizontal and vertical
    
    
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Flappy Bird")
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        self.bird = Bird(100, SCREEN_HEIGHT // 2)
        self.pipes = []
        self.score = 0
        self.game_over = False
        
    def update(self):
        self.bird.update()
        for pipe in self.pipes:
            pipe.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.bird.jump()

    def draw(self):
        self.screen.fill(BLUE)
        self.bird.draw(self.screen)
        for pipe in self.pipes:
            pipe.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.pipes.append(Pipe(250))
    game.run()