from models.config import Config


class LocalConfig(Config):
    """
    Local Configuration class that contains settings for Marcotti database.

    Multiple configurations can be created by subclassing this class and
    overwriting specific class variables.
    """
    # At a minimum, these variables must be defined.
    # Dialects are as defined by SQLAlchemy: firebird, mssql, mysql, oracle, postgresql, sqlite, sybase
    DIALECT = 'postgresql'
    DBNAME = 'marcotti-db'

    # For all other non-SQLite databases, these variables must be set.
    DBUSER = 'howard'
    DBPASSWD = '1234'
    HOSTNAME = 'localhost'
    PORT = 5432
