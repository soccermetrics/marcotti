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
