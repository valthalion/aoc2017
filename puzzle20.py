from collections import defaultdict
from dataclasses import dataclass
import re


particle_re = re.compile(r'p=<(?P<p>\-?\d+,\-?\d+,\-?\d+)>, v=<(?P<v>\-?\d+,\-?\d+,\-?\d+)>, a=<(?P<a>\-?\d+,\-?\d+,\-?\d+)>')


def read_data(testing=False):
    test_suffix = f'_test{testing}'
    filename = f'puzzle20{test_suffix if testing else ""}.in'
    with open(filename, 'r') as f:
        return [Particle(*parse(line.strip())) for line in f]


def parse(line):
    m = particle_re.match(line)
    p = Vector(int(n) for n in m.group('p').split(','))
    v = Vector(int(n) for n in m.group('v').split(','))
    a = Vector(int(n) for n in m.group('a').split(','))
    return p, v, a


class Vector:
    def __init__(self, seq):
        self.components = tuple(seq)

    def __iter__(self):
        return iter(self.components)

    def __add__(self, other):
        return Vector(c1 + c2 for c1, c2 in zip(self, other))

    def __sub__(self, other):
        return Vector(c1 - c2 for c1, c2 in zip(self, other))

    def __str__(self):
        return f'Vector{self.components}'

    __repr__ = __str__

    def abs(self):
        return sum(abs(c) for c in self)


@dataclass(slots=True)
class Particle:
    p: Vector
    v: Vector
    a: Vector

    def step(self):
        self.v += self.a
        self.p += self.v


def part_1():
    testing = False
    particles = read_data(testing=1 if testing else 0)
    pos = min(range(len(particles)), key=lambda p: particles[p].a.abs())
    print(particles[pos])
    return pos


def part_2():
    testing = False
    particles = read_data(testing=2 if testing else 0)
    particles = {part_id: part for part_id, part in enumerate(particles)}

    iteration = 0
    # TODO: define stoping condition, when are all collisions done? (this was just eyeballing it)
    while len(particles) > 1 and iteration <= 100:
        iteration += 1

        positions = defaultdict(set)
        for part_id, part in particles.items():
            part.step()
            positions[part.p.components].add(part_id)

        collisions = {part_id for group in positions.values() if len(group) > 1 for part_id in group}
        for part_id in collisions:
            del(particles[part_id])

    return len(particles)
