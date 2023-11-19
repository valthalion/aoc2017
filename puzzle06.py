def read_data():
    with open('puzzle06.in', 'r') as f:
        return [int(number) for number in next(f).strip().split()]


def cycle(memory):
    max_bank, max_blocks = -1, -1
    for bank, blocks in enumerate(memory):
        if blocks > max_blocks:
            max_bank, max_blocks = bank, blocks

    blocks_to_move = max_blocks
    memory[max_bank] = 0
    global_increment, remainder = divmod(blocks_to_move, len(memory))
    if global_increment:
        for bank in range(len(memory)):
            memory[bank] += global_increment
    bank = max_bank
    for _ in range(remainder):
        bank += 1
        if bank == len(memory):
            bank = 0
        memory[bank] += 1


def part_1():
    memory = read_data()
    seen = set()
    cycles = 0
    seen.add(tuple(memory))

    while True:
        cycle(memory)
        cycles += 1
        new_config = tuple(memory)
        if new_config in seen:
            return cycles
        seen.add(new_config)


def part_2():
    memory = read_data()
    seen = {}
    cycles = 0
    seen[tuple(memory)] = cycles

    while True:
        cycle(memory)
        cycles += 1
        new_config = tuple(memory)
        if new_config in seen:
            return cycles - seen[new_config]
        seen[new_config] = cycles
