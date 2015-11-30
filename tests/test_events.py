# coding=utf-8

import pytest
from sqlalchemy.exc import IntegrityError, DataError

import models.common.enums as enums
import models.common.personnel as mcp
import models.common.match as mcm
import models.common.events as mce


@pytest.fixture
def match_lineup(session, match_data, person_data, position_data):
    match = mcm.Matches(**match_data)
    session.add(match)

    match_from_db = session.query(mcm.Matches).one()

    lineups = [
        mcm.MatchLineups(
            match_id=match_from_db.id,
            player=mcp.Players(**plyr),
            position=pos,
            is_starting=True,
            is_captain=False)
        for j, (plyr, pos) in enumerate(zip(person_data['player'], position_data))
        ]
    session.add_all(lineups)

    scorer_indx = 1

    lineup_from_db = session.query(mcm.MatchLineups).join(mcp.Players).\
        filter(mcp.Players.last_name == person_data['player'][scorer_indx]['last_name']).one()

    return match_from_db, lineup_from_db


def test_goals_generic_insert(session, match_lineup):
    match_from_db, lineup_from_db = match_lineup

    goal = mce.Goals(
        lineup_id=lineup_from_db.id,
        bodypart=enums.BodypartType.left_foot,
        event=enums.ShotEventType.shot_18_box,
        time=65
    )
    session.add(goal)

    goals_from_db = session.query(mce.Goals).join(mcm.MatchLineups).join(mcm.Matches).\
        filter(mcm.Matches.id == match_from_db.id)

    assert goals_from_db.count() == 1
    assert goals_from_db[0].time == 65
    assert goals_from_db[0].stoppage == 0
    assert goals_from_db[0].bodypart.value == "Left foot"
    assert goals_from_db[0].event.value == "Shot inside penalty area"

    assert len(lineup_from_db.goals) == 1


def test_event_missing_time_error(session, match_lineup):
    match_from_db, lineup_from_db = match_lineup

    with pytest.raises(IntegrityError):
        goal = mce.Goals(
            lineup_id=lineup_from_db.id,
            bodypart=enums.BodypartType.left_foot,
            event=enums.ShotEventType.shot_18_box
        )
        session.add(goal)
        session.commit()


def test_event_time_out_of_range_error(session, match_lineup):
    match_from_db, lineup_from_db = match_lineup

    for out_of_range in [-1, 0, 121]:
        with pytest.raises(IntegrityError):
            goal = mce.Goals(
                lineup_id=lineup_from_db.id,
                bodypart=enums.BodypartType.left_foot,
                event=enums.ShotEventType.shot_18_box,
                time=out_of_range
            )
            session.add(goal)
            session.commit()
        session.rollback()


def test_event_stoppage_time_out_of_range_error(session, match_lineup):
    match_from_db, lineup_from_db = match_lineup

    for out_of_range in [-1, 20]:
        with pytest.raises(IntegrityError):
            goal = mce.Goals(
                lineup_id=lineup_from_db.id,
                bodypart=enums.BodypartType.left_foot,
                event=enums.ShotEventType.shot_18_box,
                time=90,
                stoppage=out_of_range
            )
            session.add(goal)
            session.commit()
        session.rollback()

