from collections import defaultdict


def read_data():
    graph = defaultdict(set)
    with open('puzzle12.in', 'r') as f:
        for line in f:
            orig, dests = line.strip().split(' <-> ')
            orig = int(orig)
            dests = [int(n) for n in dests.split(', ')]
            for dest in dests:
                graph[orig].add(dest)
                graph[dest].add(orig)
    return graph


def connected_components(graph):
    nodes = set(graph.keys())
    queue = set()

    while nodes:
        component = set()
        queue.add(nodes.pop())
        while queue:
            node = queue.pop()
            neighbours = graph[node] & nodes
            nodes -= neighbours
            queue |= neighbours
            component.add(node)
        yield component


def part_1():
    graph = read_data()
    for component in connected_components(graph):
        if 0 in component:
            return len(component)


def part_2():
    graph = read_data()
    return sum(1 for component in connected_components(graph))
