def read_data(testing=False):
    filename = f'puzzle19{"_test" if testing else ""}.in'
    cells = {}
    with open(filename, 'r') as f:
        for r, line in enumerate(f):
            for c, value in enumerate(line.rstrip()):
                if value == ' ':
                    continue    
                if r == 0 and value == '|':
                    start = complex(c, r)
                cells[complex(c, r)] = value
    return cells, start


def path(cells, start):
    heading = 1j
    pos = start
    yield cells[pos]

    while True:
        for turn in (1, 1j, -1j):
            if pos + heading * turn in cells:
                heading *= turn
                pos += heading
                yield cells[pos]
                break
        else:
            break


def part_1():
    testing = False
    cells, start = read_data(testing=testing)
    collected = [value for value in path(cells, start) if value not in '-|+']
    return ''.join(collected)


def part_2():
    testing = False
    cells, start = read_data(testing=testing)
    return sum(1 for _ in path(cells, start))
