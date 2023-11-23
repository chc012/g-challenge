class Edge:
    def __init__(self, capacity, flow, node_from, node_to,
                 reverse_edge):
        self.capacity = capacity
        self.flow = flow
        self.node_from = node_from
        self.node_to = node_to
        self.reverse_edge = reverse_edge

    def __repr__(self):
        return str({
            "capacity": self.capacity,
            "flow": self.flow,
            "node_from": self.node_from,
            "node_to": self.node_to,
        })

def create_edge(capacity, node_from, node_to):
    edge1 = Edge(capacity, 0, node_from, node_to, None)
    edge2 = Edge(0, 0, node_to, node_from, edge1)
    edge1.reverse_edge = edge2
    return edge1, edge2

def create_graph(entrances, exits, path):
    graph = []

    # add all edges
    for from_idx in range(len(path)):
        graph.append([])
        for to_idx in range(len(path[from_idx])):
            capacity = path[from_idx][to_idx]
            if capacity != 0:
                edge1, edge2 = create_edge(capacity, from_idx, to_idx)
                graph[-1].append(edge1)
                graph[-1].append(edge2)

    # create edges to source and target
    source = len(graph)
    graph.append([])
    for entrance in entrances:
        capacity = sum(path[entrance])
        edge1, edge2 = create_edge(capacity, source, entrance)
        graph[-1].append(edge1)
        graph[-1].append(edge2)

    target = len(graph)
    for exit in exits:
        capacity = sum([node[exit] for node in path])
        edge1, edge2 = create_edge(capacity, exit, target)
        graph[exit].append(edge1)
        graph[exit].append(edge2)

    # for completeness, make an empty list for the target node
    graph.append([])

    return graph, source, target

def edmunds_karp(graph, source, target):
    max_flow = 0

    while True:
        queue = []
        queue.append(source)
        links = [None for _ in range(len(graph))]

        # bfs
        while queue and links[target] == None:
            current_node = queue.pop(0)
            for edge in graph[current_node]:
                if (links[edge.node_to] == None
                        and edge.node_to != source
                        and edge.capacity > edge.flow):
                    links[edge.node_to] = edge
                    queue.append(edge.node_to)

        if links[target] != None:
            # find minimum flow in newfound path
            current_node = links[target]
            path = []
            while current_node:
                path.append(current_node)
                current_node = links[current_node.node_from]
            flow = min([edge.capacity - edge.flow for edge in path])

            # Update flow of each edge involved
            for edge in path:
                edge.flow += flow
                edge.reverse_edge.flow -= flow

            max_flow += flow

        else:
            # we exhausted the search
            break

    return max_flow

def solution(entrances, exits, path):
    # Your code here
    graph, source, target = create_graph(entrances, exits, path)
    max_flow = edmunds_karp(graph, source, target)

    return max_flow

if __name__ == "__main__":
    print(solution([0], [3], [[0, 7, 0, 0], [0, 0, 6, 0], [0, 0, 0, 8], [4, 0, 0, 0]]))
    print(solution([0, 1], [4, 5], [[0, 0, 4, 6, 0, 0], [0, 0, 5, 2, 0, 0], [0, 0, 0, 0, 4, 4], [0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]))
