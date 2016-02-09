class Config(object):
    """
    Base configuration class.  Contains one method that defines the database URI.

    This class is to be subclassed and its attributes defined therein.
    """

    def __init__(self):
        self.database_uri()

    def database_uri(self):
        if self.DIALECT == 'sqlite':
            self.DATABASE_URI = r'sqlite://{name}'.format(name=self.DBNAME)
        else:
            self.DATABASE_URI = r'{dialect}://{user}:{passwd}@{host}:{port}/{name}'.format(
                dialect=self.DIALECT, user=self.DBUSER, passwd=self.DBPASSWD,
                host=self.HOSTNAME, port=self.PORT, name=self.DBNAME
            )
