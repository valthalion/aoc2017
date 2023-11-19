def read_data():
    with open('puzzle13.in', 'r') as f:
        return {
            int((depth_range := line.strip().split(': '))[0]): int(depth_range[1])
            for line in f
        }


def caught(rng, t):
    period = 2 * (rng - 1)
    return t % period == 0


def part_1():
    testing = False
    firewall = {0: 3, 1: 2, 4: 4, 6: 4} if testing else read_data()
    severity = sum(depth * rng for depth, rng in firewall.items() if caught(rng, t=depth))
    return severity


def part_2():
    testing = False
    firewall = {0: 3, 1: 2, 4: 4, 6: 4} if testing else read_data()
    delay = 0
    while True:
        delay += 1
        if any(caught(rng, t=depth + delay) for depth, rng in firewall.items()):
            continue
        return delay
