from typing import (
    List,
    Optional,
    Set,
    Tuple,
)


def get_input_data() -> Tuple[List[List[int]], Set[int]]:
    """Возвращает существующие ссылки между узлами сети и номера узлов, являющихся выходными шлюзами.
    Нумерация узлов начинается с нуля, перемещаться между узлами можно в обоих направлениях.
    """
    _, links_n, exits_n = [int(i) for i in input().split()]
    links, exits = [], set()
    for _ in range(links_n):
        links.append([int(j) for j in input().split()])
    for _ in range(exits_n):
        exits.add(int(input()))

    return links, exits


def get_graph_repr(edges: List[List[int]]) -> dict:
    """Возвращает представление графа в виде словаря.
    Ключами словаря являются вершины графа, значениями - достижимые вершины.
    """
    def add_edge(i, j, gr):
        if i in gr:
            gr[i].add(j)
        else:
            gr[i] = {j}

    graph = {}
    for edge in edges:
        add_edge(*edge, graph)
        add_edge(*edge[::-1], graph)
    return graph


def get_edge_to_marked_vertex(graph, marked_vertexes) -> Optional[Tuple[int, int]]:
    """Возвращает ребро до размеченной вершины графа, если такое существует."""
    existing_marked_vertexes = marked_vertexes & graph.keys()
    if not existing_marked_vertexes:
        return None
    v1 = existing_marked_vertexes.pop()
    v2 = next(iter(graph[v1]))
    return v1, v2


def get_edge_to_delete(vertex: int, graph: dict, marked_vertexes: Set[int]) -> Optional[Tuple[int, int]]:
    """Возвращает ребро графа.
    Если из вершины vertex существует ребро до одной из вершин marked_vertexes, то оно будет возвращено.
    Если такого ребра нет, будет возвращено любое ребро в одну из вершин marked_vertexes. Если и таких
    ребер нет, то будет возвращено любое ребро из вершины vertex.
    Если ребер из вершины vertex не существует, будет возвращено None.
    """
    neighbors = graph.get(vertex)
    if not neighbors:
        return

    marked_neighbors = neighbors & marked_vertexes
    if marked_neighbors:
        return vertex, marked_neighbors.pop()
    else:
        edge_to_marked_vertex = get_edge_to_marked_vertex(graph, marked_vertexes)
        if edge_to_marked_vertex:
            return edge_to_marked_vertex
        else:
            return vertex, next(iter(neighbors))


def delete_edge_from_graph(edge: Tuple[int, int], graph: dict) -> None:
    """Удаляет ребро графа."""
    i, j = edge
    graph[i].remove(j)
    graph[j].remove(i)


def destroy_link(node: int, network_repr: dict, exit_nodes: Set[int]) -> Tuple[int, int]:
    """Уничтожает связи между узлами сети."""
    link_to_destroy = get_edge_to_delete(node, network_repr, exit_nodes)
    if not link_to_destroy:
        raise Exception('No links related with node %s' % node)
    delete_edge_from_graph(link_to_destroy, network_repr)
    return link_to_destroy


if __name__ == '__main__':
    links, exits = get_input_data()
    network = get_graph_repr(links)
    while True:
        node = int(input())
        print(*destroy_link(node, network, exits))