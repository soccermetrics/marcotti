# coding=utf-8

from datetime import date

import pytest
from sqlalchemy.exc import IntegrityError

import models.common.overview as mco
import models.common.personnel as mcp
import models.common.match as mcm


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


def test_match_generic_insert(session, match_data):
    match = mcm.Matches(**match_data)
    session.add(match)

    match_from_db = session.query(mcm.Matches).one()

    assert match_from_db.first_half_length == 45
    assert match_from_db.second_half_length == 45
    assert match_from_db.first_extra_length == 0
    assert match_from_db.second_extra_length == 0
    assert match_from_db.attendance == 0
    assert match_from_db.phase == 'matches'


def test_match_negative_time_error(session, match_data):
    for field in ['first_half_length', 'second_half_length', 'first_extra_length', 'second_extra_length']:
        new_match_data = dict(match_data, **{field: -1})
        match = mcm.Matches(**new_match_data)
        with pytest.raises(IntegrityError):
            session.add(match)
            session.commit()
        session.rollback()


def test_match_negative_attendance_error(session, match_data):
    new_match_data = dict(match_data, **{'attendance': -1})
    match = mcm.Matches(**new_match_data)
    with pytest.raises(IntegrityError):
        session.add(match)
        session.commit()
    session.rollback()


def test_match_conditions_insert(session, match_data, match_condition_data):
    match_condition_data['match'] = mcm.Matches(**match_data)
    match_conditions = mcm.MatchConditions(**match_condition_data)
    session.add(match_conditions)

    match_from_db = session.query(mcm.Matches).one()
    conditions_from_db = session.query(mcm.MatchConditions).one()

    assert repr(conditions_from_db) == "<MatchCondition(id={}, kickoff=19:30, " \
                                       "temp=15.0, kickoff_weather=Partly Cloudy)>".format(match_from_db.id)


def test_match_conditions_temp_error(session, match_data, match_condition_data):
    match_condition_data['match'] = mcm.Matches(**match_data)
    for out_of_range in [-20.0, 55.0]:
        match_condition_data['kickoff_temp'] = out_of_range
        match_conditions = mcm.MatchConditions(**match_condition_data)
        with pytest.raises(IntegrityError):
            session.add(match_conditions)
            session.commit()
        session.rollback()
