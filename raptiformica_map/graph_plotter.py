import pygraphviz as pgv
import time
import json
import networkx as nx
from networkx.algorithms import centrality

from raptiformica_map.utils import load_json


def position_nodes(nodes, edges):
    graph = pgv.AGraph(strict=True, directed=False, size='10!')

    for n in nodes.values():
        graph.add_node(n.ip, label=n.label, version=n.version)

    for e in edges:
        graph.add_edge(e.a.ip, e.b.ip, len=1.0)

    graph.layout(
        prog='neato',
        args='-Gepsilon=0.0001 -Gmaxiter=100000'
    )

    return graph


def compute_betweenness(G):
    ng = nx.Graph()
    for start in G.iternodes():
        others = G.neighbors(start)
        for other in others:
            ng.add_edge(start, other)

    c = centrality.betweenness_centrality(ng)

    for k, v in c.items():
        c[k] = v

    return c


def canonalize_ip(ip):
    return ':'.join(i.rjust(4, '0') for i in ip.split(':'))


def load_db():
    with open('nodes', 'w+') as f:
        return dict(
            [(canonalize_ip(v[0]), v[1]) for v in
             [l.split(None)[:2] for l in f.readlines()]
             if len(v) > 1]
        )


def strip_leading_zeroes(ipv6_address):
    """
    Sometimes ipv6 addresses are stored without leaving zeroes in the segments.
    To make sure we get the right matches when comparing addresses, always
    strip zeroes
    :param str ipv6_address: the ipv6 address to strip zeroes from
    :return str stripped_ipv6_address: The stripped ipv6 address
    """
    if ipv6_address[0] == '0':
        ipv6_address = ipv6_address[1:]
    return ipv6_address.replace(':0', ':')


def get_graph_json(G):
    max_neighbors = 1
    for n in G.iternodes():
        neighbors = len(G.neighbors(n))
        if neighbors > max_neighbors:
            max_neighbors = neighbors
    print('Max neighbors: {}'.format(max_neighbors or 0))

    out_data = {
        'created': int(time.time()),
        'nodes': [],
        'edges': []
    }

    centralities = compute_betweenness(G)
    db = load_db()

    own_ipv6_address = load_json('/etc/cjdroute.conf')['ipv6']

    for n in G.iternodes():
        neighbor_ratio = len(G.neighbors(n)) / float(max_neighbors)
        pos = n.attr['pos'].split(',', 1)
        centrality = centralities.get(n.name, 0)
        pcentrality = (centrality + 0.0001) * 500
        size = (pcentrality ** 0.3 / 500) * 1000 + 1
        name = db.get(n.name)

        out_data['nodes'].append({
            'id': n.name,
            'label': name if name else n.attr['label'],
            'name': name,
            'version': n.attr['version'],
            'x': float(pos[0]),
            'y': float(pos[1]),
            'color': _gradient_color(
                neighbor_ratio, [(100, 100, 100), (0, 0, 0)]
            ),
            'size': size,
            'centrality': '%.4f' % centrality,
            'is_self': strip_leading_zeroes(n.name) == strip_leading_zeroes(own_ipv6_address),
        })

    for e in G.iteredges():
        out_data['edges'].append({
            'sourceID': e[0],
            'targetID': e[1]
        })

    return json.dumps(out_data)


def _gradient_color(ratio, colors):
    jump = 1.0 / (len(colors) - 1)
    gap_num = int(ratio / (jump + 0.0000001))

    a = colors[gap_num]
    b = colors[gap_num + 1]

    ratio = (ratio - gap_num * jump) * (len(colors) - 1)

    r = a[0] + (b[0] - a[0]) * ratio
    g = a[1] + (b[1] - a[1]) * ratio
    b = a[2] + (b[2] - a[2]) * ratio

    return '#{:02X}{:02X}{:02X}'.format(*map(int, (r, g, b)))
