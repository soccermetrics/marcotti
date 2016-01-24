# coding=utf-8

import pytest
from sqlalchemy.exc import IntegrityError

import models.common.personnel as mcp
import models.common.match as mcm


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

    assert repr(conditions_from_db) == "<MatchCondition(id={}, kickoff=19:30, temp=15.0, " \
                                       "humid=68.0, kickoff_weather=Partly Cloudy)>".format(match_from_db.id)


def test_match_conditions_temp_error(session, match_data, match_condition_data):
    match_condition_data['match'] = mcm.Matches(**match_data)
    for out_of_range in [-20.0, 55.0]:
        match_condition_data['kickoff_temp'] = out_of_range
        match_conditions = mcm.MatchConditions(**match_condition_data)
        with pytest.raises(IntegrityError):
            session.add(match_conditions)
            session.commit()
        session.rollback()


def test_match_conditions_humid_error(session, match_data, match_condition_data):
    match_condition_data['match'] = mcm.Matches(**match_data)
    for out_of_range in [-1.0, 102.0]:
        match_condition_data['kickoff_humidity'] = out_of_range
        match_conditions = mcm.MatchConditions(**match_condition_data)
        with pytest.raises(IntegrityError):
            session.add(match_conditions)
            session.commit()
        session.rollback()


def test_match_lineup_generic_insert(session, match_data, person_data, position_data):
    lineup = mcm.MatchLineups(
        match=mcm.Matches(**match_data),
        player=mcp.Players(**person_data['player'][1]),
        position=position_data[1]
    )
    session.add(lineup)

    lineup_from_db = session.query(mcm.MatchLineups).one()
    match_from_db = session.query(mcm.Matches).one()
    player_from_db = session.query(mcp.Players).one()

    assert lineup_from_db.is_starting is False
    assert lineup_from_db.is_captain is False
    assert lineup_from_db.match_id == match_from_db.id
    assert lineup_from_db.player_id == player_from_db.id


def test_lineup_designate_captain(session, match_data, person_data, position_data):
    capn_indx = 1
    lineups = [
        mcm.MatchLineups(
            match=mcm.Matches(**match_data),
            player=mcp.Players(**plyr),
            position=pos,
            is_starting=True,
            is_captain=(j == capn_indx))
        for j, (plyr, pos) in enumerate(zip(person_data['player'], position_data))
        ]
    session.add_all(lineups)

    capn_position = position_data[capn_indx]

    lineup_from_db = session.query(mcm.MatchLineups).join(mcp.Positions).filter(
        mcp.Positions.name == capn_position.name).all()
    assert len(lineup_from_db) == 1
    assert lineup_from_db[0].is_captain is True

    other_lineup_from_db = session.query(mcm.MatchLineups).join(mcp.Positions).filter(
        mcp.Positions.name != capn_position.name).all()
    for others in other_lineup_from_db:
        assert others.is_captain is False


def test_lineup_designate_starter(session, match_data, person_data, position_data):
    starter_indx = 0
    lineups = [
        mcm.MatchLineups(
            match=mcm.Matches(**match_data),
            player=mcp.Players(**plyr),
            position=pos,
            is_starting=(j == starter_indx))
        for j, (plyr, pos) in enumerate(zip(person_data['player'], position_data))
        ]
    session.add_all(lineups)

    starter_position = position_data[starter_indx]

    lineup_from_db = session.query(mcm.MatchLineups).join(mcp.Positions).filter(
        mcp.Positions.name == starter_position.name).all()
    assert len(lineup_from_db) == 1
    assert lineup_from_db[0].is_starting is True
    assert lineup_from_db[0].is_captain is False

    other_lineup_from_db = session.query(mcm.MatchLineups).join(mcp.Positions).filter(
        mcp.Positions.name != starter_position.name).all()
    for others in other_lineup_from_db:
        assert others.is_starting is False
        assert others.is_captain is False
