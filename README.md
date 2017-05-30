Marcotti
========

Marcotti (formerly named the Football Match Result Database) is a data schema that captures match result data in 
order to support football research activities.  Match result data is defined as historical and publicly-available 
data that includes the following:

* Friendly matches and matches that make up league, knockout or hybrid (group + knockout) football competitions, and 
involve either clubs or national team selections.
* Complete data on participating personnel such as players, managers, and match officials.
* Complete top-level data on the football match, including match date, competition name, participating teams, venues, 
and environmental conditions.
* Complete data on macro-events that occur during a match, including goals, penalties, disciplinary events, 
substitutions, and penalty shootouts.
* Summary in-match statistics on participating players, including crossing, passing, shooting, defensive, 
disciplinary, and goalkeeping categories.

The Marcotti data schema is made up of backend-independent SQLAlchemy objects, and club and national team databases are 
built from these objects.

## Installation

Marcotti is written in Python and uses the SQLAlchemy package heavily.

While not required, [virtualenv](https://pypi.python.org/pypi/virtualenv) is strongly recommended and
[virtualenvwrapper](https://pypi.python.org/pypi/virtualenvwrapper) is very convenient.

Installation instructions:

1. Setup the virtual environment and use `pip` to install the package:

        $ cd /path/to/working/dir
        $ mkvirtualenv marcotti
        (marcotti) $ pip install git+https://github.com/soccermetrics/marcotti.git[@{release_tag}]
    
2. Run the `dbsetup` command and answer the setup questions to create configuration and data loading scripts.

    ```shell
    (marcotti-mls) $ dbsetup
    #### Please answer the following questions to setup the folder ####
    Work folder (must exist): [.] /path/to/files
    Logging folder (must exist): [.] /path/to/logs
    Config file name: [local]
    Config class name: [LocalConfig]
    ```
    The command will produce three files in the working folder:

    * `local.py`: A user-defined database configuration file
    * `logging.json`: Default logging configuration file
    * `loader.py`: Data loading module

## Data Models

Two data schemas are created - one for clubs, the other for national teams.  There is a collection of common data 
models upon which both schemas are based, and data models specific to either schema.

The common data models are classified into five categories:

* **Overview**: High-level data about the football competition
* **Personnel**: Participants and officials in the football match
* **Match**: High-level data about the match
* **Match Events**: The main events of the football match
* **Statistics**: Summary statistics of participating players in the football match
* **Suppliers**: Mapping data records from outside sources to Marcotti database

## Documentation

The [Marcotti wiki](https://github.com/soccermetrics/marcotti/wiki) contains extensive user documentation of the 
package.

## License

(c) 2015-2017 Soccermetrics Research, LLC. Created under MIT license.  See `LICENSE` file for details.
