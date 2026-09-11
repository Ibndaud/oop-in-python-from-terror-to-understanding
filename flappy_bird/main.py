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
        SCREEN_WIDTH, 
        SCREEN_HEIGHT, 
        FPS, 
        PIPE_SPAWN_INTERVAL, 
        GRAVITY, 
        JUMP_VELOCITY, 
        PIPE_WIDTH, 
        PIPE_GAP, 
        PIPE_VELOCITY
        )
    print("And, here we go again...")
    game.run()