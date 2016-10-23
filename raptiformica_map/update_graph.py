#!/usr/bin/env python
from flask import Config
from os.path import join, dirname, realpath
from raptiformica_map.database import get_node_db_driver
from raptiformica_map import graph_plotter

GRAPH_FILE = 'static/graph.json'
PROJECT_DIR = join(dirname(realpath(__file__)))
NODE_TIME_LIMIT = 60 * 60 * 3  # 3 hours
EDGE_TIME_LIMIT = 60 * 60 * 24 * 7  # 7 days


def generate_graph(time_limit=NODE_TIME_LIMIT):
    nodes, edges = load_graph_from_db(time_limit)
    print('{} nodes, {} edges'.format(len(nodes), len(edges)))

    graph = graph_plotter.position_nodes(nodes, edges)
    json = graph_plotter.get_graph_json(graph)

    graph_path = join(PROJECT_DIR, GRAPH_FILE)
    with open(graph_path, 'w+') as f:
        f.write(json)


def load_graph_from_db(time_limit):
    config = Config(PROJECT_DIR)
    config.from_pyfile('settings.cfg')

    with get_node_db_driver(config) as db:
        nodes = db.get_nodes(time_limit)
        edges = db.get_edges(nodes, EDGE_TIME_LIMIT)
        return nodes, edges


if __name__ == '__main__':
    generate_graph()
