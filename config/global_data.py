import os, yaml
from pathlib import Path
from loguru import logger

CONFIG_LOADED=False


def get_env_config():
    global ENV
    global CONFIG
    global CONFIG_LOADED

    if CONFIG_LOADED:
        return CONFIG

    ENV = os.environ.get('ENV') or "local"

    config_file = Path("config/config.yaml")
    with open(config_file, 'r') as config:
        try:
            CONFIG = yaml.safe_load(config).get(ENV)
            logger.info("Environment config file successfully loaded.")
            logger.debug(CONFIG)
            CONFIG_LOADED=True
        except (yaml.YAMLError, Exception) as e:
            CONFIG=None
            logger.error("Failed to load environment config.")
            logger.error(e)
    return CONFIG


def get_config_val(*args):
    config = get_env_config()
    for arg in args:
        config = config.get(arg)
    return config


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_env_config())