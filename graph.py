__author__ = 'arlen'

import os
import argparse

import networkx as nx

import crossings
import coffman_graham_layering


OUTPUTS_DIR = 'outputs'


def draw(graph, filename):
    converted_graph = nx.nx_agraph.to_agraph(graph)
    converted_graph.graph_attr['overlap'] = 'scale'
    converted_graph.layout(prog='fdp', args='-n')
    if not os.path.exists(OUTPUTS_DIR):
        os.mkdir(OUTPUTS_DIR)
    filepath = os.path.join(OUTPUTS_DIR, filename + '.png')
    converted_graph.draw(filepath)
    print('draw to file: {}'.format(filepath))


def draw_by_layers(graph, layers, filename, replace_dummies=False):
    node_attrs = {}
    edge_attrs = {}

    for y, layer in enumerate(layers):
        for x, v in enumerate(layer):
            node_attrs[v] = {'pos': '{},{}!'.format(x, y)}
            if replace_dummies and v.startswith('dummy'):
                node_attrs[v]['shape'] = 'point'
                for edge in graph.in_edges(v):
                    edge_attrs[edge] = {'arrowhead': 'none'}

    nx.set_node_attributes(graph, node_attrs)
    if edge_attrs:
        nx.set_edge_attributes(graph, edge_attrs)

    draw(graph, filename)


def process_graph(graph, max_width=3):
    if not nx.is_directed_acyclic_graph(graph):
        print('Cyclic graph not supported!')
        exit(1)

    labels = coffman_graham_layering.assign_labels(graph)

    layers, y_labels = coffman_graham_layering.do_layering(graph, max_width, labels)
    draw_by_layers(graph, layers, 'after_layering')

    crossings.add_dummy_vertices(graph, layers, y_labels)
    draw_by_layers(graph, layers, 'after_adding_dummy')

    after_reducing_layers = crossings.reduce_crossings(graph, layers)
    draw_by_layers(graph, after_reducing_layers, 'after_reducing', replace_dummies=True)


def get_sample_graph():
    sample_graph = nx.DiGraph()
    edges = [('b', 'd'), ('b', 'm'), ('m', 'k'), ('m', 'c'), ('d', 'c'), ('m', 'e'),
             ('d', 'n'), ('d', 'f'), ('m', 'l'), ('n', 'l'), ('l', 'i'), ('f', 'i'),
             ('c', 'f'), ('f', 'r'), ('e', 'r'), ('r', 'p'), ('i', 'p')]
    sample_graph.add_edges_from(edges)
    sample_graph.add_node('a')
    return sample_graph


def read_graph(filename):
    graph = nx.DiGraph()
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip('\n').strip()
            if line:
                edge = line.split(' ')
                if len(edge) == 1:
                    graph.add_node(edge[0])
                elif len(edge) == 2:
                    graph.add_edge(edge[0], edge[1])
                else:
                    print('Can\'t parse line {}. It will be ignored'.format(line))
    return graph


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', help='Input file with graph.')
    args = parser.parse_args()

    if not args.file:
        graph = get_sample_graph()
    else:
        graph = read_graph(args.file)

    draw(graph, 'init_graph')
    process_graph(graph)


if __name__ == "__main__":
    main()
