def read_data():
    with open('puzzle02.in', 'r') as f:
        table = [[int(number) for number in line.strip().split()] for line in f]
        for row in table:
            row.sort(reverse=True)
        return table


def part_1():
    table = read_data()
    return sum(row[0] - row[-1] for row in table)


def checkdiv(row):
    for idx1 in range(len(row) - 1):
        for idx2 in range(idx1 + 1, len(row)):
            if row[idx1] % row[idx2] == 0:
                return row[idx1] // row[idx2]


def part_2():
    table = read_data()
    return sum(checkdiv(row) for row in table)
