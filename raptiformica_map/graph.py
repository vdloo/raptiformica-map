import re

CJDNS_IP_REGEX = re.compile(r'^fc[0-9a-f]{2}(:[0-9a-f]{4}){7}$', re.IGNORECASE)


class Node(object):

    def __init__(self, ip, version=None, label=None):
        if not valid_cjdns_ip(ip):
            raise ValueError('Invalid IP address')
        if not valid_version(version):
            raise ValueError('Invalid version')

        self.ip = ip
        self.version = int(version)
        self.label = ip[-4:] or label

    def __lt__(self, b):
        return self.ip < b.ip

    def __repr__(self):
        return 'Node(ip="%s", version=%s, label="%s")' % (
            self.ip,
            self.version,
            self.label)


class Edge(object):

    def __init__(self, a, b):
        self.a, self.b = sorted([a, b])

    def __eq__(self, that):
        return self.a.ip == that.a.ip and self.b.ip == that.b.ip

    def __repr__(self):
        return 'Edge(a.ip="{}", b.ip="{}")'.format(self.a.ip, self.b.ip)


def valid_cjdns_ip(ip):
    return CJDNS_IP_REGEX.match(ip)


def valid_version(version):
    try:
        return int(version) < 30
    except ValueError:
        return False
