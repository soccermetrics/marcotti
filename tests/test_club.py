# coding=utf-8
import pytest
from sqlalchemy.exc import DataError

import models.club as mc
import models.common.overview as mco
import models.common.personnel as mcp
import models.common.enums as enums


club_only = pytest.mark.skipif(
    pytest.config.getoption("--schema") != "club",
    reason="Test only valid for club databases"
)


@club_only
def test_club_insert(session):
    club = mc.Clubs(name=u"Arsenal",
                    country=mco.Countries(name=u"England", confederation=enums.ConfederationType.europe))
    session.add(club)

    result = session.query(mc.Clubs).one()
    assert result.name == u"Arsenal"
    assert repr(result) == "<Club(name=Arsenal, country=England)>"


@club_only
def test_club_unicode_insert(session):
    club = mc.Clubs(name=u"Фк Спартак Москва",
                    country=mco.Countries(name=u"Russia", confederation=enums.ConfederationType.europe))
    session.add(club)

    result = session.query(mc.Clubs).join(mco.Countries).filter(mco.Countries.name == u"Russia").one()

    assert result.name == u"Фк Спартак Москва"
    assert unicode(result) == u"<Club(name=Фк Спартак Москва, country=Russia)>"


@club_only
def test_club_name_overflow(session):
    too_long_name = "blahblah" * 8
    too_long_club = mc.Clubs(name=too_long_name,
                             country=mco.Countries(name=u"foo", confederation=enums.ConfederationType.fifa))
    with pytest.raises(DataError):
        session.add(too_long_club)
        session.commit()


@club_only
def test_club_friendly_match_insert(session, club_data):
    friendly_match = mc.ClubFriendlyMatches(**club_data)
    session.add(friendly_match)

    match_from_db = session.query(mc.ClubFriendlyMatches).one()

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


@club_only
def test_club_group_match_insert(session, club_data):
    group_match = mc.ClubGroupMatches(
        group_round=enums.GroupRoundType.group_stage,
        group='A',
        matchday=1,
        **club_data)
    session.add(group_match)

    match_from_db = session.query(mc.ClubGroupMatches).one()

    assert match_from_db.phase == "group"
    assert match_from_db.group_round.value == u"Group Stage"
    assert match_from_db.group == "A"
    assert match_from_db.matchday == 1
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
def test_club_knockout_match_insert(session, club_data):
    knockout_match = mc.ClubKnockoutMatches(
        ko_round=enums.KnockoutRoundType.quarterfinal,
        **club_data)
    session.add(knockout_match)

    match_from_db = session.query(mc.ClubKnockoutMatches).filter(
        mc.ClubKnockoutMatches.ko_round == enums.KnockoutRoundType.quarterfinal)

    assert match_from_db[0].phase == "knockout"
    assert match_from_db[0].ko_round.value == u"Quarterfinal (1/4)"
    assert match_from_db[0].matchday == 1
    assert match_from_db[0].extra_time is False
    assert match_from_db[0].season.name == "2014-2015"
    assert match_from_db[0].competition.name == u"Test Competition"
    assert match_from_db[0].competition.country.name == u"England"
    assert match_from_db[0].venue.name == u"Emirates Stadium"
    assert match_from_db[0].home_team.name == u"Arsenal FC"
    assert match_from_db[0].away_team.name == u"Lincoln City FC"
    assert match_from_db[0].home_manager.full_name == u"Arsène Wenger"
    assert match_from_db[0].away_manager.full_name == u"Gary Simpson"
    assert match_from_db[0].referee.full_name == u"Mark Clattenburg"


@club_only
def test_club_match_lineup_insert(session, club_data, person_data, position_data):
    match = mc.ClubLeagueMatches(matchday=15, **club_data)
    session.add(match)
    player = mcp.Players(position=position_data[0], **person_data['player'][0])
    session.add(player)
    session.commit()

    club_from_db = session.query(mc.Clubs).filter(mc.Clubs.name == u"Arsenal FC").one()

    lineup = mc.ClubMatchLineups(
        match_id=match.id,
        team_id=club_from_db.id,
        player_id=player.id,
        position_id=player.position_id
    )
    session.add(lineup)

    lineup_from_db = session.query(mc.ClubMatchLineups).join(mc.ClubLeagueMatches)\
        .filter(mc.ClubLeagueMatches.id == match.id)

    assert lineup_from_db.count() == 1
    assert unicode(lineup_from_db[0]) == u"<ClubMatchLineup(match={}, player=Miguel Ángel Ponce, team=Arsenal FC, " \
                                         u"position=Left back, starter=False, captain=False)>".format(match.id)


@club_only
def test_club_goal_insert(session, club_data, person_data, position_data):
    match = mc.ClubLeagueMatches(matchday=15, **club_data)
    session.add(match)
    player = mcp.Players(position=position_data[0], **person_data['player'][0])
    session.add(player)
    session.commit()

    club_from_db = session.query(mc.Clubs).filter(mc.Clubs.name == u"Arsenal FC").one()

    lineup = mc.ClubMatchLineups(
        match_id=match.id,
        team_id=club_from_db.id,
        player_id=player.id,
        position_id=player.position_id
    )
    session.add(lineup)
    session.commit()

    goal = mc.ClubGoals(
        lineup_id=lineup.id,
        team_id=club_from_db.id,
        bodypart=enums.BodypartType.head,
        event=enums.ShotEventType.cross_ck,
        time=70
    )
    session.add(goal)

    goals_from_db = session.query(mc.ClubGoals).join(mc.ClubMatchLineups).join(mc.ClubLeagueMatches).filter(
        mc.ClubLeagueMatches.id == match.id
    )

    assert goals_from_db.count() == 1
    assert goals_from_db[0].team.name == u"Arsenal FC"
    assert goals_from_db[0].lineup.full_name == u"Miguel Ángel Ponce"
    assert goals_from_db[0].bodypart.value == "Head"
    assert goals_from_db[0].event.value == "Cross from corner kick"
    assert goals_from_db[0].time == 70


@club_only
def test_club_penalty_shootout_opener_insert(session, club_data):
    match = mc.ClubKnockoutMatches(ko_round=enums.KnockoutRoundType.semifinal, **club_data)
    session.add(match)
    session.commit()

    result = session.query(mc.ClubKnockoutMatches.home_team_id, mc.ClubKnockoutMatches.away_team_id)\
        .filter_by(id=match.id)

    home, away = result[0]

    shootout = mc.ClubPenaltyShootoutOpeners(match_id=match.id, team_id=home)
    session.add(shootout)

    shootout_from_db = session.query(mc.ClubPenaltyShootoutOpeners)\
        .filter(mc.ClubPenaltyShootoutOpeners.match_id == match.id).one()

    assert unicode(shootout_from_db) == u"<ClubPenaltyShootoutOpener(match={}, team=Arsenal FC)>".format(match.id)
