import glob
import csv


class BaseCSV(object):

    def __init__(self, session):
        self.session = session

    def load_feed(self, handle):
        rows = csv.DictReader(handle)
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
    glob_pattern = "%s*%s" % (prefix, pattern)
    for filename in glob.glob(glob_pattern):
        with open(filename) as fh:
            yield fh
