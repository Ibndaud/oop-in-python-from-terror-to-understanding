from game import Game


# ------------------------------------------------------------
# Константы (настройки игры)
# ------------------------------------------------------------
FPS = 60
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Физика птицы
GRAVITY = 1800 # px/s²
JUMP_VELOCITY = -600 # px/s

# Физика трубы
PIPE_WIDTH = 70 # px
PIPE_GAP = 200 # px
PIPE_SPAWN_INTERVAL = 1500 # ms
PIPE_VELOCITY = -180 # px/s


if __name__ == "__main__":
    game = Game(
        screen_width=SCREEN_WIDTH, 
        screen_height=SCREEN_HEIGHT, 
        fps=FPS, 
        pipe_spawn_interval=PIPE_SPAWN_INTERVAL, 
        gravity=GRAVITY, 
        jump_velocity=JUMP_VELOCITY, 
        pipe_width=PIPE_WIDTH, 
        pipe_gap=PIPE_GAP, 
        pipe_velocity=PIPE_VELOCITY
        )
    print("And, here we go again...")
    game.run()