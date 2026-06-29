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


class Game:
    _CIRCLE_NUMBER = 5
    
    def __init__(self):
        self.setup_game()
        
    def setup_game(self):
        self.circles = [self.spawn_circle() for _ in range(self._CIRCLE_NUMBER)]
        self.score = 0
        self.speed_multiplier = 1.0
        
    def spawn_circle(self):
        return Circle()
    
    def handle_click(self, pos):
        for circle in self.circles:
            if circle.is_clicked(pos):
                circle.is_popping = True
                self.score += 1
                self.speed_multiplier = 1 + self.score * 0.1
                break
                
    def update(self):
        self.circles = [circle if not circle.update() else self.spawn_circle() for circle in self.circles]
        for circle in self.circles:
            circle.move(self.speed_multiplier)
            
    def draw(self):
        return self.score, [circle.draw() for circle in self.circles]
    