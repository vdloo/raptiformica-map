import time
from hashlib import md5
from contextlib import suppress
from urllib.error import HTTPError

from raptiformica_map.database.consul.serializer import insert_dict, download_dict, KEY_VALUE_PATH
from raptiformica_map.graph import Node, Edge
from raptiformica_map.utils import startswith


class NodeDB(object):

    def __init__(self, config):
        pass

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @staticmethod
    def encode_edge_ip_pair(from_ip, to_ip):
        hashed = md5("{},{}".format(from_ip, to_ip).encode('utf-8'))
        return hashed.hexdigest()

    @staticmethod
    def select_from_key_value(table, identifier):
        data = download_dict()
        key_path = '{}/{}/{}/'.format(
            KEY_VALUE_PATH, table, identifier
        )
        items = map(
            lambda x: x.split('/')[3],
            filter(
                startswith(key_path),
                data
            )
        )
        return {k: data[key_path + k] for k in items}

    def get_node_by_ip(self, ip):
        with suppress(HTTPError):
            return self.select_from_key_value(
                'nodes',
                ip
            )

    def get_edge_by_ips(self, from_ip, to_ip):
        with suppress(HTTPError):
            return self.select_from_key_value(
                'edges',
                self.encode_edge_ip_pair(from_ip, to_ip)
            )

    def insert_node(self, node):
        now = int(time.time())
        previous_data = self.get_node_by_ip(node.ip) or {}
        previous_time = previous_data.get('first_seen', now)
        node_information = {
            'nodes': {
                node.ip: {
                    'ip': node.ip,
                    'name': node.label,
                    'version': node.version,
                    'first_seen': previous_time or now,
                    'last_seen': now,
                }
            }
        }
        insert_dict(node_information)

    def insert_edge(self, edge, uploaded_by):
        now = int(time.time())
        previous_data = self.get_edge_by_ips(edge.a.ip, edge.b.ip) or {}
        previous_time = previous_data.get('first_seen', now)

        edge_information = {
            'edges': {
                self.encode_edge_ip_pair(edge.a.ip, edge.b.ip): {
                    'from_ip': edge.a.ip,
                    'to_ip': edge.b.ip,
                    'first_seen': previous_time,
                    'last_seen': now,
                    'uploaded_by': uploaded_by
                }
            }
        }
        insert_dict(edge_information)

    def insert_graph(self, nodes, edges, uploaded_by):
        for n in nodes.values():
            self.insert_node(n)

        for e in edges:
            self.insert_edge(e, uploaded_by)

    @staticmethod
    def get_nodes(time_limit):
        data = download_dict()
        key_path = '{}/{}/'.format(
            KEY_VALUE_PATH, 'nodes'
        )
        ips = set(map(
            lambda x: x.split('/')[2],
            filter(
                startswith(key_path),
                data
            )
        ))

        nodes = dict()
        since = int(time.time() - time_limit)
        for ip in ips:
            if int(data[key_path + ip + "/last_seen"]) > since:
                nodes[ip] = Node(
                    ip,
                    data[key_path + ip + "/version"],
                    data[key_path + ip + "/name"],
                )
        return nodes

    @staticmethod
    def get_edges(nodes, time_limit):
        data = download_dict()
        key_path = '{}/{}/'.format(
            KEY_VALUE_PATH, 'edges'
        )
        ip_pair_hashes = set(map(
            lambda x: x.split('/')[2],
            filter(
                startswith(key_path),
                data
            )
        ))

        edges = list()
        since = int(time.time() - time_limit)
        for ip_pair_hash in ip_pair_hashes:
            if int(data[key_path + ip_pair_hash + "/last_seen"]) > since:
                edges.append(
                    Edge(
                        nodes[data[key_path + ip_pair_hash + "/from_ip"]],
                        nodes[data[key_path + ip_pair_hash + "/to_ip"]]
                    )
                )
        return edges

    def get_graph(self, time_limit):
        nodes = self.get_nodes(time_limit)
        edges = self.get_edges(nodes, time_limit)
        return nodes, edges
