# coding=utf-8
from datetime import date

import pytest
from sqlalchemy.sql import func
from sqlalchemy.exc import DataError, IntegrityError

import models.common.enums as enums
import models.common.overview as mco


def test_confederation_insert(session):
    """Confederation 001: Insert a single record into Confederation table and verify data."""
    uefa = mco.Confederations(name=u"UEFA")
    session.add(uefa)

    result = session.query(mco.Confederations).filter_by(name=u"UEFA").one()
    assert result.name == u"UEFA"
    assert repr(result) == "<Confederation(id={0}, name=UEFA)>".format(result.id)


def test_confederation_overflow_error(session):
    """Confederation 002: Verify error if confederation name exceeds field length."""
    too_long_confederation = mco.Confederations(name=u'ABCDEFGHIJKL')
    with pytest.raises(DataError):
        session.add(too_long_confederation)
        session.commit()


def test_country_insert(session):
        """Country 001: Insert a single record into Countries table and verify data."""
        england = mco.Countries(name=u'England', confederation=mco.Confederations(name=u'UEFA'))
        session.add(england)

        country = session.query(mco.Countries).all()

        assert country[0].name == u'England'
        assert country[0].confederation.name == u'UEFA'
        assert repr(country[0]) == "<Country(id={0}, name=England, confed=UEFA)>".format(country[0].id)


def test_country_unicode_insert(session):
    """Country 002: Insert a single record with Unicode characters into Countries table and verify data."""
    ivory_coast = mco.Countries(name=u"Côte d'Ivoire", confederation=mco.Confederations(name=u'CAF'))
    session.add(ivory_coast)

    country = session.query(mco.Countries).join(mco.Confederations).filter(mco.Confederations.name == u'CAF').one()

    assert country.name == u"Côte d'Ivoire"
    assert country.confederation.name == u'CAF'


def test_country_name_overflow_error(session):
    """Country 003: Verify error if country name exceeds field length."""
    too_long_name = "blahblah" * 8
    too_long_country = mco.Countries(name=unicode(too_long_name), confederation=mco.Confederations(name=u'CONCACAF'))
    with pytest.raises(DataError):
        session.add(too_long_country)
        session.commit()


def test_competition_insert(session):
    """Competition 001: Insert a single record into Competitions table and verify data."""
    record = mco.Competitions(name=u"English Premier League", level=1)
    session.add(record)

    competition = session.query(mco.Competitions).filter_by(level=1).one()

    assert competition.name == u"English Premier League"
    assert competition.level == 1


def test_competition_unicode_insert(session):
    """Competition 002: Insert a single record with Unicode characters into Competitions table and verify data."""
    record = mco.Competitions(name=u"Süper Lig", level=1)
    session.add(record)

    competition = session.query(mco.Competitions).one()

    assert competition.name == u"Süper Lig"


def test_competition_name_overflow_error(session):
    """Competition 003: Verify error if competition name exceeds field length."""
    too_long_name = "leaguename" * 9
    record = mco.Competitions(name=unicode(too_long_name), level=2)
    with pytest.raises(DataError):
        session.add(record)
        session.commit()


def test_domestic_competition_insert(session):
    """Domestic Competition 001: Insert domestic competition record and verify data."""
    comp_name = u"English Premier League"
    comp_country = u"England"
    comp_confed = u"UEFA"
    comp_level = 1
    record = mco.DomesticCompetitions(name=comp_name, level=comp_level, country=mco.Countries(
        name=comp_country, confederation=mco.Confederations(name=comp_confed)))
    session.add(record)

    competition = session.query(mco.DomesticCompetitions).one()

    assert repr(competition) == "<DomesticCompetition(name={0}, country={1}, level={2})>".format(
        comp_name, comp_country, comp_level)
    assert competition.name == comp_name
    assert competition.level == comp_level
    assert competition.country.name == comp_country


