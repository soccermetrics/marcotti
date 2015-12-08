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

1. Grab latest repo, setup the virtual environment, and install the dependent packages into it:

        $ git clone git://github.com/soccermetrics/marcotti.git
        $ cd marcotti
        $ mkvirtualenv marcotti
        (marcotti) $ pip install -r requirements.txt
    
2. Copy `models\config\local.skel` to `models\config\local.py` and populate it.  Alternative configuration
   settings can be created by subclassing `LocalConfig` and overwriting the attributes.
    
   ```python
   class LocalConfig(Config):
        # At a minimum, these variables must be defined.
        DIALECT = ''
        DBNAME = ''
        
        # For all other non-SQLite databases, these variables must be set.
        DBUSER = ''
        DBPASSWD = ''
        HOSTNAME = ''
        PORT = 5432
   ```
    
## Data Models

Two data schemas are created - one for clubs, the other for national teams.  There is a collection of common data 
models upon which both schemas are based, and data models specific to either schema.

The common data models are classified into five categories:

* **Overview**: High-level data about the football competition
* **Personnel**: Participants and officials in the football match
* **Match**: High-level data about the match
* **Match Events**: The main events of the football match
* **Statistics**: Summary statistics of participating players in the football match

### Common Data Models

#### Overview

* Competitions
* Countries
* DomesticCompetitions
* InternationalCompetitions
* Seasons
* Surfaces
* Timezones
* VenueHistory
* Venues
* Years

#### Personnel

* Managers
* Persons
* Players
* PlayerHistory
* Positions
* Referees

#### Match

* MatchConditions
* Matches
* MatchLineups

#### Events

* Bookables
* Goals
* Penalties
* PenaltyShootoutOpeners
* PenaltyShootouts
* Substitutions

#### Statistics

##### Crosses

* Crosses
* CornerCrosses

##### Defense

* Clearances
* Defensives
* GoalLineClearances
* ShotBlocks
* Tackles

##### Fouls

* Discipline
* FoulWins

##### Goals

* Assists
* GoalBodyparts
* GoalLocations
* GoalTotals
* PenaltyActions

##### Goalkeeper

* GoalkeeperActions
* GoalkeeperAllowedShots
* GoalkeeperAllowedGoals
* GoalkeeperSaves

##### Passes

* Passes
* PassDirections
* PassLengths
* PassLocations

##### Set-Pieces

* Freekicks
* Throwins
* Corners
* ImportantPlays

##### Shots

* ShotBodyparts
* ShotLocations
* ShotPlays
* ShotTotals

##### Touches

* Duels
* Touches
* TouchLocations

### Club-Specific Data Models

* Clubs
* ClubFriendlyMatches
* ClubGroupMatches
* ClubKnockoutMatches
* ClubLeagueMatches
* ClubMatchLineups
* ClubGoals
* ClubPenaltyShootoutOpeners

### National Team-Specific Data Models

* NationalFriendlyMatches
* NationalGroupMatches
* NationalKnockoutMatches
* NationalMatchLineups
* NationalGoals
* NationalPenaltyShootoutOpeners

### Enumerated Types

* BodypartType
* CardType
* ConfederationType
* FoulEventType
* GroupRoundType
* KnockoutRoundType
* NameOrderType
* PositionType
* ShotEventType
* ShotOutcomeType
* SurfaceType
* WeatherConditionType

## Validation Data

Marcotti ships with data that is used to populate the remaining validation models that can't be converted to enumerated types.  The data is in CSV and JSON formats.

Data File            | Data Model
-------------------- | ----------
countries.[csv,json] | Countries
positions.[csv,json] | Positions
surfaces.[csv,json]  | Surfaces
timezones.[csv,json] | Timezones


## Testing

The test suite uses [py.test](http://www.pytest.org) and a PostgreSQL database.  A blank database named `test-marcotti-db` must be created before the tests are run.

Use the following command from the top-level directory of the repository to run the tests:

        $ py.test [--schema club|natl]

If the `schema` option is not passed, only the tests on common data models are run.  The `club` parameter will run the common and club-specific models, while the `natl` parameter will run tests on the common and national-team-specific models.

The tests should work for other server-based RMDBSs such as MySQL or SQL Server.  There _may_ be issues with SQLite backends, but this hasn't been confirmed.

## License

(c) 2015 Soccermetrics Research, LLC. Created under MIT license.  See `LICENSE` file for details.
