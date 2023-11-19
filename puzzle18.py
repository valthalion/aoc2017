from collections import deque


def convert(arg):
    try:
        result = int(arg)
    except ValueError:
        result = arg
    return result


def read_data(testing=False):
    filename = f'puzzle18{"_test" if testing else ""}.in'
    cmds = []
    with open(filename, 'r') as f:
        for line in f:
            cmd, *args = line.strip().split()
            cmds.append((cmd, tuple(convert(arg) for arg in args)))
    return cmds


class Program:
    def __init__(self, cmds, pid, send_to):
        self.cmds = cmds
        self.pid = pid
        self.send_to = send_to
        self.queue = deque()
        self.registers = {
            reg: 0
            for reg in set(arg
                           for _, args in cmds
                           for arg in args
                           if isinstance(arg, str)
                        )
            }
        self.registers['p'] = pid
        self.pc = 0
        self.running = True

    @property
    def waiting(self):
        return (not self.running) or len (self.queue) == 0
    
    def eval(self, x):
        if isinstance(x, str):
            return self.registers[x]
        return x

    def run(self, debug=False):
        exit_signal = None
        muls = 0
        while exit_signal is None:
            if not (0 <= self.pc < len(self.cmds)):
                self.running == False
                break
            cmd, args = self.cmds[self.pc]
            if cmd == 'mul':
                muls += 1
            exit_signal = getattr(self, cmd)(*args)
            self.pc += 1
        if debug:
            return exit_signal, muls
        return exit_signal

    def snd(self, x):
        x = self.eval(x)
        return(self.pid, self.send_to, x)  # from, to, value

    def set(self, x, y):
        y = self.eval(y)
        self.registers[x] = y

    def add(self, x, y):
        y = self.eval(y)
        self.registers[x] += y

    def sub(self, x, y):
        y = self.eval(y)
        self.registers[x] -= y

    def mul(self, x, y ):
        y = self.eval(y)
        self.registers[x] *= y

    def mod(self, x, y ):
        y = self.eval(y)
        self.registers[x] %= y

    def rcv(self, x):
        if not self.queue:
            self.pc -= 1  # To restart in the same place
            return 'waiting', x
        self.registers[x] = self.queue.popleft()

    def jgz(self, x, y):
        x, y = self.eval(x), self.eval(y)
        if x > 0:
            self.pc += y - 1  # pc will be incremented after command

    def jnz(self, x, y):
        x, y = self.eval(x), self.eval(y)
        if x != 0:
            self.pc += y - 1  # pc will be incremented after command


def computer1(cmds):
    program = Program(cmds, pid=0, send_to=0)
    last_msg = None
    while True:
        output = program.run()
        if output[0] == 'waiting':
            x = output[1]
            if program.registers[x] != 0:
                return last_msg
            program.queue.append(0)
        else:
            last_msg = output[2]


def computer(programs):
    deadlock = False
    msgs_sent = {pid: 0 for pid in programs}

    while not deadlock:
        for program in programs.values():
            if not program.running:
                continue
            while True:
                output = program.run()
                if output is None or output[0] == 'waiting':
                    break
                pid, send_to, value = output
                msgs_sent[pid] += 1
                programs[send_to].queue.append(value)
        deadlock = all(program.waiting for program in programs.values())

    return msgs_sent


def part_1():
    testing = False
    cmds = read_data(testing=testing)
    return computer1(cmds)


def part_2():
    testing = False
    test_cmds = [
        ('snd', (1,)),
        ('snd', (2,)),
        ('snd', ('p',)),
        ('rcv', ('a',)),
        ('rcv', ('b',)),
        ('rcv', ('c',)),
        ('rcv', ('d',)),
    ]
    cmds = test_cmds if testing else read_data(testing=testing)
    programs = {
        0: Program(cmds, pid=0, send_to=1),
        1: Program(cmds, pid=1, send_to=0)
    }
    msgs = computer(programs)
    return msgs[1]
