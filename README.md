Marcotti
========

This is the implementation of the Marcotti database models (formerly named the Football Match Result Database).  The models are implemented as backend-independent SQLAlchemy objects, and club and national team databases are 
built from these objects.

This data model captures major events for teams, whether clubs or national teams, participating in league, knockout, or hybrid (league+knockout) competitions.  

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

There are four categories under which the tables are classified:

* **Overview**: High-level data about the football competition
* **Personnel**: Participants and officials in the football match
* **Match**: High-level data about the match
* **Match Events**: The main events of the football match

Two data schemas are created - one for clubs, the other for national teams.  There is a collection of common data models that are shared by both schemas.

### Common Data Models

#### Overview

* Competitions
* Confederations
* Countries
* DomesticCompetitions
* GroupRounds
* InternationalCompetitions
* KnockoutRounds
* Seasons
* Surfaces
* Timezones
* VenueHistory
* Venues
* WeatherConditions
* Years

#### Personnel

* Managers
* Persons
* Players
* Positions
* Referees

#### Match

* FriendlyMatches
* GroupMatches
* KnockoutMatches
* LeagueMatches
* MatchConditions
* Matches
* MatchLineups

#### Events

* Bookables
* Fouls
* Goals
* Penalties
* PenaltyShootoutOpeners
* PenaltyShootouts
* ShotEvents
* Substitutions

### Club-Specific Data Models

* Clubs
* ClubFriendlyMatches
* ClubGroupMatches
* ClubKnockoutMatches
* ClubLeagueMatches
* ClubMatchLineups

### National Team-Specific Data Models

* NationalFriendlyMatches
* NationalGroupMatches
* NationalKnockoutMatches
* NationalLeagueMatches
* NationalMatchLineups

## Testing

The test suite uses [py.test](http://www.pytest.org) and a PostgreSQL database.  A blank database named `test-marcotti-db` must be created before the tests are run.

Use the following command from the top-level directory of the repository to run the tests:

        $ py.test [--schema club|natl]

If the `schema` option is not passed, only the tests on common data models are run.  The `club` parameter will run the common and club-specific models, while the `natl` parameter will run tests on the common and national-team-specific models.

The tests should work for other server-based RMDBSs such as MySQL or SQL Server.  There _may_ be issues with SQLite backends, but this hasn't been confirmed.

## License

(c) 2015 Soccermetrics Research, LLC. Created under MIT license.  See `LICENSE` file for details.
