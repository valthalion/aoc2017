# Double-heigh hex coordinates from https://www.redblobgames.com/grids/hexagons/

vector = {
    'n': 2j,
    'ne': 1+1j,
    'se': 1-1j,
    's': -2j,
    'sw': -1-1j,
    'nw': -1+1j
}


def read_data():
    with open('puzzle11.in', 'r') as f:
        for direction in next(f).strip().split(','):
            yield vector[direction]


def distance(v):
    dcol, drow = abs(v.real), abs(v.imag)
    return dcol + max(0, (drow - dcol) / 2)


def part_1():
    pos = 0
    for move in read_data():
        pos += move
    return distance(pos)


def part_2():
    pos, max_dist = 0, 0
    for move in read_data():
        pos += move
        if (dist := distance(pos)) > max_dist:
            max_dist = dist
    return max_dist
