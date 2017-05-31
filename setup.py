import sys
from setuptools import setup, find_packages


REQUIRES = ['SQLAlchemy>=1.0.9',
            'jinja2>=2.7',
            'clint>=0.4.0']
needs_pytest = {'pytest', 'test', 'ptr'}.intersection(sys.argv)
pytest_runner = ['pytest_runner'] if needs_pytest else []
exec(open('marcotti/version.py').read())

setup(
    name='marcotti',
    version=__version__,
    packages=find_packages(),
    package_data={
        'marcotti': ['data/*.csv', 'data/*.json', 'data/templates/*.skel']
    },
    entry_points={
        'console_scripts': [
            'dbsetup = marcotti.tools.dbsetup:main',
            'testsetup = marcotti.tools.testsetup:main',
        ]
    },
    url='https://github.com/soccermetrics/marcotti',
    license='MIT',
    author='Soccermetrics Research',
    author_email='info@soccermetrics.net',
    keywords=['soccer', 'football', 'soccer analytics', 'data modeling'],
    setup_requires=pytest_runner,
    install_requires=REQUIRES,
    extras_require={
        'PostgreSQL': ['psycopg2>=2.5.1'],
        'MySQL': ['mysql-python>=1.2.3'],
        'MSSQL': ['pyodbc>=3.0'],
        'Oracle': ['cx_oracle>=5.0'],
        'Firebird': ['fdb>=1.6']
    },
    tests_require=['pytest>=2.8.2'],
    description='Data modeling software library for capture of football match result data',
    long_description=open('README.md').read()
)
