from game import Game


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

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600


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