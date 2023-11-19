def read_data():
    with open('puzzle05.in', 'r') as f:
        return [int(line.strip()) for line in f]


def part_1():
    memory = read_data()
    pc, jumps = 0, 0
    max_address = len(memory)
    while 0 <= pc < max_address:
        offset = memory[pc]
        memory[pc] += 1
        pc += offset
        jumps += 1
    return jumps


def part_2():
    memory = read_data()
    pc, jumps = 0, 0
    max_address = len(memory)
    while 0 <= pc < max_address:
        offset = memory[pc]
        memory[pc] += 1 if offset < 3 else -1
        pc += offset
        jumps += 1
    return jumps
