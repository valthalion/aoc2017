from math import sqrt


test = False


def read_data():
    filename = 'puzzle21_test.in' if test else 'puzzle21.in'
    transform = {2: {}, 3: {}}
    with open(filename, 'r') as f:
        for line in f:
            orig, dest = line.strip().split(' => ')
            size, orig = parse(orig)
            dest = parse(dest)[1]
            for orig_variant in variants(orig, size):
                transform[size][orig_variant] = dest
    return transform


def parse(pattern):
    pattern = ''.join(c for c in pattern if c != '/')
    size = int(sqrt(len(pattern)))
    return size, frozenset(divmod(pos, size) for pos, value in enumerate(pattern) if value == '#')


def flip_h(pattern, size):
    return frozenset((r, size - c - 1) for r, c in pattern)


def flip_v(pattern, size):
    return frozenset((size - r - 1, c) for r, c in pattern)


def rot90(pattern, size):
    return frozenset((c, size - r - 1) for r, c in pattern)

def rot90_flip_h(pattern, size):
    return flip_h(rot90(pattern, size), size)


def rot90_flip_v(pattern, size):
    return flip_v(rot90(pattern, size), size)


def rot180(pattern, size):
    return frozenset((size - r - 1, size - c - 1) for r, c in pattern)


def rot180_flip_h(pattern, size):
    return flip_h(rot180(pattern, size), size)


def rot180_flip_v(pattern, size):
    return flip_v(rot180(pattern, size), size)


def rot270(pattern, size):
    return frozenset((size - c - 1, r) for r, c in pattern)


def rot270_flip_h(pattern, size):
    return flip_h(rot270(pattern, size), size)


def rot270_flip_v(pattern, size):
    return flip_v(rot270(pattern, size), size)


variations = [
    flip_h, flip_v,
    rot90, rot90_flip_h, rot90_flip_v,
    rot180, rot180_flip_h, rot180_flip_v,
    rot270, rot270_flip_h, rot270_flip_v,
]


def variants(pattern, size):
    yield pattern
    seen = {pattern}
    for variation in variations:
        new_pattern = variation(pattern, size)
        if new_pattern in seen:
            continue
        yield new_pattern
        seen.add(new_pattern)


class Grid:
    transform = read_data()

    def __init__(self, pattern='.#./..#/###'):
        self.size, on = parse(pattern)
        self.on = set(on)

    def __iter__(self):
        stride = 2 if self.size % 2 == 0 else 3
        for r_offset in range(0, self.size, stride):
            for c_offset in range(0, self.size, stride):
                yield (
                    (r_offset, c_offset),
                    frozenset((r, c)
                          for r in range(stride)
                          for c in range(stride)
                          if (r_offset + r, c_offset + c) in self.on)
                )

    def step(self):
        if self.size % 2 == 0:
            pattern_size = 2
            growth = lambda n: 3 * (n // 2)
        else:
            pattern_size = 3
            growth = lambda n: 4 * (n // 3)
        displace = lambda offset: (growth(offset[0]), growth(offset[1]))
        new_size = growth(self.size)

        new_on = set()
        for offset, pattern in self:
            r_offset, c_offset = displace(offset)
            new_on |= {(r_offset + r, c_offset + c) for r, c in self.transform[pattern_size][pattern]}
        self.on = new_on
        self.size = new_size

    def __str__(self):
        return '\n'.join(''.join('#' if (r, c) in self.on else '.' for c in range(self.size)) for r in range(self.size))

    __repr__ = __str__


def part_1():
    grid = Grid()
    for _ in range(2 if test else 5):
        grid.step()
    return len(grid.on)


def part_2():
    grid = Grid()
    for _ in range(2 if test else 18):
        grid.step()
    return len(grid.on)
