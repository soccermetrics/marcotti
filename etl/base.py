import os
import csv
import glob
import json

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound


class BaseIngest(object):

    def __init__(self, session):
        self.session = session

    def get_id(self, model, **conditions):

        try:
            record_id = self.session.query(model).filter_by(**conditions).one().id
        except NoResultFound:
            print "{} has no records in Marcotti database for: {}".format(model.__name__, conditions)
            return None
        except MultipleResultsFound:
            print "{} has multiple records in Marcotti database for: {}".format(model.__name__, conditions)
            return None
        return record_id

    def record_exists(self, model, **conditions):
        return self.session.query(model).filter_by(**conditions).count() != 0

    def load_feed(self, handle):
        raise NotImplementedError


class BaseCSV(BaseIngest):

    def load_feed(self, handle):
        rows = csv.DictReader(handle)
        self.parse_file(rows)

    @staticmethod
    def column(field, **kwargs):
        try:
            value = kwargs[field].strip()
            return value if value != "" else None
        except (AttributeError, TypeError) as ex:
            raise ex

    def column_unicode(self, field, **kwargs):
        try:
            return self.column(field, **kwargs).decode('utf-8')
        except AttributeError:
            return None

    def column_int(self, field, **kwargs):
        try:
            return int(self.column(field, **kwargs))
        except TypeError:
            return None

    def column_bool(self, field, **kwargs):
        try:
            return bool(self.column_int(field, **kwargs))
        except TypeError:
            return None

    def column_float(self, field, **kwargs):
        try:
            return float(self.column(field, **kwargs))
        except TypeError:
            return None

    def parse_file(self, rows):
        raise NotImplementedError


class BaseJSON(BaseIngest):

    def load_feed(self, handle):
        rows = json.load(handle)
        self.parse_file(rows)

    def parse_file(self, rows):
        raise NotImplementedError


def ingest_feeds(handle_iterator, prefix, pattern, feed_class):
    """Ingest contents of XML files of a common type, as
    described by a common filename pattern.

    :param handle_iterator: A sequence of file handles of XML files.
    :type handle_iterator: return value of generator
    :param prefix: File path, which is also defined as the prefix of the filename.
    :type prefix: string
    :param pattern: Text pattern common to group of XML files.
    :type pattern: string
    :param feed_class: Data feed interface class.
    :type feed_class: class
    """
    for handle in handle_iterator(prefix, pattern):
        feed_class.load_feed(handle)


def get_local_handles(prefix, pattern):
    """Generates a sequence of file handles for XML files of a common type
    that are hosted on a local machine.

    :param prefix: File path, which is also defined as the prefix of the filename.
    :type prefix: string
    :param pattern: Text pattern common to group of files.
    :type pattern: string
    """
    glob_pattern = os.path.join(prefix, "{}".format(pattern))
    for filename in glob.glob(glob_pattern):
        with open(filename, 'r') as fh:
            yield fh
