def percent_range(size: int, value_range: tuple[int, int]) -> tuple[int, int]:
    return (
        int(size * value_range[0] / 100),
        int(size * value_range[1] / 100),
    )