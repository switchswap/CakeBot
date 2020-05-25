from .exceptions import ConfigKeyNotFoundException
import config


def load_key(key, type_hint):
    if hasattr(config, key):
        return getattr(config, key)
    else:
        error = f"{key} ({type_hint}) not found in config file!"
        raise ConfigKeyNotFoundException(error)
