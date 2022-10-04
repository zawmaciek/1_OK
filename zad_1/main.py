import time
from itertools import chain, combinations
from typing import Any
import networkx as nx
import random


def valid_result(graph: Any, group: set[int]) -> bool:
    unconnected_nodes = set(graph.nodes) - group
    connected_nodes = set()
    for node in unconnected_nodes:
        if group & set(graph.successors(node)):
            connected_nodes.add(node)

    return connected_nodes == unconnected_nodes


def get_all_unconnected_groups(graph) -> list[set[int]]:
    def powerset(nodes: list[str]) -> list[set[str]]:
        """
        https://stackoverflow.com/questions/1482308/how-to-get-all-subsets-of-a-set-powerset/1482316#1482316
        powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)
        """
        return [set(subset) for subset in chain.from_iterable(combinations(nodes, r) for r in range(1, len(nodes) + 1))]

    possible_groups = powerset(list(graph.nodes))
    # remove connected groups
    for edge in list(graph.edges):
        edge_set = {edge[0], edge[1]}
        groups_to_remove = list()
        for group in possible_groups:
            if edge_set.issubset(group):
                groups_to_remove.append(group)
        possible_groups = [group for group in possible_groups if group not in groups_to_remove]
    return possible_groups


def solve(graph) -> None:
    possible_groups = get_all_unconnected_groups(graph)

    sorted_possible_groups = sorted(possible_groups, key=lambda x: len(x), reverse=True)

    for group in sorted_possible_groups:
        if valid_result(graph, group):
            print(group)
            break
    else:
        print('not found')


def solve_example() -> None:
    # open file and process
    path = 'ex_1.txt'
    with open(path, 'r') as f:
        graph = nx.drawing.nx_pydot.read_dot(f)
    graph.remove_node('\\n')  # only needed if not formatted correctly
    # remove groups that aren't connected to rest of the nodes
    solve(graph)


def create_random_directed_graph(nodes: int, edges: int):
    G = nx.DiGraph()
    for i in range(nodes):
        G.add_node(str(i))
    e = set()
    for i in range(edges):
        num_1 = random.randint(0, nodes)
        num_2 = random.randint(0, nodes)
        while num_1 == num_2:
            num_2 = random.randint(0, nodes)
        e.add((str(num_1), str(num_2)))
    for s in e:
        G.add_edge(s[0], s[1])
    return G


if __name__ == '__main__':
    # Example
    solve_example()
    # Random
    graph = create_random_directed_graph(10, 100)
    t = time.time()
    solve(graph)
    print(time.time() - t)