def test_international_competition_insert(session):
    """International Competition 001: Insert international competition record and verify data."""
    comp_name = u"UEFA Champions League"
    comp_confed = u"UEFA"
    record = mco.InternationalCompetitions(name=comp_name, level=1,
                                           confederation=mco.Confederations(name=comp_confed))
    session.add(record)

    competition = session.query(mco.InternationalCompetitions).one()

    assert repr(competition) == "<InternationalCompetition(name={0}, confederation={1})>".format(
        comp_name, comp_confed
    )
    assert competition.name == comp_name
    assert competition.level == 1
    assert competition.confederation.name == comp_confed


def test_year_insert(session):
    """Year 001: Insert multiple years into Years table and verify data."""
    years_list = range(1990, 1994)
    for yr in years_list:
        record = mco.Years(yr=yr)
        session.add(record)

    years = session.query(mco.Years.yr).all()
    years_from_db = [x[0] for x in years]

    assert set(years_from_db) & set(years_list) == set(years_list)


def test_year_duplicate_error(session):
    """Year 002: Verify error if year is inserted twice in Years table."""
    for yr in range(1992, 1995):
        record = mco.Years(yr=yr)
        session.add(record)

    duplicate = mco.Years(yr=1994)
    with pytest.raises(IntegrityError):
        session.add(duplicate)
        session.commit()


def test_season_insert(session):
    """Season 001: Insert records into Seasons table and verify data."""
    yr_1994 = mco.Years(yr=1994)
    yr_1995 = mco.Years(yr=1995)

    season_94 = mco.Seasons(start_year=yr_1994, end_year=yr_1994)
    season_9495 = mco.Seasons(start_year=yr_1994, end_year=yr_1995)
    session.add(season_94)
    session.add(season_9495)

    seasons_from_db = [repr(obj) for obj in session.query(mco.Seasons).all()]
    seasons_test = ["<Season(1994)>", "<Season(1994-1995)>"]

    assert set(seasons_from_db) & set(seasons_test) == set(seasons_test)


def test_season_multiyr_search(session):
    """Season 002: Retrieve Season record using multi-year season name."""
    yr_1994 = mco.Years(yr=1994)
    yr_1995 = mco.Years(yr=1995)
    season_9495 = mco.Seasons(start_year=yr_1994, end_year=yr_1995)
    session.add(season_9495)

    record = session.query(mco.Seasons).filter(mco.Seasons.name == '1994-1995').one()
    assert repr(season_9495) == repr(record)


def test_season_multiyr_reference_date(session):
    """Season 003: Verify that reference date for season across two years is June 30."""
    yr_1994 = mco.Years(yr=1994)
    yr_1995 = mco.Years(yr=1995)
    season_9495 = mco.Seasons(start_year=yr_1994, end_year=yr_1995)
    session.add(season_9495)

    record = session.query(mco.Seasons).filter(mco.Seasons.start_year == yr_1994).one()
    assert record.reference_date == date(1995, 6, 30)


def test_season_singleyr_search(session):
    """Season 002: Retrieve Season record using multi-year season name."""
    yr_1994 = mco.Years(yr=1994)
    season_94 = mco.Seasons(start_year=yr_1994, end_year=yr_1994)
    session.add(season_94)

    record = session.query(mco.Seasons).filter(mco.Seasons.name == '1994').one()
    assert repr(season_94) == repr(record)


def test_season_singleyr_reference_date(session):
    """Season 005: Verify that reference date for season over one year is December 31."""
    yr_1994 = mco.Years(yr=1994)
    season_94 = mco.Seasons(start_year=yr_1994, end_year=yr_1994)
    session.add(season_94)

    record = session.query(mco.Seasons).filter(mco.Seasons.start_year == yr_1994).one()
    assert record.reference_date == date(1994, 12, 31)


def test_group_round_insert(session):
    """Group Rounds 001: Insert a single record into Group Rounds table and verify data."""
    grp_stage_name = u"Group Stage"
    grp_stage = mco.GroupRounds(name=grp_stage_name)
    session.add(grp_stage)

    result = session.query(mco.GroupRounds).filter_by(name=grp_stage_name).one()
    assert result.name == grp_stage_name
    assert repr(result) == "<GroupRound(name={0})>".format(grp_stage_name)


