import json
from contextlib import suppress

from raptiformica_map.database import get_node_db_driver
from raptiformica_map.graph import Node, Edge
import traceback
import time


def insert_graph_data(config, data, ip, version):
    try:
        graph_data = json.loads(data)
    except ValueError:
        return 'Invalid JSON'

    log = '[{}] ip: {}, version: {}, nodes: {}, edges: {}'.format(
        time.strftime('%Y-%m-%d %H:%M:%S'),
        ip,
        version,
        len(graph_data['nodes']),
        len(graph_data['edges'])
    )

    with open(config['LOG'], 'a') as f:
        f.write(log + '\n')

    nodes = dict()
    edges = []

    for n in graph_data['nodes']:
        with suppress(ValueError, KeyError):
            node = Node(n['ip'], version=n['version'])
            nodes[n['ip']] = node

    for e in graph_data['edges']:
        with suppress(ValueError, KeyError):
            edge = Edge(nodes[e['a']], nodes[e['b']])
            edges.append(edge)

    print("Accepted {} nodes and {} links.".format(len(nodes), len(edges)))

    if len(nodes) == 0 or len(edges) == 0:
        return 'No valid nodes or edges'

    uploaded_by = ip

    try:
        with get_node_db_driver(config) as db:
            db.insert_graph(nodes, edges, uploaded_by)
    except Exception:
        traceback.print_exc()
        return 'Database failure'

    return None
