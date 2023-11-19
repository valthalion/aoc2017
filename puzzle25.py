testing = False


class TuringMachine:
    def __init__(self, initial_state, steps, states):
        self.state = initial_state
        self.memory = set()
        self.cursor = 0
        self.states = states
        self.steps = steps
        # self.print()

    def step(self):
        state = self.states[self.state]
        value_read = 1 if self.cursor in self.memory else 0
        write_value, offset, new_state = state[value_read]

        if value_read != write_value:
            if write_value:
                self.memory.add(self.cursor)
            else:
                self.memory.remove(self.cursor)

        self.cursor += offset
        self.state = new_state
        # self.print()

    def run(self):
        for _ in range(self.steps):
            self.step()

    def checksum(self):
        return len(self.memory)

    # def print(self):
    #     print(self.state, self.cursor, self.memory)


def read_data():
    filename = 'puzzle25_test.in' if testing else 'puzzle25.in'
    with open(filename, 'r') as f:
        initial_state = next(f)[-3]
        steps = int(next(f).split()[-2])
        next(f)

        states = {}
        while True:
            name = next(f)[-3]
            states[name] = {}
            for _ in range(2):
                value_read = int(next(f)[-3])
                to_write = int(next(f)[-3])
                offset = 1 if next(f).strip().endswith('right.') else -1
                next_state = next(f)[-3]
                states[name][value_read] = (to_write, offset, next_state)
            try:
                next(f)
            except StopIteration:
                break
    return TuringMachine(initial_state, steps, states)


def part_1():
    turing_macihne = read_data()
    turing_macihne.run()
    return turing_macihne.checksum()


def part_2():
    pass
