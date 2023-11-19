from math import sqrt

from puzzle18 import convert, Program


def read_data():
    filename = 'puzzle23.in'
    cmds = []
    with open(filename, 'r') as f:
        for line in f:
            cmd, *args = line.strip().split()
            cmds.append((cmd, tuple(convert(arg) for arg in args)))
    return cmds


def primes(up_to):
    primes_known = [3, 5, 7, 11, 13, 17, 19, 23, 29]
    current = 31
    while current < up_to:
        is_prime = True
        limit = int(sqrt(current)) + 1
        for p in primes_known:
            if p > limit:
                break
            if current % p == 0:
                is_prime = False
                break
        if is_prime:
            primes_known.append(current)
        current += 2
    return set(primes_known)


def part_1():
    program = Program(read_data(), pid=0, send_to=None)
    output, muls = program.run(debug=True)
    return muls


def part_2():
    b = 67 * 100 + 100_000
    c = b + 17_000
    all_primes = primes(up_to=c)
    return sum(1 for n in range(b, c + 1, 17) if n not in all_primes)
