from raptiformica_map.database.consul.models import NodeDB as consul_NodeDB
from raptiformica_map.database.mysql.models import NodeDB as mysql_NodeDB


def get_node_db_driver(config):
    """
    Get a NodeDB database object
    :obj config: Flask config object
    :param dict config: database config
    :return class NodeDB: NodeDB ORM object for
    the configured database backend
    """
    backend = config.get('DATABASE_BACKEND')
    if backend == 'consul':
        return consul_NodeDB(config)
    else:
        return mysql_NodeDB(config)
