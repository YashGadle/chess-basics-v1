def coordinates_to_notations(coordinates):
    return [f"{chr(97 + col)}{8 - row}" for row, col in coordinates]
