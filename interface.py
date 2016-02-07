from contextlib import contextmanager

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import Session

from etl import get_local_handles, ingest_feeds, create_seasons
from etl.ecsv import validation


class Marcotti(object):

    def __init__(self, config):
        self.engine = create_engine(config.DATABASE_URI)
        self.connection = self.engine.connect()
        self.start_year = config.START_YEAR
        self.end_year = config.END_YEAR

    def create_db(self, base):
        """
        Create database tables from models defined in schema and populate validation tables.

        :param base: One of the declarative class objects (ClubSchema, NatlSchema).
        """
        print "Creating schemas..."
        base.metadata.create_all(self.connection)
        print "Ingesting validation files..."
        with self.create_session() as sess:
            create_seasons(sess, self.start_year, self.end_year)
            ingest_feeds(get_local_handles, 'data', 'countries.csv', validation.CountryIngest(sess))
            ingest_feeds(get_local_handles, 'data', 'timezones.csv', validation.TimezoneIngest(sess))
            ingest_feeds(get_local_handles, 'data', 'surfaces.csv', validation.SurfaceIngest(sess))
            ingest_feeds(get_local_handles, 'data', 'positions.csv', validation.PositionIngest(sess))
        print "Ingestion complete."

    @contextmanager
    def create_session(self):
        """
        Create a session context that communicates with the database.

        Commits all changes to the database before closing the session, and if an exception is raised,
        rollback the session.
        """
        session = Session(self.connection)
        try:
            yield session
            session.commit()
        except Exception as ex:
            session.rollback()
            raise ex
        finally:
            session.close()


if __name__ == "__main__":
    from models.club import ClubSchema
    from models.config.local import LocalConfig

    marcotti = Marcotti(LocalConfig())
    marcotti.create_db(ClubSchema)
