# coding=utf-8
from datetime import date

import pytest
from sqlalchemy.exc import DataError

import models.club as mc
import models.common.overview as mco


club_only = pytest.mark.skipif(
    pytest.config.getoption("--schema") != "club",
    reason="Test only valid for club databases"
)


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


@club_only
def test_club_friendly_match_insert(session, club_data):
    friendly_match = mc.ClubFriendlyMatches(**club_data)
    session.add(friendly_match)

    match_from_db = session.query(mc.ClubFriendlyMatches).one()

    print session.query(mco.Confederations).count()

    assert match_from_db.season.name == "2014-2015"
    assert match_from_db.competition.name == u"Test Competition"
    assert match_from_db.competition.country.name == u"England"
    assert match_from_db.venue.name == u"Emirates Stadium"
    assert match_from_db.home_team.name == u"Arsenal FC"
    assert match_from_db.away_team.name == u"Lincoln City FC"
    assert match_from_db.home_manager.full_name == u"Arsène Wenger"
    assert match_from_db.away_manager.full_name == u"Gary Simpson"
    assert match_from_db.referee.full_name == u"Mark Clattenburg"


@club_only
def test_club_league_match_insert(session, club_data):
    league_match = mc.ClubLeagueMatches(matchday=5, **club_data)
    session.add(league_match)

    match_from_db = session.query(mc.ClubLeagueMatches).join(mco.DomesticCompetitions)\
        .filter(mco.DomesticCompetitions.name == club_data['competition'].name).all()[0]

    assert match_from_db.phase == "league"
    assert match_from_db.matchday == 5
    assert match_from_db.season.name == "2014-2015"
    assert match_from_db.competition.name == u"Test Competition"
    assert match_from_db.competition.country.name == u"England"
    assert match_from_db.venue.name == u"Emirates Stadium"
    assert match_from_db.home_team.name == u"Arsenal FC"
    assert match_from_db.away_team.name == u"Lincoln City FC"
    assert match_from_db.home_manager.full_name == u"Arsène Wenger"
    assert match_from_db.away_manager.full_name == u"Gary Simpson"
    assert match_from_db.referee.full_name == u"Mark Clattenburg"

