from puzzle10 import CircularList
from puzzle12 import connected_components


ones = {
    '0': (0, 0, 0, 0),
    '1': (0, 0, 0, 1),
    '2': (0, 0, 1, 0),
    '3': (0, 0, 1, 1),
    '4': (0, 1, 0, 0),
    '5': (0, 1, 0, 1),
    '6': (0, 1, 1, 0),
    '7': (0, 1, 1, 1),
    '8': (1, 0, 0, 0),
    '9': (1, 0, 0, 1),
    'a': (1, 0, 1, 0),
    'b': (1, 0, 1, 1),
    'c': (1, 1, 0, 0),
    'd': (1, 1, 0, 1),
    'e': (1, 1, 1, 0),
    'f': (1, 1, 1, 1)
}


def chain(*args):
    for arg in args:
        for item in arg:
            yield item


def neighbours(node):
    r, c = node
    yield (r - 1, c)
    yield (r + 1, c)
    yield (r, c - 1)
    yield (r, c + 1)


def part_1():
    testing = False
    key_string = 'flqrgnkx' if testing else 'uugsqrei'
    used = 0
    for n in range(128):
        row_key = f'{key_string}-{n}'
        clist = CircularList()
        row_hash = clist.knot_hash(row_key)
        row = chain(*(ones[c] for c in row_hash))
        used += sum(row)
    return used


def part_2():
    testing = False
    key_string = 'flqrgnkx' if testing else 'uugsqrei'
    nodes = set()
    for r in range(128):
        row_key = f'{key_string}-{r}'
        clist = CircularList()
        row_hash = clist.knot_hash(row_key)
        row = chain(*(ones[c] for c in row_hash))
        nodes |= {(r, c) for c, used in enumerate(row) if used}

    graph = {
        node: {neighbour for neighbour in neighbours(node) if neighbour in nodes}
        for node in nodes
    }

    return sum(1 for _ in connected_components(graph))
