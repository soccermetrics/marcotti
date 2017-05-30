import re
import sys
import logging
import pkg_resources
from contextlib import contextmanager

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session

from .version import __version__


logger = logging.getLogger(__name__)


class Marcotti(object):

    def __init__(self, config):
        logger.info("Marcotti v{0}: Python {1} on {2}".format(
            __version__, sys.version, sys.platform))
        logger.info("Opened connection to {0}".format(self._public_db_uri(config.database_uri)))
        self.engine = create_engine(config.database_uri)
        self.connection = self.engine.connect()

    @staticmethod
    def _public_db_uri(uri):
        """
        Strip out database username/password from database URI.

        :param uri: Database URI string.
        :return: Database URI with username/password removed.
        """
        return re.sub(r"//.*@", "//", uri)

    def create_db(self, base):
        """
        Create database models from database schema object.
        
        :param base: Base schema object that contains data model objects.
        """
        logger.info("Creating data models")
        base.metadata.create_all(self.connection)

    @contextmanager
    def create_session(self):
        """
        Open transaction session with an active database object.
        
        If an error occurs during the session, roll back uncommitted changes
        and report error to log file and user.
        
        If session is no longer needed, commit remaining transactions before closing it.
        """
        session = Session(self.connection)
        logger.info("Create session {0} with {1}".format(
            id(session), self._public_db_uri(str(self.engine.url))))
        try:
            yield session
            session.commit()
            logger.info("Committing remaining transactions to database")
        except Exception as ex:
            session.rollback()
            logger.exception("Database transactions rolled back")
            raise ex
        finally:
            logger.info("Session {0} with {1} closed".format(
                id(session), self._public_db_uri(str(self.engine.url))))
            session.close()


class MarcottiConfig(object):
    """
    Base configuration class for Marcotti.  Contains one method that defines the database URI.

    This class is to be subclassed and its attributes defined therein.
    """

    @property
    def database_uri(self):
        if getattr(self, 'DIALECT') == 'sqlite':
            uri = r'sqlite://{p.DBNAME}'.format(p=self)
        else:
            uri = r'{p.DIALECT}://{p.DBUSER}:{p.DBPASSWD}@{p.HOSTNAME}:{p.PORT}/{p.DBNAME}'.format(p=self)
        return uri
