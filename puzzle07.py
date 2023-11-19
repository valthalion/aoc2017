from collections import Counter


def read_data():
    nodes = {}
    leafs = set()
    with open('puzzle07.in', 'r') as f:
        for line in f:
            node_spec = line.strip().split(' -> ')
            name, weight = node_spec[0][:-1].split(' (')
            nodes[name] = {'weight': int(weight), 'children': None}
            if len(node_spec) == 1:
                leafs.add(name)
                continue
            nodes[name]['children'] = set(node_spec[1].split(', '))
    potential_heads = set(nodes) - leafs
    potential_heads -= set(child for name in potential_heads for child in nodes[name]['children'])
    nodes['head'] = potential_heads.pop()
    return nodes


def part_1():
    tree = read_data()
    return tree['head']


def tree_weight(tree, node_name='head'):
    if node_name == 'head':
        node_name = tree['head']
    node = tree[node_name]
    if node['children'] is None:
        node['total_weight'] = node['weight']
    else:
        node['total_weight'] = node['weight'] + sum(tree_weight(tree, node_name=child) for child in node['children'])
    return node['total_weight']


def balance_node(tree, node_name='head', target=None):
    if node_name == 'head':
        node_name = tree['head']
    node = tree[node_name]
    if node['children'] is None:
        raise RuntimeError
    children_weights = Counter(tree[child]['total_weight'] for child in node['children'])
    target_weight, count = children_weights.most_common(1)[0]
    if count == len(node['children']):  # All equal, this is the problem node, target should be set
        return node_name, target - target_weight * count
    for child in node['children']:
        if tree[child]['total_weight'] == target_weight:
            continue
        return balance_node(tree, node_name=child, target=target_weight)


def part_2():
    tree = read_data()
    tree_weight(tree)
    node, new_weight = balance_node(tree)
    return new_weight
