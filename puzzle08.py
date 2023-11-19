from itertools import chain
from typing import NamedTuple


class Cmd(NamedTuple):
    target_reg: str
    op: str
    val: int
    cond_reg: str
    cond: str
    cond_val: int


class Cpu:
    def __init__(self, cmds):
        self.max_value = 0
        registers = set(chain((cmd.target_reg for cmd in cmds), (cmd.cond_reg for cmd in cmds)))
        self.registers = {register: 0 for register in registers}
        self.cmds = cmds

    def run(self):
        for cmd in self.cmds:
            if self.condition(cmd):
                self.operation(cmd)

    def condition(self, cmd):
        if cmd.cond == '==':
            return self.registers[cmd.cond_reg] == cmd.cond_val
        elif cmd.cond == '!=':
            return self.registers[cmd.cond_reg] != cmd.cond_val
        elif cmd.cond == '>=':
            return self.registers[cmd.cond_reg] >= cmd.cond_val
        elif cmd.cond == '<=':
            return self.registers[cmd.cond_reg] <= cmd.cond_val
        elif cmd.cond == '>':
            return self.registers[cmd.cond_reg] > cmd.cond_val
        elif cmd.cond == '<':
            return self.registers[cmd.cond_reg] < cmd.cond_val
        else:
            raise ValueError('Unknown condition', cmd)

    def operation(self, cmd):
        if cmd.op == 'inc':
            value = self.registers[cmd.target_reg] + cmd.val
        elif cmd.op == 'dec':
            value = self.registers[cmd.target_reg] - cmd.val
        else:
            raise ValueError('Unknown operation', cmd)
        self.registers[cmd.target_reg] = value
        if value > self.max_value:
            self.max_value = value


def read_data():
    cmds = []
    with open('puzzle08.in', 'r') as f:
        for line in f:
            target_reg, op, val, _if, cond_reg, cond, cond_val = line.strip().split()
            val, cond_val = int(val), int(cond_val)
            cmds.append(Cmd(target_reg, op, val, cond_reg, cond, cond_val))
    return Cpu(cmds)


def part_1():
    cpu = read_data()
    cpu.run()
    return max(cpu.registers.values())


def part_2():
    cpu = read_data()
    cpu.run()
    return cpu.max_value