def test_group_round_name_overflow_error(session):
    """Group Rounds 002: Verify error if group round name exceeds field length."""
    too_long_name = "groupround" * 5
    record = mco.GroupRounds(name=unicode(too_long_name))
    with pytest.raises(DataError):
        session.add(record)
        session.commit()


def test_knockout_round_insert(session):
    """Knockout Rounds 001: Insert a single record into Knockout Rounds table and verify data."""
    qfinal_name = u"Quarterfinal (1/4)"
    qfinal = mco.KnockoutRounds(name=qfinal_name)
    session.add(qfinal)

    result = session.query(mco.KnockoutRounds).filter_by(name=qfinal_name).one()
    assert result.name == qfinal_name
    assert repr(result) == "<KnockoutRound(name={0})>".format(qfinal_name)


def test_knockout_round_name_overflow_error(session):
    """Knockout Rounds 002: Verify error if knockout round name exceeds field length."""
    too_long_name = "knockoutround" * 5
    record = mco.KnockoutRounds(name=unicode(too_long_name))
    with pytest.raises(DataError):
        session.add(record)
        session.commit()


def test_timezone_insert(session):
    """Timezone 001: Insert timezone records into Timezones table and verify data."""
    timezones = [
        mco.Timezones(name=u"Europe/Paris", offset=1, confederation=mco.Confederations(name=u"UEFA")),
        mco.Timezones(name=u"America/New_York", offset=-5.0, confederation=mco.Confederations(name=u"CONCACAF")),
        mco.Timezones(name=u"Asia/Kathmandu", offset=+5.75, confederation=mco.Confederations(name=u"AFC"))
    ]
    session.add_all(timezones)

    tz_uefa = session.query(mco.Timezones).join(mco.Confederations).filter(mco.Confederations.name == u"UEFA").one()
    assert repr(tz_uefa) == "<Timezone(name=Europe/Paris, offset=+1.00, confederation=UEFA)>"

    stmt = session.query(func.min(mco.Timezones.offset).label('far_west')).subquery()
    tz_farwest = session.query(mco.Timezones).filter(mco.Timezones.offset == stmt.c.far_west).one()
    assert repr(tz_farwest) == "<Timezone(name=America/New_York, offset=-5.00, confederation=CONCACAF)>"

    stmt = session.query(func.max(mco.Timezones.offset).label('far_east')).subquery()
    tz_fareast = session.query(mco.Timezones).filter(mco.Timezones.offset == stmt.c.far_east).one()
    assert repr(tz_fareast) == "<Timezone(name=Asia/Kathmandu, offset=+5.75, confederation=AFC)>"


def test_venue_generic_insert(session, venue_data):
    """Venue 001: Insert generic venue records into Venues table and verify data."""
    session.add(mco.Venues(**venue_data))

    emirates = session.query(mco.Venues).one()

    assert repr(emirates) == u"<Venue(name=Emirates Stadium, city=London, country=England)>"
    assert emirates.region is None
    assert emirates.latitude == 51.555000
    assert emirates.longitude == -0.108611
    assert emirates.altitude == 41
    assert repr(emirates.timezone) == "<Timezone(name=Europe/London, offset=+0.00, confederation=UEFA)>"


def test_venue_empty_coordinates(session, venue_data):
    """Venue 002: Verify that lat/long/alt coordinates are zeroed if not present in Venues object definition."""
    revised_venue_data = {key: value for key, value in venue_data.items()
                          if key not in ['latitude', 'longitude', 'altitude']}
    session.add(mco.Venues(**revised_venue_data))

    emirates = session.query(mco.Venues).one()

    assert emirates.latitude == 0.000000
    assert emirates.longitude == 0.000000
    assert emirates.altitude == 0


def test_venue_latitude_error(session, venue_data):
    """Venue 003: Verify error if latitude of match venue exceeds range."""
    for direction in [-1, 1]:
        venue_data['latitude'] = 92.123456 * direction
        venue = mco.Venues(**venue_data)
        with pytest.raises(IntegrityError):
            session.add(venue)
            session.commit()
        session.rollback()


