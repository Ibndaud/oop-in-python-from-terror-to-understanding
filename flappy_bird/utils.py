def percent_range(size: int, value_range: tuple[int, int]) -> tuple[int, int]:
    """Переводит диапазон в процентах в точные граничные пиксели: (7, 55) от size -> (px, px)."""
    return (
        int(size * value_range[0] / 100),
        int(size * value_range[1] / 100),
    )