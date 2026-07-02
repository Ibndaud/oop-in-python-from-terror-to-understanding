import pgzrun
from game import Game


# ------------------------------------------------------------
# Константы (настройки игры)
# ------------------------------------------------------------
TITLE = "Тык-тык"

BACKGROUND_COLOR = (20, 30, 40)
TEXT_COLOR = (220, 220, 220)
SECONDARY_TEXT_COLOR = (200, 200, 200)
HINT_TEXT_COLOR = (180, 180, 200)
HELP_TEXT_COLOR = (160, 160, 180)

WIDTH, HEIGHT = 1200, 768

MIN_SPEED = 1.0
MAX_SPEED = 3.0

MIN_CIRCLES = 3
MAX_CIRCLES = 7


# ------------------------------------------------------------
# Pygame Zero hooks (функции, которые вызывает движок)
# ------------------------------------------------------------
game = Game(
    width=WIDTH,
    height=HEIGHT,
    min_circles=MIN_CIRCLES,
    max_circles=MAX_CIRCLES,
    min_speed=MIN_SPEED,
    max_speed=MAX_SPEED,
    bg_color=BACKGROUND_COLOR,
    text_color=TEXT_COLOR,
    secondary_color=SECONDARY_TEXT_COLOR,
    hint_color=HINT_TEXT_COLOR,
    help_color=HELP_TEXT_COLOR
    )


def update():
    """Pygame Zero вызывает эту функцию каждый кадр."""
    game.update()


def draw():
    """Pygame Zero вызывает эту функцию для отрисовки кадра."""
    game.draw(screen)


def on_mouse_down(pos, button):
    """
    Pygame Zero вызывает эту функцию при клике мышью.

    pos — координаты клика (x, y)
    button — кнопка мыши
    """
    if button == mouse.LEFT:
        game.handle_click(pos)


def on_key_down(key):
    """
    Pygame Zero вызывает эту функцию при нажатии клавиши.

    R — перезапуск
    ESC — выход из игры
    """
    if key == keys.R:
        game.setup_game()
    elif key == keys.ESCAPE:
        exit()


print(f"And, here we go again...")
pgzrun.go()