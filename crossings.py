__author__ = 'arlen'
import itertools
import random


def add_dummy_vertices(graph, layers, layer_labels):
    print("\n---Dummying---")
    new_edges = []
    edges_to_remove = []
    dummy_index = 0
    for edge in graph.edges():
        layer_out = layer_labels[edge[0]]
        layer_in = layer_labels[edge[1]]

        if layer_out != layer_in + 1:
            print('add dummy vertices for: {} layer {} -> {} layer {}'.format(edge[0], layer_out, edge[1], layer_in))
            new_dummy = "dummy" + str(dummy_index)
            curr_vertex = edge[0]
            for i in range(layer_out - layer_in - 1):
                print('\tadd edge: {} -> {}'.format(curr_vertex, new_dummy))
                new_edges.append((curr_vertex, new_dummy))

                dummy_layer = layer_out - i - 1
                print('\tadd vertex {} to layer {}'.format(new_dummy, dummy_layer))
                layer_labels[new_dummy] = dummy_layer
                layers[dummy_layer].append(new_dummy)

                curr_vertex = new_dummy
                dummy_index += 1
                new_dummy = "dummy" + str(dummy_index)

            print('\tadd edge: {} -> {}'.format(curr_vertex, edge[1]))
            new_edges.append((curr_vertex, edge[1]))
            edges_to_remove.append(edge)

    graph.add_edges_from(new_edges)
    graph.remove_edges_from(edges_to_remove)
    print("layers after adding dummy vertices:", layers)
    print("---Dummying end---\n")
    return edges_to_remove


def compute_crossing_matrix(graph, layer_down, layer_up, x_down):
    crossing_matrix = dict(dict())

    for u in layer_up:
        crossing_matrix[u] = {}
        for v in layer_up:
            crossing_matrix[u][v] = 0

    for w, z in itertools.combinations(layer_down, 2):
        for edge_to_w in graph.in_edges(w):
            for edge_to_z in graph.in_edges(z):
                u = edge_to_w[0]
                v = edge_to_z[0]
                if u != v:
                    if x_down[w] < x_down[z]:
                        crossing_matrix[v][u] += 1
                    elif x_down[z] < x_down[w]:
                        crossing_matrix[u][v] += 1

    return crossing_matrix


def split(graph, vertices, crossing_matrix):
    if len(vertices) <= 1:
        return vertices

    p = random.choice(vertices)
    vertices_left, vertices_right = [], []

    for q in vertices:
        if q != p:
            if crossing_matrix[q][p] <= crossing_matrix[p][q]:
                vertices_left.append(q)
            else:
                vertices_right.append(q)

    out_left = split(graph, vertices_left, crossing_matrix)
    out_right = split(graph, vertices_right, crossing_matrix)

    return out_left + [p] + out_right


def reduce_crossings(graph, layers):
    print("\n---Reducing crossings---")
    new_layers = [layers[0]]
    x_down = {el: i for (i, el) in enumerate(layers[0])}

    for i, layer in enumerate(layers[1:]):
        layer_down = layers[i]
        crossing_matrix = compute_crossing_matrix(graph, layer_down, layer, x_down)
        layer_order = split(graph, layer, crossing_matrix)
        x_down = {el: j for (j, el) in enumerate(layer_order)}
        new_layers.append(layer_order)

    print('layers after reducing crossings:', new_layers)
    print("---Reducing crossings end---\n")
    return new_layers

