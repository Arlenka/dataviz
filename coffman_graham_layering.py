__author__ = 'arlen'
from heapq import heappush, heappop


def is_less_internal(s, t):
    if not s and t:
        return True
    if not t:
        return False
    if s[0] > t[0]:  # because labels are negative
        return True
    if heappop(s) == heappop(t) and is_less_internal(s, t):
        return True
    return False


def is_less(s, t):
    return is_less_internal(list(s), list(t))


def assign_labels(graph):
    print("\n---Labeling---")
    current_label = -1  # use negative numbers because of min heap
    labels = {}
    parent_labels = dict(map(lambda n: (n, []), graph.nodes()))
    processing = set()
    for v, d in graph.in_degree():
        if d == 0:
            processing.add(v)
    while processing:
        picked_v = None
        min_set = None
        print('processing:', processing)
        for v in processing:
            print('\tvertex:', v)
            print('\tparent labels:', parent_labels[v])
            if len(parent_labels[v]) != graph.in_degree(v):
                print('\tnot completed')
                continue  # not all parents were processed
            if min_set is None \
                    or is_less(parent_labels[v], min_set):
                min_set = parent_labels[v]
                picked_v = v
        print('labeled:', picked_v, current_label)
        labels[picked_v] = -current_label
        for e in graph.out_edges(picked_v):
            print('push parent label to:', e[1], current_label)
            heappush(parent_labels[e[1]], current_label)
            processing.add(e[1])
        current_label -= 1
        processing.remove(picked_v)
    print("labels:", labels)
    print("---Labeling end---\n")
    return labels


def do_layering(graph, max_width, labels):
    print("\n---Layering---")
    processed = set()
    layers, layer_k = [], []
    k = 0
    layer_labels = {}

    processing = set()
    for v, d in graph.out_degree():
        if d == 0:
            processing.add(v)
    while processing:
        picked_v = None
        max_label = None
        save_same_layer = False
        print('processing:', processing)
        for v in processing:
            print('\tvertex:', v)
            print('\tlabel:', labels[v])
            all_adj_nodes_processed = True
            all_adj_nodes_not_in_same_layer = True

            for e in graph.out_edges(v):
                if not e[1] in processed:
                    all_adj_nodes_processed = False
                    break
                if layer_labels[e[1]] == k:
                    all_adj_nodes_not_in_same_layer = False

            if not all_adj_nodes_processed:
                print('\tnot completed')
                continue

            if max_label is None or labels[v] > max_label:
                max_label = labels[v]
                picked_v = v
                save_same_layer = all_adj_nodes_not_in_same_layer
        print('picked:', picked_v)

        if len(layer_k) < max_width and save_same_layer:
            print('add to layer №', len(layers))
            layer_k.append(picked_v)
        else:
            layers.append(layer_k)
            k += 1
            print('add to layer №', len(layers))
            layer_k = [picked_v]
        layer_labels[picked_v] = k
        for e in graph.in_edges(picked_v):
            print('add to processing:', e[0])
            processing.add(e[0])
        processing.remove(picked_v)
        processed.add(picked_v)
    layers.append(layer_k)
    print("layers:", layers)
    print("---Layering end---\n")
    return layers, layer_labels