def generator(seed, factor, mod_value=2147483647):
    current = seed
    while True:
        current = (current * factor) % mod_value
        yield current


def picky_generator(seed, factor, picky_factor, mod_value=2147483647):
    current = seed
    while True:
        current = (current * factor) % mod_value
        if current % picky_factor != 0:
            continue
        yield current


def match(a, b):
    return 1 if (a & 0xffff) == (b & 0xffff) else 0


def part_1():
    testing = False
    generator_a = generator(seed=65 if testing else 722, factor=16807)
    generator_b = generator(seed=8921 if testing else 354, factor=48271)
    return sum(match(next(generator_a), next(generator_b)) for _ in range(40_000_000))


def part_2():
    testing = False
    generator_a = picky_generator(seed=65 if testing else 722, factor=16807, picky_factor=4)
    generator_b = picky_generator(seed=8921 if testing else 354, factor=48271, picky_factor=8)
    return sum(match(next(generator_a), next(generator_b)) for _ in range(5_000_000))
