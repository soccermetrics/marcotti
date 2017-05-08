import os
import json
import logging
import logging.config


def setup_logging(settings_path="logging.json", default_level=logging.INFO):
    """Setup logging configuration"""
    path = settings_path
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
