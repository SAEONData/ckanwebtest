import pkg_resources

__version__ = pkg_resources.require('ckanwebtest')[0].version

CONFIG_FILENAME = pkg_resources.resource_filename(__name__, '../server.ini')


def load_template(filename):
    return pkg_resources.resource_string(__name__, 'templates/' + filename).decode('utf-8')