def test_venue_longitude_error(session, venue_data):
    """Venue 004: Verify error if longitude of match venue exceeds range."""
    for direction in [-1, 1]:
        venue_data['longitude'] = 200.000000 * direction
        venue = mco.Venues(**venue_data)
        with pytest.raises(IntegrityError):
            session.add(venue)
            session.commit()
        session.rollback()


def test_venue_altitude_error(session, venue_data):
    """Venue 005: Verify error if altitude of match venue is out of range."""
    for out_of_range in [-205, 4600]:
        venue_data['altitude'] = out_of_range
        venue = mco.Venues(**venue_data)
        with pytest.raises(IntegrityError):
            session.add(venue)
            session.commit()
        session.rollback()


def test_venue_history_insert(session, venue_data, venue_config):
    """Venue 006: Insert venue history data into VenueHistory model and verify data."""
    emirates = mco.Venues(**venue_data)
    venue_config['venue'] = emirates
    emirates_config = mco.VenueHistory(**venue_config)
    session.add(emirates_config)

    record = session.query(mco.VenueHistory).one()

    assert repr(record) == u"<VenueHistory(name=Emirates Stadium, date=2006-07-22, " \
                           u"length=105, width=68, capacity=60361)>"
    assert record.seats == 60361
    assert record.surface.description == u"Desso GrassMaster"
    assert record.surface.type == enums.SurfaceType.hybrid


def test_venue_history_empty_numbers(session, venue_data, venue_config):
    """Venue 007: Verify that length/width/capacity/seats fields are set to default if missing in VenueHistory data."""
    emirates = mco.Venues(**venue_data)
    venue_config['venue'] = emirates
    revised_venue_config = {key: value for key, value in venue_config.items()
                            if key not in ['length', 'width', 'capacity', 'seats']}
    emirates_config = mco.VenueHistory(**revised_venue_config)
    session.add(emirates_config)

    record = session.query(mco.VenueHistory).one()

    assert record.length == 105
    assert record.width == 68
    assert record.capacity == 0
    assert record.seats == 0


def test_venue_history_field_dimension_error(session, venue_data, venue_config):
    """Venue 007: Verify error if length/width fields in VenueHistory data are out of range."""
    emirates = mco.Venues(**venue_data)
    venue_config['venue'] = emirates
    for field, values in zip(['length', 'width'], [(85, 125), (40, 95)]):
        for out_of_range in values:
            venue_config[field] = out_of_range
            emirates_config = mco.VenueHistory(**venue_config)
            with pytest.raises(IntegrityError):
                session.add(emirates_config)
                session.commit()
            session.rollback()


def test_venue_history_capacity_error(session, venue_data, venue_config):
    """Venue 007: Verify error if length/width fields in VenueHistory data are out of range."""
    emirates = mco.Venues(**venue_data)
    venue_config['venue'] = emirates
    for field in ['capacity', 'seats']:
        new_venue_config = dict(venue_config, **{field: -1})
        emirates_config = mco.VenueHistory(**new_venue_config)
        with pytest.raises(IntegrityError):
            session.add(emirates_config)
            session.commit()
        session.rollback()


def test_surface_generic_insert(session):
    """Playing Surface 001: Insert playing surface data into Surfaces model and verify data."""
    surfaces = [
        mco.Surfaces(description=u"Perennial ryegrass", type=enums.SurfaceType.natural),
        mco.Surfaces(description=u"Desso GrassMaster", type=enums.SurfaceType.hybrid),
        mco.Surfaces(description=u"FieldTurf", type=enums.SurfaceType.artificial)
    ]
    session.add_all(surfaces)

    natural = session.query(mco.Surfaces).filter(mco.Surfaces.type == enums.SurfaceType.natural).one()

    assert repr(natural) == u"<Surface(description=Perennial ryegrass, type=Natural)>"


def test_surface_empty_description_error(session):
    """Playing Surface 002: Verify error if description field for Surfaces model is empty."""
    surface = mco.Surfaces(type=enums.SurfaceType.natural)
    with pytest.raises(IntegrityError):
        session.add(surface)
        session.commit()
