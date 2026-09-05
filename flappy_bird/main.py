GRAVITY = 0.5
JUMP_VELOCITY = -10

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