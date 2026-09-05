import pygame
import sys


FPS = 60
GRAVITY = 0.5
JUMP_VELOCITY = -10

PIPE_WIDTH = 70
PIPE_GAP = 200
PIPE_VELOCITY = -4

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
        
    def draw(self):
        print('(•)>')


class Pipe:
    def __init__(self, x):
        self.x = x
        self.width = PIPE_WIDTH
        self.gap = PIPE_GAP
        self.top_height = 100
        self.bottom_y = self.top_height + self.gap
        self.passed = False
        
    def update(self):
        self.x += PIPE_VELOCITY
        
    def off_screen(self):
        return self.x + PIPE_WIDTH < 0
    
    def draw(self):
        print(('###' + '\n') * (self.top_height // 20) 
              + '\n' 
              + ('###' + '\n') * ((SCREEN_HEIGHT - self.bottom_y) // 20 - 1) 
              + '###')
    
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

    def run(self):
        while True:
            self.handle_events()
            self.clock.tick(FPS)


if __name__ == "__main__":
    game = Game()
    game.run()