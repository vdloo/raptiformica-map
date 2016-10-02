from base64 import b64decode
from json import loads
from os.path import join, dirname, realpath
from urllib import request
from flask import Config

PROJECT_DIR = join(dirname(dirname(dirname(realpath(__file__)))))

app_config = Config(PROJECT_DIR)
app_config.from_pyfile('settings.cfg')

KEY_VALUE_ENDPOINT = app_config.get(
    'CONSUL_KV_ENDPOINT', 'http://localhost:8500/v1/kv/'
)
KEY_VALUE_PATH = app_config.get(
    'CONSUL_KV_PATH', 'raptiformica_map'
)


def put_kv(path, k, v):
    """
    Put a key and value to the distributed key value store at the location path
    :param str path: api path to PUT to
    :param str k: the key to put
    :param str v: the value to put
    :return None:
    """
    encoded = str.encode(str(v))
    url = join(path, k)
    req = request.Request(
        url=url, data=encoded, method='PUT'
    )
    with request.urlopen(req) as f:
        print("PUT k v pair ({}, {}) to {}: {}, {}".format(
            k, v, url, f.status, f.reason
        ))


def get_kv(path, recurse=False):
    """
    Get the key value mapping from the distributed key value store
    :param str path: path to get the value from
    :param bool recurse: whether or not to recurse over the path and
    retrieve all nested values
    :return dict mapping: key value mapping
    """
    req = request.Request(
        url=join(path, '?recurse') if recurse else path,
        method='GET'
    )
    with request.urlopen(req) as r:
        result = loads(r.read().decode('utf-8'))
    mapping = {
        # values are stored base64 encoded in consul, they
        # are decoded before returned by this function.
        r['Key']: b64decode(r['Value']).decode('utf-8') for r in result
    }
    return mapping


def delete_kv(path, recurse=False):
    """
    Delete a key from the distributed key value mapping
    :param str path: path to the key to remove
    :param bool recurse: recurse the path and delete all entries
    :return:
    """
    req = request.Request(
        url=join(path, '?recurse') if recurse else path,
        method='DELETE'
    )
    with request.urlopen(req) as f:
        print("DELETEd key {}{}: {} {}".format(
            path,
            ' recursively' if recurse else '',
            f.status,
            f.reason
        ))


def loop_dict(dictionary, path='/', callback=lambda path, k, v: None):
    """
    Loop the dictionary and perform the callback for each value
    :param dict dictionary: config to loop for values
    :param str path: the depth in the dict joined by /
    :param func callback: the callback to perform for each value
    :return None:
    """
    for k, v in dictionary.items():
        if isinstance(v, dict):
            loop_dict(v, path=join(path, k), callback=callback)
        else:
            callback(path, k, v)


def map_dictionaries(configs):
    """
    Map the dict to the flattened key value associative array
    :param iterable[dict, ..] configs: list of configs to map as key value pairs
    :return dict mapping: key value mapping with config data
    """
    d = dict()
    for config in configs:
        loop_dict(
            config,
            path=join(KEY_VALUE_ENDPOINT, KEY_VALUE_PATH),
            callback=lambda path, k, v: d.update(
                {join(path.replace(KEY_VALUE_ENDPOINT, ''), k): v}
            )
        )
    return d


def upload_dict(mapped):
    """
    Upload a mapped dict to the distributed key value store
    :param iterable[dict, ..] mapped: list of key value pairs
    :return None:
    """
    for key, value in mapped.items():
        put_kv(KEY_VALUE_ENDPOINT, key, value)


def insert_dict(dictionary):
    """
    Insert a dict into the key value store
    :param dict dictionary: the dict to put
    :return None:
    """
    upload_dict(
        map_dictionaries(
            (dictionary,)
        )
    )


def download_dict():
    """
    Get all the stored data from the distributed key value store
    :return dict mapping: all registered key value pairs
    """
    endpoint = join(KEY_VALUE_ENDPOINT, KEY_VALUE_PATH)
    return get_kv(endpoint, recurse=True)
