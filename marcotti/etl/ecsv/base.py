import os
import csv
import glob
import logging


logger = logging.getLogger(__name__)


def extract(func):
    """
    Decorator function. Open and extract data from CSV files.  Return list of dictionaries.

    :param func: Wrapped function with *args and **kwargs arguments.
    """
    def _wrapper(*args):
        out = []
        instance, prefix = args
        for fname in glob.glob(os.path.join(getattr(instance, 'directory'), *prefix)):
            with open(fname) as g:
                out.extend(func(instance, data=csv.DictReader(g)))
        return out
    return _wrapper


class BaseCSV(object):
    def __init__(self, directory):
        self.directory = directory

    @staticmethod
    def column(field, **kwargs):
        try:
            value = kwargs[field].strip()
            return value if value != "" else None
        except (AttributeError, KeyError, TypeError) as ex:
            return None

    def column_unicode(self, field, **kwargs):
        try:
            return self.column(field, **kwargs).decode('utf-8')
        except (KeyError, AttributeError):
            return None

    def column_int(self, field, **kwargs):
        try:
            return int(self.column(field, **kwargs))
        except (KeyError, TypeError):
            return None

    def column_bool(self, field, **kwargs):
        try:
            return bool(self.column_int(field, **kwargs))
        except (KeyError, TypeError):
            return None

    def column_float(self, field, **kwargs):
        try:
            return float(self.column(field, **kwargs))
        except (KeyError, TypeError):
            return None

