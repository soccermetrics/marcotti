import os
import glob
import json
import logging


logger = logging.getLogger(__name__)


def extract(func):
    """
    Decorator function. Open and extract data from JSON files.  Return list of dictionaries.

    :param func: Wrapped function with *args and **kwargs arguments.
    """
    def _wrapper(*args):
        out = []
        instance, prefix = args
        for fname in glob.glob(os.path.join(getattr(instance, 'directory'), *prefix)):
            with open(fname) as g:
                out.extend(func(instance, data=json.load(g)))
        return out
    return _wrapper


class BaseJSON(object):
    def __init__(self, directory):
        self.directory = directory
