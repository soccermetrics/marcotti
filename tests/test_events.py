# coding=utf-8

import pytest
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError

import marcotti.models.common.enums as enums
import marcotti.models.common.personnel as mcp
import marcotti.models.common.match as mcm
import marcotti.models.common.events as mce


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


def test_penalties_insert(session, match_lineup):
    match_from_db, lineup_from_db = match_lineup
    
    penalty = mce.Penalties(
        lineup_id = lineup_from_db.id,
        foul=enums.FoulEventType.handball,
        outcome=enums.ShotOutcomeType.goal,
        time=77
    )
    session.add(penalty)
    
    penalties_from_db = session.query(mce.Penalties).filter(mce.Penalties.outcome == enums.ShotOutcomeType.goal)
    
    assert penalties_from_db.count() == 1
    assert penalties_from_db[0].foul.value == "Handball"
    assert penalties_from_db[0].lineup == lineup_from_db
    assert len(lineup_from_db.penalties) == 1


def test_bookable_offense_insert(session, match_lineup):
    match_from_db, lineup_from_db = match_lineup
    
    offense = mce.Bookables(
        lineup_id = lineup_from_db.id,
        foul=enums.FoulEventType.repeated_fouling,
        card=enums.CardType.yellow,
        time=53
    )
    session.add(offense)

    offenses_from_db = session.query(mce.Bookables).join(mcm.MatchLineups).\
        filter(mcm.MatchLineups.id == lineup_from_db.id)

    assert offenses_from_db.count() == 1
    assert offenses_from_db[0].card.value == "Yellow"
    assert offenses_from_db[0].foul.value == "Persistent infringement"
    assert offenses_from_db[0].time == 53
    assert len(lineup_from_db.bookables) == 1


def test_substitutions_insert(session, match_lineup, person_data):
    match_from_db, lineup_from_db = match_lineup

    bench_lineup = mcm.MatchLineups(
        match_id=match_from_db.id,
        player=mcp.Players(**person_data['generic']),
        position=mcp.Positions(name=u"Center back", type=enums.PositionType.defender),
        is_starting=False,
        is_captain=False
    )
    session.add(bench_lineup)
    session.commit()

    substitution = mce.Substitutions(
        lineup_in_id=bench_lineup.id,
        lineup_out_id=lineup_from_db.id,
        time=67
    )
    session.add(substitution)

    lineup_alias = aliased(mcm.MatchLineups)
    substitution_from_db = session.query(mce.Substitutions)\
        .join(mcm.MatchLineups, mcm.MatchLineups.id == mce.Substitutions.lineup_in_id)\
        .join(lineup_alias, lineup_alias.id == mce.Substitutions.lineup_out_id)\
        .join(mcm.Matches).filter(mcm.Matches.id == match_from_db.id)

    assert substitution_from_db.count() == 1
    assert substitution_from_db[0].lineup_out.full_name == u"Cristiano Ronaldo"
    assert substitution_from_db[0].lineup_in.full_name == u"John Doe"
    assert substitution_from_db[0].time == 67


def test_retirement_insert(session, match_lineup):
    match_from_db, lineup_from_db = match_lineup

    withdrawal = mce.Substitutions(lineup_out_id=lineup_from_db.id, time=85)
    session.add(withdrawal)

    lineup_alias = aliased(mcm.MatchLineups)
    withdrawal_from_db = session.query(mce.Substitutions)\
        .outerjoin(mcm.MatchLineups, mcm.MatchLineups.id == mce.Substitutions.lineup_in_id)\
        .join(lineup_alias, lineup_alias.id == mce.Substitutions.lineup_out_id)\
        .join(mcm.Matches).filter(mcm.Matches.id == match_from_db.id)

    assert withdrawal_from_db.count() == 1
    assert withdrawal_from_db[0].lineup_out.full_name == u"Cristiano Ronaldo"
    assert withdrawal_from_db[0].lineup_in is None
    assert withdrawal_from_db[0].time == 85


def test_penalty_shootouts_insert(session, match_lineup):
    match_from_db, lineup_from_db = match_lineup

    shootout = mce.PenaltyShootouts(
        lineup_id=lineup_from_db.id,
        round=4,
        outcome=enums.ShotOutcomeType.over
    )
    session.add(shootout)

    shootout_from_db = session.query(mce.PenaltyShootouts).join(mcm.MatchLineups)\
        .join(mcm.Matches).filter(mcm.Matches.id == match_from_db.id)

    assert shootout_from_db.count() == 1
    assert shootout_from_db[0].round == 4
    assert shootout_from_db[0].outcome.value == "Over crossbar"
    assert shootout_from_db[0].lineup.full_name == u"Cristiano Ronaldo"
