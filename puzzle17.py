from collections import deque


def part_1():
    testing = False
    step = -(3 if testing else 354) - 1
    buffer = deque([0])
    for n in range(1, 2018):
        buffer.rotate(step)
        buffer.appendleft(n)
    return buffer[1]


def part_2():
    step = -354 - 1
    buffer = deque([0])
    zero_pos = 0
    for n in range(1, 50_000_001):
        zero_pos = (zero_pos + step) % len(buffer) + 1
        buffer.rotate(step)
        buffer.appendleft(n)
    return buffer[(zero_pos + 1) % len(buffer)]
