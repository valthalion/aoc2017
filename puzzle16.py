from collections import deque


commands = {
    's': 'spin',
    'x': 'exchange',
    'p': 'partner',
}


class Dance:
    def __init__(self, seq):
        self.programs = deque(seq)

    def spin(self, n):
        self.programs.rotate(n)

    def exchange(self, pos1, pos2):
        self.programs[pos1], self.programs[pos2] = self.programs[pos2], self.programs[pos1]

    def partner(self, p1, p2):
        self.exchange(self.programs.index(p1), self.programs.index(p2))

    def run_cmds(self, dance_steps):
        for cmd, args in dance_steps:
            getattr(self, cmd)(*args)
        return ''.join(self.programs)


def read_data():
    with open('puzzle16.in', 'r') as f:
        for spec in next(f).strip().split(','):
            cmd = spec[0]
            if cmd == 's':
                args = (int(spec[1:]),)
            elif cmd == 'x':
                args = tuple(int(n) for n in spec[1:].split('/'))
            elif cmd == 'p':
                args = tuple(spec[1:].split('/'))
            else:
                raise ValueError('Unknown command in spec:', spec)
            yield commands[cmd], args


def part_1():
    seq = 'abcdefghijklmnop'
    dance_steps = tuple(read_data())
    dance = Dance(seq)
    return dance.run_cmds(dance_steps)


def part_2():
    target = 1_000_000_000
    start = 'abcdefghijklmnop'
    dance_steps = tuple(read_data())
    dance = Dance(start)
    last = start
    configurations = {last: 0}
    
    for idx in range(1, target + 1):
        last = dance.run_cmds(dance_steps)
        if last in configurations:
            break
        configurations[last] = idx
    else:
        return last

    cycle_start = configurations[last]
    cycle_len = idx - cycle_start
    target_idx = cycle_start + ((target - idx) % cycle_len)
    configurations_lookup = {idx: config for config, idx in configurations.items()}
    final_config = configurations_lookup[target_idx]
    return final_config
