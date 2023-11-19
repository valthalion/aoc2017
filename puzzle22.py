testing = False


def read_data():
    filename = 'puzzle22_test.in' if testing else 'puzzle22.in'
    infected = set()
    with open(filename, 'r') as f:
        for r, line in enumerate(f):
            for c, value in enumerate(line.strip()):
                if value == '#':
                    infected.add((r, c))
    rows, columns = r, c
    infected = {complex(c, rows - r) for r, c in infected}
    start = complex(columns // 2, rows // 2)
    return start, infected


def part_1():
    pos, infected = read_data()

    def burst(pos, heading):
        started_infected = pos in infected
        if started_infected:
            heading *= -1j
            infected.remove(pos)
        else:
            heading *= 1j
            infected.add(pos)
        return pos + heading, heading, not started_infected

    heading, infections = 1j, 0
    for _ in range(10_000):
        pos, heading, new_infection = burst(pos, heading)
        if new_infection:
            infections += 1
    return infections


def part_2():
    pos, infected = read_data()
    weakened, flagged = set(), set()

    def burst(pos, heading):
        infection = False
        if pos in infected:
            heading *= -1j
            infected.remove(pos)
            flagged.add(pos)
        elif pos in weakened:
            infection = True
            weakened.remove(pos)
            infected.add(pos)
        elif pos in flagged:
            heading *= -1
            flagged.remove(pos)
        else:  # clean
            heading *= 1j
            weakened.add(pos)
        return pos + heading, heading, infection

    heading, infections = 1j, 0
    for _ in range(10_000_000):
        pos, heading, new_infection = burst(pos, heading)
        if new_infection:
            infections += 1
    return infections
