# coding=utf-8
import pytest

import marcotti.models.national as mn
import marcotti.models.common.overview as mco
import marcotti.models.common.personnel as mcp
import marcotti.models.common.enums as enums


natl_only = pytest.mark.skipif(
    pytest.config.getoption("--schema") != "natl",
    reason="Test only valid for national team databases"
)


@natl_only
def test_natl_friendly_match_insert(session, national_data):
    friendly_match = mn.NationalFriendlyMatches(**national_data)
    session.add(friendly_match)

    match_from_db = session.query(mn.NationalFriendlyMatches).one()

    assert unicode(match_from_db) == u"<NationalFriendlyMatch(home=France, away=Mexico, " \
                                     u"competition=International Cup, date=1997-11-12)>"
    assert match_from_db.season.name == "1997-1998"
    assert match_from_db.competition.confederation.value == u"FIFA"
    assert match_from_db.venue.name == u"Emirates Stadium"
    assert match_from_db.home_manager.full_name == u"Arsène Wenger"
    assert match_from_db.away_manager.full_name == u"Gary Simpson"
    assert match_from_db.referee.full_name == u"Pierluigi Collina"


@natl_only
def test_natl_group_match_insert(session, national_data):
    group_match = mn.NationalGroupMatches(
        group_round=enums.GroupRoundType.first_round,
        group='C',
        matchday=2,
        **national_data
    )
    session.add(group_match)

    match_from_db = session.query(mn.NationalGroupMatches).one()

    assert unicode(match_from_db) == u"<NationalGroupMatch(home=France, away=Mexico, competition=International Cup, " \
                                     u"round=First Round, group=C, matchday=2, date=1997-11-12)>"
    assert match_from_db.season.name == "1997-1998"
    assert match_from_db.competition.confederation.value == u"FIFA"
    assert match_from_db.venue.name == u"Emirates Stadium"
    assert match_from_db.home_manager.full_name == u"Arsène Wenger"
    assert match_from_db.away_manager.full_name == u"Gary Simpson"
    assert match_from_db.referee.full_name == u"Pierluigi Collina"


@natl_only
def test_natl_knockout_match_insert(session, national_data):
    knockout_match = mn.NationalKnockoutMatches(
        ko_round=enums.KnockoutRoundType.semifinal,
        **national_data
    )
    session.add(knockout_match)

    match_from_db = session.query(mn.NationalKnockoutMatches).filter_by(ko_round=enums.KnockoutRoundType.semifinal)

    assert match_from_db.count() == 1
    assert unicode(match_from_db[0]) == u"<NationalKnockoutMatch(home=France, away=Mexico, " \
                                        u"competition=International Cup, " \
                                        u"round=Semi-Final (1/2), matchday=1, date=1997-11-12)>"
    assert match_from_db[0].season.name == "1997-1998"
    assert match_from_db[0].competition.confederation.value == u"FIFA"
    assert match_from_db[0].venue.name == u"Emirates Stadium"
    assert match_from_db[0].home_manager.full_name == u"Arsène Wenger"
    assert match_from_db[0].away_manager.full_name == u"Gary Simpson"
    assert match_from_db[0].referee.full_name == u"Pierluigi Collina"


@natl_only
def test_natl_match_lineup_insert(session, national_data, person_data, position_data):
    match = mn.NationalGroupMatches(
        group_round=enums.GroupRoundType.first_round,
        group='C',
        matchday=2,
        **national_data
    )
    session.add(match)
    session.commit()

    nation_from_db = session.query(mco.Countries).filter(mco.Countries.name == u"Mexico").one()

    player_data = person_data['player'][0]
    del player_data['country']
    player_data['country_id'] = nation_from_db.id
    player = mcp.Players(position=position_data[0], **player_data)
    session.add(player)
    session.commit()

    lineup = mn.NationalMatchLineups(
        match_id=match.id,
        team_id=nation_from_db.id,
        player_id=player.id,
        position_id=player.position_id
    )
    session.add(lineup)

    lineup_from_db = session.query(mn.NationalMatchLineups).join(mn.NationalGroupMatches).\
        filter(mn.NationalGroupMatches.id == match.id)

    assert lineup_from_db.count() == 1
    assert unicode(lineup_from_db[0]) == u"<NationalMatchLineup(match={}, player=Miguel Ángel Ponce, team=Mexico, " \
                                         u"position=Left back, starter=False, captain=False)>".format(match.id)


@natl_only
def test_natl_goal_insert(session, national_data, person_data, position_data):
    match = mn.NationalKnockoutMatches(
        ko_round=enums.KnockoutRoundType.round_16,
        **national_data
    )
    session.add(match)
    session.commit()

    nation_from_db = session.query(mco.Countries).filter(mco.Countries.name == u"Mexico").one()

    player_data = person_data['player'][0]
    del player_data['country']
    player_data['country_id'] = nation_from_db.id
    player = mcp.Players(position=position_data[0], **player_data)
    session.add(player)
    session.commit()

    lineup = mn.NationalMatchLineups(
        match_id=match.id,
        team_id=nation_from_db.id,
        player_id=player.id,
        position_id=player.position_id
    )
    session.add(lineup)
    session.commit()

    goal = mn.NationalGoals(
        lineup_id=lineup.id,
        team_id=nation_from_db.id,
        bodypart=enums.BodypartType.head,
        event=enums.ShotEventType.cross_ck,
        time=70
    )
    session.add(goal)

    goals_from_db = session.query(mn.NationalGoals).join(mn.NationalMatchLineups)\
        .join(mn.NationalKnockoutMatches).filter(mn.NationalKnockoutMatches.id == match.id)

    assert goals_from_db.count() == 1
    assert goals_from_db[0].team.name == u"Mexico"
    assert goals_from_db[0].lineup.full_name == u"Miguel Ángel Ponce"
    assert goals_from_db[0].bodypart.value == "Head"
    assert goals_from_db[0].event.value == "Cross from corner kick"
    assert goals_from_db[0].time == 70


@natl_only
def test_natl_penalty_shootout_opener_insert(session, national_data):
    match = mn.NationalKnockoutMatches(
        ko_round=enums.KnockoutRoundType.final,
        **national_data
    )
    session.add(match)
    session.commit()

    result = session.query(mn.NationalKnockoutMatches.home_team_id, mn.NationalKnockoutMatches.away_team_id)\
        .filter_by(id=match.id)

    home, away = result[0]

    shootout = mn.NationalPenaltyShootoutOpeners(match_id=match.id, team_id=away)
    session.add(shootout)

    shootout_from_db = session.query(mn.NationalPenaltyShootoutOpeners)\
        .filter(mn.NationalPenaltyShootoutOpeners.match_id == match.id).one()

    assert unicode(shootout_from_db) == u"<NationalPenaltyShootoutOpener(match={}, team=Mexico)>".format(match.id)
