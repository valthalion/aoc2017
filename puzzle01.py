def read_data():
    with open('puzzle01.in', 'r') as f:
        return [int(digit) for digit in next(f).strip()]


def part_1():
    digits = read_data()
    total = sum(digit1 for digit1, digit2 in zip(digits, digits[1:]) if digit1 == digit2)
    if digits[-1] == digits[0]:
        total += digits[0]
    return total


def part_2():
    digits1 = read_data()
    halfpoint = len(digits1) // 2
    digits2 = digits1[halfpoint:] + digits1[:halfpoint]
    return sum(digit1 for digit1, digit2 in zip(digits1, digits2) if digit1 == digit2)
