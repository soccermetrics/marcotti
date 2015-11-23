# coding=utf-8
from datetime import date

import pytest
from sqlalchemy.exc import DataError

import models.club as mc
import models.common.overview as mco
import models.common.personnel as mcp


club_only = pytest.mark.skipif(
    pytest.config.getoption("--schema") != "club",
    reason="Test only valid for club databases"
)


@pytest.fixture
def club_data():
    uefa = mco.Confederations(name=u"UEFA")
    england = mco.Countries(name=u"England", confederation=uefa)
    france = mco.Countries(name=u"France", confederation=uefa)
    tz_london = mco.Timezones(name=u"Europe/London", offset=0.0, confederation=uefa)
    return {
        'date': date(2015, 1, 1),
        'competition': mco.DomesticCompetitions(name=u'Test Competition', level=1, country=england),
        'season': mco.Seasons(start_year=mco.Years(yr=2014), end_year=mco.Years(yr=2015)),
        'venue': mco.Venues(name="Emirates Stadium", city="London", country=england, timezone=tz_london),
        'home_team': mc.Clubs(name=u"Arsenal FC", country=england),
        'away_team': mc.Clubs(name=u"Lincoln City FC", country=england),
        'home_manager': mcp.Managers(first_name=u"Arsène", last_name=u"Wenger",
                                     birth_date=date(1949, 10, 22), country=france),
        'away_manager': mcp.Managers(first_name=u"Gary", last_name=u"Simpson",
                                     birth_date=date(1961, 4, 11), country=england),
        'referee': mcp.Referees(first_name=u"Mark", last_name=u"Clattenburg",
                                birth_date=date(1975, 3, 13), country=england)
    }


@club_only
def test_club_insert(session):
    club = mc.Clubs(name=u"Arsenal",
                    country=mco.Countries(name=u"England", confederation=mco.Confederations(name=u"UEFA")))
    session.add(club)

    result = session.query(mc.Clubs).one()
    assert result.name == u"Arsenal"
    assert repr(result) == "<Club(name=Arsenal, country=England)>"


@club_only
def test_club_unicode_insert(session):
    club = mc.Clubs(name=u"Фк Спартак Москва",
                    country=mco.Countries(name=u"Russia", confederation=mco.Confederations(name=u"UEFA")))
    session.add(club)

    result = session.query(mc.Clubs).join(mco.Countries).filter(mco.Countries.name == u"Russia").one()

    assert result.name == u"Фк Спартак Москва"
    assert unicode(result) == u"<Club(name=Фк Спартак Москва, country=Russia)>"


@club_only
def test_club_name_overflow(session):
    too_long_name = "blahblah" * 8
    too_long_club = mc.Clubs(name=too_long_name,
                             country=mco.Countries(name=u"foo", confederation=mco.Confederations(name=u"bar")))
    with pytest.raises(DataError):
        session.add(too_long_club)
        session.commit()
