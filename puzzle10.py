from __future__ import annotations
from dataclasses import dataclass
from math import prod


def read_data(ascii_mode=False, test=False):
    if test:
        return (3, 4, 1, 5)
    with open('puzzle10.in', 'r') as f:
        if ascii_mode:
            return next(f).strip()
        return (int(n) for n in next(f).strip().split(','))


def multixor(seq):
    result = 0
    for item in seq:
        result ^= item
    return result


@dataclass(slots=True)
class Node:
    value: int
    succ: Node | None = None
    pred: Node | None = None

    def print(self):
        return f'[{self.pred.value} <- {self.value} -> {self.succ.value}]'


class CircularList:
    def __init__(self, size=256, debug=False):
        self.size = size
        self.debug = debug
        self.nodes = {n: Node(n) for n in range(size)}
        self.current = self.nodes[0]
        self.current_position = 0
        self.cursor = self.nodes[0]
        self.skip_size = 0
        for node in self.nodes.values():
            node.succ = self.nodes[(node.value + 1) % size]
            node.pred = self.nodes[(node.value - 1) % size]

    def __iter__(self):
        self.reset()
        yield from self.take(self.size)

    def reset(self):
        pos = self.current
        for _ in range(self.current_position):
            pos = pos.pred
        self.cursor = pos

    def take(self, k, reset=True):
        if reset:
            self.reset()
        for _ in range(k):
            yield self.cursor.value
            self.cursor = self.cursor.succ

    def subtour(self, start, length):
        pos = start
        for _ in range(length):
            yield pos
            pos = pos.succ

    def advance(self, length, start=None):
        if start is None:
            start = self.current
        pos = start
        for _ in range(length):
            pos = pos.succ
        return pos

    def move(self, length):
        if length <= 1:
            self.current = self.advance(self.skip_size + length)
            self.current_position = (self.current_position + self.skip_size + length) % self.size
            self.skip_size += 1
            return

        start = self.current
        end = self.advance(length - 1)

        start_dock, end_dock = start.pred, end.succ
        subtour = tuple(self.subtour(start, length))
        for pred, succ in zip(subtour[1:], subtour):
            pred.succ, succ.pred = succ, pred

        if length == self.size:
            # switch connections
            start.succ, end.pred = end, start
        else:
            start.succ, end_dock.pred = end_dock, start
            end.pred, start_dock.succ = start_dock, end

        self.current = self.advance(self.skip_size, start=self.current.succ)
        self.current_position = (self.current_position + self.skip_size + length) % self.size
        self.skip_size += 1

    def knot_hash(self, key):
        lengths = [ord(c) for c in key] + [17, 31, 73, 47, 23]
        for _ in range(64):
            for length in lengths:
                self.move(length)

        dense_h = self.dense_hash()
        knot_h = ''.join(int2hex(n) for n in dense_h)
        return knot_h

    def dense_hash(self):
        self.reset()
        for _ in range(16):
            yield multixor(self.take(16, reset=False))

    def print(self):
        pos = self.current
        while pos.succ is not self.current:
            print(pos.print() if self.debug else pos.value, end=', ')
            pos = pos.succ
        print(pos.print() if self.debug else pos.value, end=' | ')
        print(self.current_position)


def int2hex(n):
    digit1, digit2 = divmod(n, 16)
    return ''.join(str(d) if d < 10 else 'abcdef'[d - 10] for d in (digit1, digit2))


def part_1():
    test = False
    clist = CircularList(size=5 if test else 256)
    for length in read_data(test=test):
        clist.move(length)
    return prod(clist.take(2))


def part_2():
    test = False
    clist = CircularList(256)
    if test:
        key = '1,2,3'
    else:
        key = read_data(ascii_mode=True, test=test)
    return clist.knot_hash(key)
