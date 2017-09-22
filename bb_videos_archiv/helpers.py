import configparser
import os


def get_default_config():
    """Return the default config."""
    default_config = configparser.ConfigParser()
    path_config = os.path.join(os.path.dirname(__file__), 'default_config.ini')
    default_config.read(path_config)
    return default_config
