testing = False


def read_data():
    filename = 'puzzle24_test.in' if testing else 'puzzle24.in'
    with open(filename, 'r') as f:
        return frozenset(tuple(int(n) for n in line.strip().split('/')) for line in f)


def build_bridge(connectors, start_connector=0, acc=(tuple(), (0, 0)), maximize_len=True):
    options = frozenset(connector for connector in connectors if start_connector in connector)
    if not options:
        return acc

    base_path, best_metric = acc
    if maximize_len:
        base_length, base_strength = best_metric
    else:
        base_strength, base_length = best_metric
    best_path = None
    new_length = base_length + 1

    for connector in options:
        remaining_connector = connector[1] if connector[0] == start_connector else connector[0]
        new_strength = base_strength + sum(connector)
        new_metric = (new_length, new_strength) if maximize_len else (new_strength, new_length)
        path, metric = build_bridge(connectors=connectors - {connector},
                                    start_connector=remaining_connector,
                                    acc=((*base_path, connector), new_metric),
                                    maximize_len=maximize_len
                                   )
        if metric > best_metric:
            best_path, best_metric = path, metric
    return best_path, best_metric


def part_1():
    nodes = read_data()
    bridge, (strength, length) = build_bridge(nodes, maximize_len=False)
    return strength


def part_2():
    nodes = read_data()
    bridge, (length, strength) = build_bridge(nodes, maximize_len=True)
    return strength
