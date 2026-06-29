WIDTH, HEIGHT = 1200, 768


class Circle:
    def __init__(self):
        self.radius = 5
        self.color = (132, 255, 24)
        self.x = 100
        self.y = 150
        self.dx = 2.0
        self.dy = 1.5
        self.is_popping = False
        self.pop_progress = 0.0
        self.pop_speed = 0.2
        
    def move(self, multiplier):
        if self.is_popping:
            return
        self.x += self.dx * multiplier
        self.y += self.dy * multiplier
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.x = min(max(self.x, self.radius), WIDTH - self.radius)
            self.dx = -self.dx
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.y = min(max(self.y, self.radius), HEIGHT - self.radius)
            self.dy = -self.dy
                
    def update(self):
        if self.is_popping:
            self.pop_progress += self.pop_speed
            return True if self.pop_progress >= 1 else False
        return False
    
    def is_clicked(self, pos):
        _x, _y = pos
        return (pow(_x - self.x, 2) + pow(_y - self.y, 2)) ** 0.5 <= self.radius
    
    def draw(self):
        return f'Circle: ({self.x}, {self.y}), r={self.radius}, color={self.color}'
