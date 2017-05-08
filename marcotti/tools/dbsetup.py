import os
import pip
import pkg_resources

import jinja2
from clint.textui import colored, prompt, puts, validators


db_ports = {
    'postgresql': '5432',
    'mysql': '3306',
    'mssql': '1433',
    'oracle': '1521',
    'firebird': '3050'
}

db_modules = {
    'postgresql': 'psycopg2>=2.6.1',
    'mssql': 'pyodbc>=3.0',
    'mysql': 'mysql-python>=1.2.3',
    'oracle': 'cx_oracle>=5.0',
    'firebird': 'fdb>=1.6'
}

dialect_options = [{'selector': '1', 'prompt': 'PostgreSQL', 'return': 'postgresql'},
                   {'selector': '2', 'prompt': 'MySQL', 'return': 'mysql'},
                   {'selector': '3', 'prompt': 'SQL Server', 'return': 'mssql'},
                   {'selector': '4', 'prompt': 'Oracle', 'return': 'oracle'},
                   {'selector': '5', 'prompt': 'Firebird', 'return': 'firebird'},
                   {'selector': '6', 'prompt': 'SQLite', 'return': 'sqlite'}]


binary_options = [{'selector': '1', 'prompt': 'Yes', 'return': True},
                  {'selector': '2', 'prompt': 'No', 'return': False}]


def path_query(query_string):
    path_txt = prompt.query(query_string, validators=[])
    return None if path_txt == '' else os.path.split(path_txt)


def setup_user_input():
    """
    Setup configuration and database loading script by querying information from user.
    """
    print("#### Please answer the following questions to setup the folder ####")
    log_folder = prompt.query('Logging folder (must exist):', default='.', validators=[validators.PathValidator()])
    loader_file = prompt.query('Loader file name:', default='loader')
    config_file = prompt.query('Config file name:', default='local')
    config_class = prompt.query('Config class name:', default='LocalConfig')
    print("#### Database configuration setup ####")
    dialect = prompt.options('Marcotti-Events Database backend:', dialect_options)
    if dialect == 'sqlite':
        dbname = prompt.query('Database filename (must exist):', validators=[validators.FileValidator()])
        dbuser = ''
        hostname = ''
        dbport = 0
    else:
        dbname = prompt.query('Database name:')
        dbuser = prompt.query('Database user:', default='')
        puts(colored.red('Database password is not defined -- You must define it in the config file!'))
        hostname = prompt.query('Database hostname:', default='localhost')
        dbport = prompt.query('Database path:', default=db_ports.get(dialect))
    print("#### Database season setup ####")
    start_yr = prompt.query('Start season year', default='1990', validators=[validators.IntegerValidator()])
    end_yr = prompt.query('End season year', default='2020', validators=[validators.IntegerValidator()])
    print("#### Data file setup ####")
    supplier = prompt.query('Name of data supplier:')
    is_club_db = prompt.options('Is this a club database?')
    spanish = prompt.options('Are country names in Spanish?')
    using_xml = prompt.options('Are XML files stored locally?', binary_options)
    if using_xml:
        xml_data_dir = prompt.query('Directory containing XML data files:', default='.',
                                    validators=[validators.PathValidator()])
        xml_squads = path_query('Relative path of Squad XML data files:')
        xml_summaries = path_query('Relative path of Match Summary XML data files:')
        xml_events = path_query('Relative path of Match Event XML data files:')
    else:
        xml_data_dir = None
        xml_squads = None
        xml_summaries = None
        xml_events = None
    csv_data_dir = prompt.query('Directory containing CSV data files:', default='.',
                                validators=[validators.PathValidator()])
    supplier_data_path = path_query('Relative path of Suppliers CSV data files:')
    club_data_path = path_query('Relative path of Clubs CSV data files:')
    comp_data_path = path_query('Relative path of Competitions CSV data files:')
    season_data_path = path_query('Relative path of Seasons CSV data files:')
    venue_data_path = path_query('Relative path of Venues CSV data files:')
    player_data_path = path_query('Relative path of Players CSV data files:')
    manager_data_path = path_query('Relative path of Managers CSV data files:')
    referee_data_path = path_query('Relative path of Referees CSV data files:')
    summary_data_path = path_query('Relative path of Match Summary CSV data files:')
    event_data_path = path_query('Relative path of Match Event CSV data files:')

    print("#### End setup questions ####")

    setup_dict = {
        'loader_file': loader_file.lower(),
        'config_file': config_file.lower(),
        'config_class': config_class,
        'supplier': supplier,
        'dialect': dialect,
        'dbname': dbname,
        'dbuser': dbuser,
        'dbhost': hostname,
        'dbport': dbport,
        'start_yr': start_yr,
        'end_yr': end_yr,
        'logging_dir': log_folder,
        'log_file_path': os.path.join(log_folder, 'marcotti.log'),
        'club_db': is_club_db,
        'country_prefix': 'es' * (spanish is True),
        'xml_data_dir': xml_data_dir,
        'xml_data': {
            'squads': xml_squads,
            'matches': xml_summaries,
            'events': xml_events
        },
        'csv_data_dir': csv_data_dir,
        'csv_data': {
            'suppliers': supplier_data_path,
            'competitions': comp_data_path,
            'seasons': season_data_path,
            'clubs': club_data_path,
            'venues': venue_data_path,
            'players': player_data_path,
            'managers': manager_data_path,
            'referees': referee_data_path,
            'matches': summary_data_path,
            'events': event_data_path
        }
    }
    return setup_dict


def main():
    """
    Main function exposed as script command.
    """
    DATA_PATH = pkg_resources.resource_filename('marcottievents', 'data/')
    setup_dict = setup_user_input()
    print("#### Installing database driver ####")
    if setup_dict['dialect'] == 'sqlite':
        print('SQLite database is used -- no external driver needed')
    else:
        pip.main(['install', db_modules.get(setup_dict['dialect'])])
    print("#### Creating settings and data loader modules ####")
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=DATA_PATH),
                             trim_blocks=True, lstrip_blocks=True)
    template_files = ['local.skel', 'logging.skel', 'loader.skel']
    output_files = ['{config_file}.py'.format(**setup_dict),
                    'logging.json',
                    '{loader_file}.py'.format(**setup_dict)]
    for template_file, output_file in zip(template_files, output_files):
        template = env.get_template(os.path.join('templates', template_file))
        with open(output_file, 'w') as g:
            result = template.render(setup_dict)
            g.write(result)
            print("Configured {}".format(output_file))
    print("#### Setup complete ####")
