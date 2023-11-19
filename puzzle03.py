from math import ceil, sqrt


def distance(x1, y1, x2, y2):
    return abs(x2 - x1) + abs(y2 - y1)


def position(n):
    if n == 1:
        return 0, 0

    shell = ceil(sqrt(n))
    if shell % 2 == 0:
        shell += 1
    shell_side = shell - 1
    half_side = shell // 2

    start = (shell - 2) * (shell - 2) + 1
    side, steps = divmod(n - start, shell_side)
    if side == 0:
        x, y = half_side, 1 - half_side + steps
    elif side == 1:
        x, y = half_side - 1 - steps, half_side
    elif side == 2:
        x, y = -half_side, half_side - 1 - steps
    elif side == 3:
        x, y = -half_side + 1 + steps, -half_side
    else:
        raise RuntimeError
    return x, y


def part_1():
    address = 289326
    return distance(*position(address), 0, 0)


def neighbours(cell):
    x, y = cell
    for new_cell in (
        (x - 1, y - 1), (x - 1,   y  ), (x - 1, y + 1),
        (x    , y - 1),                 (x    , y + 1),
        (x + 1, y - 1), (x + 1,   y  ), (x + 1, y + 1),
    ):
        yield new_cell


def walk_memory():
    shell, x, y = 1, 0, 0
    while True:
        x += 1
        y -= 1
        shell += 2
        for _ in range(shell - 1):
            y += 1
            yield x, y
        for _ in range(shell - 1):
            x -= 1
            yield x, y
        for _ in range(shell - 1):
            y -= 1
            yield x, y
        for _ in range(shell - 1):
            x += 1
            yield x, y


def part_2():
    memory = {(0, 0): 1}
    for cell in walk_memory():
        cell_value = sum(memory[c] for c in neighbours(cell) if c in memory)
        if cell_value > 289326:
            return cell_value
        memory[cell] = cell_value
