from contextlib import contextmanager

from sqlalchemy.orm.session import Session
from sqlalchemy.engine import create_engine


class Marcotti(object):

    def __init__(self, config):
        self.engine = create_engine(config.DATABASE_URI)
        self.connection = self.engine.connect()

    def create_db(self, base):
        base.metadata.create_all(self.connection)

    @contextmanager
    def create_session(self):
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
