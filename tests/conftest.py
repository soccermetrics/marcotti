# coding: utf-8
# data fixtures for functional tests

from datetime import date, time

import pytest

import models.common.enums as enums
import models.common.overview as mco
import models.common.personnel as mcp
import models.club as mc


@pytest.fixture
def comp_data():
    return {
        'domestic': {
            'name': u"English Premier League",
            'level': 1,
            'country': mco.Countries(name=u"England", confederation=enums.ConfederationType.europe)
        },
        'international': {
            'name': u"FIFA Club World Cup",
            'level': 1,
            'confederation': enums.ConfederationType.europe
        }
    }


@pytest.fixture
def season_data():
    return {
        'start_year': {
            'yr': 2012
        },
        'end_year': {
            'yr': 2013
        }
    }


@pytest.fixture
def venue_data():
    england = mco.Countries(name=u"England", confederation=enums.ConfederationType.europe)
    tz_london = mco.Timezones(name=u"Europe/London", offset=0.0, confederation=enums.ConfederationType.europe)
    return {
        "name": "Emirates Stadium",
        "city": "London",
        "country": england,
        "timezone": tz_london,
        "latitude": 51.555000,
        "longitude": -0.108611,
        "altitude": 41
    }


@pytest.fixture
def venue_config():
    return {
        "date": date(2006, 7, 22),
        "length": 105,
        "width": 68,
        "capacity": 60361,
        "seats": 60361,
        "surface": mco.Surfaces(description="Desso GrassMaster", type=enums.SurfaceType.hybrid)
    }


@pytest.fixture
def person_data():
    return {
        'generic': {
            'first_name': u"John",
            'last_name': u"Doe",
            'birth_date': date(1980, 1, 1),
            'country': mco.Countries(name=u"Portlandia", confederation=enums.ConfederationType.north_america)
        },
        'manager': [
            {
                'first_name': u"Arsène",
                'last_name': u"Wenger",
                'birth_date': date(1949, 10, 22),
                'country': mco.Countries(name=u"France", confederation=enums.ConfederationType.europe)
            },
            {
                'first_name': u"Arthur",
                'middle_name': u"Antunes",
                'last_name': u"Coimbra",
                'nick_name': u"Zico",
                'birth_date': date(1953, 3, 3),
                'country': mco.Countries(name=u"Brazil", confederation=enums.ConfederationType.south_america)
            }
        ],
        'player': [
            {
                'first_name': u'Miguel',
                'middle_name': u'Ángel',
                'last_name': u'Ponce',
                'second_last_name': u'Briseño',
                'birth_date': date(1989, 4, 12),
                'country': mco.Countries(name=u"Mexico", confederation=enums.ConfederationType.north_america),
                'order': enums.NameOrderType.middle
            },
            {
                'first_name': u"Cristiano",
                'middle_name': u"Ronaldo",
                'last_name': u"Aveiro",
                'second_last_name': u"dos Santos",
                'nick_name': u"Cristiano Ronaldo",
                'birth_date': date(1985, 2, 5),
                'country': mco.Countries(name=u"Portugal", confederation=enums.ConfederationType.europe),
                'order': enums.NameOrderType.western
            },
            {
                'first_name': u'Heung-Min',
                'last_name': u'Son',
                'birth_date': date(1992, 7, 8),
                'country': mco.Countries(name=u"Korea Republic", confederation=enums.ConfederationType.asia),
                'order': enums.NameOrderType.eastern
            }
        ],
        'referee': [
            {
                'first_name': u"Christopher",
                'middle_name': u"J",
                'last_name': u"Foy",
                'birth_date': date(1962, 11, 20),
                'country': mco.Countries(name=u"England", confederation=enums.ConfederationType.europe)
            },
            {
                'first_name': u"Cüneyt",
                'last_name': u"Çakır",
                'birth_date': date(1976, 11, 23),
                'country': mco.Countries(name=u"Turkey", confederation=enums.ConfederationType.europe)
            }
        ]
    }


@pytest.fixture
def position_data():
    return [
        mcp.Positions(name=u"Left back", type=enums.PositionType.defender),
        mcp.Positions(name=u"Forward", type=enums.PositionType.forward),
        mcp.Positions(name=u"Second striker", type=enums.PositionType.forward)
    ]


