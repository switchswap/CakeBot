from .exceptions import ConfigKeyNotFoundException
from typing import TypeVar
import config

T = TypeVar('T')


def load_key(key: str, type_hint: T):
    """
    Load a key from config file

    Parameters
    ----------
    key : Name of config key to load
    type_hint : The typing of the config key
    """
    if hasattr(config, key):
        return getattr(config, key)

    error = f"{key} ({type_hint}) not found in config file!"
    raise ConfigKeyNotFoundException(error)
