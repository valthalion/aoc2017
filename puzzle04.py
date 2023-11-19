from collections import Counter


def read_data():
    with open('puzzle04.in', 'r') as f:
        for line in f:
            yield line.strip().split()


def part_1():
    return sum(1 for passphrase in read_data() if len(passphrase) == len(set(passphrase)))


def specs(passphrase):
    for password in passphrase:
        spec = list(Counter(password).items())
        spec.sort()
        yield tuple(spec)


def part_2():
    return sum(1 for passphrase in read_data() if len(passphrase) == len(set(specs(passphrase))))