@pytest.fixture
def player_history_data():
    return [
        {
            'date': date(1996, 1, 1),
            'height': 1.70,
            'weight': 70
        },
        {
            'date': date(1998, 7, 15),
            'height': 1.74,
            'weight': 76
        },
        {
            'date': date(2001, 3, 11),
            'height': 1.76,
            'weight': 80
        }
    ]


@pytest.fixture
def match_condition_data():
    return {
        'kickoff_time': time(19, 30),
        'kickoff_temp': 15.0,
        'kickoff_humidity': 68.0,
        'kickoff_weather': enums.WeatherConditionType.partly_cloudy,
        'halftime_weather': enums.WeatherConditionType.clear,
        'fulltime_weather': enums.WeatherConditionType.windy_clear
    }


@pytest.fixture
def match_data(comp_data, season_data, venue_data, person_data):
    return {
        "date": date(2012, 12, 12),
        "competition": mco.DomesticCompetitions(**comp_data['domestic']),
        "season": mco.Seasons(**{k: mco.Years(**v) for k, v in season_data.items()}),
        "venue": mco.Venues(**venue_data),
        "home_manager": mcp.Managers(**person_data['manager'][0]),
        "away_manager": mcp.Managers(**person_data['manager'][1]),
        "referee": mcp.Referees(**person_data['referee'][0])
    }


@pytest.fixture
def club_data():
    england = mco.Countries(name=u"England", confederation=enums.ConfederationType.europe)
    france = mco.Countries(name=u"France", confederation=enums.ConfederationType.europe)
    tz_london = mco.Timezones(name=u"Europe/London", offset=0.0, confederation=enums.ConfederationType.europe)
    return {
        'date': date(2015, 1, 1),
        'competition': mco.DomesticCompetitions(name=u'Test Competition', level=1, country=england),
        'season': mco.Seasons(start_year=mco.Years(yr=2014), end_year=mco.Years(yr=2015)),
        'venue': mco.Venues(name=u"Emirates Stadium", city=u"London", country=england, timezone=tz_london),
        'home_team': mc.Clubs(name=u"Arsenal FC", country=england),
        'away_team': mc.Clubs(name=u"Lincoln City FC", country=england),
        'home_manager': mcp.Managers(first_name=u"Arsène", last_name=u"Wenger",
                                     birth_date=date(1949, 10, 22), country=france),
        'away_manager': mcp.Managers(first_name=u"Gary", last_name=u"Simpson",
                                     birth_date=date(1961, 4, 11), country=england),
        'referee': mcp.Referees(first_name=u"Mark", last_name=u"Clattenburg",
                                birth_date=date(1975, 3, 13), country=england)
    }


@pytest.fixture
def national_data():
    mexico = mco.Countries(name=u"Mexico", confederation=enums.ConfederationType.north_america)
    england = mco.Countries(name=u"England", confederation=enums.ConfederationType.europe)
    france = mco.Countries(name=u"France", confederation=enums.ConfederationType.europe)
    italy = mco.Countries(name=u"Italy", confederation=enums.ConfederationType.europe)
    tz_london = mco.Timezones(name=u"Europe/London", offset=0.0, confederation=enums.ConfederationType.europe)
    return {
        'date': date(1997, 11, 12),
        'competition': mco.InternationalCompetitions(name=u"International Cup", level=1,
                                                     confederation=enums.ConfederationType.fifa),
        'season': mco.Seasons(start_year=mco.Years(yr=1997), end_year=mco.Years(yr=1998)),
        'venue': mco.Venues(name=u"Emirates Stadium", city=u"London", country=england, timezone=tz_london),
        'home_team': france,
        'away_team': mexico,
        'home_manager': mcp.Managers(first_name=u"Arsène", last_name=u"Wenger",
                                     birth_date=date(1949, 10, 22), country=france),
        'away_manager': mcp.Managers(first_name=u"Gary", last_name=u"Simpson",
                                     birth_date=date(1961, 4, 11), country=england),
        'referee': mcp.Referees(first_name=u"Pierluigi", last_name=u"Collina",
                                birth_date=date(1960, 2, 13), country=italy)
    }
