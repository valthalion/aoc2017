def read_data():
    with open('puzzle09.in', 'r') as f:
        return next(f).strip()


def parse_stream(stream):
    score, total_score, garbage_count = 0, 0, 0
    state = 'groups'
    for c in stream:
        if state == 'groups':
            if c == '{':
                score += 1
            elif c == '}':
                total_score += score
                score -= 1
            elif c == '<':
                state = 'garbage'
        elif state == 'garbage':
            if c == '!':
                state = 'ignore'
            elif c == '>':
                state = 'groups'
            else:
                garbage_count += 1
        elif state == 'ignore':
            state = 'garbage'
    return total_score, garbage_count


def part_1():
    total_score, _ = parse_stream(read_data())
    return total_score


def part_2():
    _, garbage_count = parse_stream(read_data())
    return garbage_count
