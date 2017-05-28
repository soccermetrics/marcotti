from sqlalchemy import Column, Integer, Boolean, Sequence, ForeignKey
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship, backref

from marcotti.models.common import BaseSchema


class Assists(BaseSchema):
    __name__ = "Assists"
    __tablename__ = "assists"

    id = Column(Integer, Sequence('assist_id_seq', start=1000000), primary_key=True)

    corners = Column(Integer, CheckConstraint('corners >= 0'), default=0)
    freekicks = Column(Integer, CheckConstraint('freekicks >= 0'), default=0)
    throwins = Column(Integer, CheckConstraint('throwins >= 0'), default=0)
    goalkicks = Column(Integer, CheckConstraint('goalkicks >= 0'), default=0)
    setpieces = Column(Integer, CheckConstraint('setpieces >= 0'), default=0)
    total = Column(Integer, CheckConstraint('total >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_assists'))


class Clearances(BaseSchema):
    __name__ = "Clearances"
    __tablename__ = "clearances"

    id = Column(Integer, Sequence('clearance_id_seq', start=1000000), primary_key=True)

    total = Column(Integer, CheckConstraint('total >= 0'), default=0)
    headed = Column(Integer, CheckConstraint('headed >= 0'), default=0)
    other = Column(Integer, CheckConstraint('other >= 0'), default=0)
    goalline = Column(Integer, CheckConstraint('goalline >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_clearances'))


class Corners(BaseSchema):
    __name__ = "Corners"
    __tablename__ = 'corners'

    id = Column(Integer, Sequence('corner_id_seq', start=1000000), primary_key=True)

    penbox_success = Column(Integer, CheckConstraint('penbox_success >= 0'), default=0)
    penbox_failure = Column(Integer, CheckConstraint('penbox_failure >= 0'), default=0)
    left_success = Column(Integer, CheckConstraint('left_success >= 0'), default=0)
    left_failure = Column(Integer, CheckConstraint('left_failure >= 0'), default=0)
    right_success = Column(Integer, CheckConstraint('right_success >= 0'), default=0)
    right_failure = Column(Integer, CheckConstraint('right_failure >= 0'), default=0)
    short = Column(Integer, CheckConstraint('short >= 0'), default=0)
    total = Column(Integer, CheckConstraint('total >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_corners'))


class CornerCrosses(BaseSchema):
    __name__ = "CornerCrosses"
    __tablename__ = 'cornercrosses'

    id = Column(Integer, Sequence('ccross_id_seq', start=1000000), primary_key=True)

    total_success = Column(Integer, CheckConstraint('total_success >= 0'), default=0)
    total_failure = Column(Integer, CheckConstraint('total_failure >= 0'), default=0)
    air_success = Column(Integer, CheckConstraint('air_success >= 0'), default=0)
    air_failure = Column(Integer, CheckConstraint('air_failure >= 0'), default=0)
    left_success = Column(Integer, CheckConstraint('left_success >= 0'), default=0)
    left_failure = Column(Integer, CheckConstraint('left_failure >= 0'), default=0)
    right_success = Column(Integer, CheckConstraint('right_success >= 0'), default=0)
    right_failure = Column(Integer, CheckConstraint('right_failure >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_cornercrosses'))


class Crosses(BaseSchema):
    __name__ = "Crosses"
    __tablename__ = 'crosses'

    id = Column(Integer, Sequence('cross_id_seq', start=1000000), primary_key=True)

    total_success = Column(Integer, CheckConstraint('total_success >= 0'), default=0)
    total_failure = Column(Integer, CheckConstraint('total_failure >= 0'), default=0)
    air_success = Column(Integer, CheckConstraint('air_success >= 0'), default=0)
    air_failure = Column(Integer, CheckConstraint('air_failure >= 0'), default=0)
    openplay_success = Column(Integer, CheckConstraint('openplay_success >= 0'), default=0)
    openplay_failure = Column(Integer, CheckConstraint('openplay_failure >= 0'), default=0)
    left_success = Column(Integer, CheckConstraint('left_success >= 0'), default=0)
    left_failure = Column(Integer, CheckConstraint('left_failure >= 0'), default=0)
    right_success = Column(Integer, CheckConstraint('right_success >= 0'), default=0)
    right_failure = Column(Integer, CheckConstraint('right_failure >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_crosses'))


class Defensives(BaseSchema):
    __name__ = "Defensives"
    __tablename__ = 'defensives'

    id = Column(Integer, Sequence('defensive_id_seq', start=1000000), primary_key=True)

    blocks = Column(Integer, CheckConstraint('blocks >= 0'), default=0)
    interceptions = Column(Integer, CheckConstraint('interceptions >= 0'), default=0)
    recoveries = Column(Integer, CheckConstraint('recoveries >= 0'), default=0)
    corners_conceded = Column(Integer, CheckConstraint('corners_conceded >= 0'), default=0)
    fouls_conceded = Column(Integer, CheckConstraint('fouls_conceded >= 0'), default=0)
    challenges_lost = Column(Integer, CheckConstraint('challenges_lost >= 0'), default=0)
    handballs_conceded = Column(Integer, CheckConstraint('handballs_conceded >= 0'), default=0)
    penalties_conceded = Column(Integer, CheckConstraint('penalties_conceded >= 0'), default=0)
    error_goals = Column(Integer, CheckConstraint('error_goals >= 0'), default=0)
    error_shots = Column(Integer, CheckConstraint('error_shots >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_defensives'))


class Discipline(BaseSchema):
    __name__ = "Discipline"
    __tablename__ = 'discipline'

    id = Column(Integer, Sequence('discipline_id_seq', start=1000000), primary_key=True)

    yellows = Column(Integer, CheckConstraint('yellows >= 0'), default=0)
    reds = Column(Integer, CheckConstraint('reds >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_discipline'))


class Duels(BaseSchema):
    __name__ = "Duels"
    __tablename__ = 'duels'

    id = Column(Integer, Sequence('duel_id_seq', start=1000000), primary_key=True)

    total_won = Column(Integer, CheckConstraint('total_won >= 0'), default=0)
    total_lost = Column(Integer, CheckConstraint('total_lost >= 0'), default=0)
    aerial_won = Column(Integer, CheckConstraint('aerial_won >= 0'), default=0)
    aerial_lost = Column(Integer, CheckConstraint('aerial_lost >= 0'), default=0)
    ground_won = Column(Integer, CheckConstraint('ground_won >= 0'), default=0)
    ground_lost = Column(Integer, CheckConstraint('ground_lost >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_duels'))


class FoulWins(BaseSchema):
    __name__ = "FoulWins"
    __tablename__ = 'foulwins'

    id = Column(Integer, Sequence('foulwin_id_seq', start=1000000), primary_key=True)

    total_danger = Column(Integer, CheckConstraint('total_danger >= 0'), default=0)
    total_penalty = Column(Integer, CheckConstraint('total_penalty >= 0'), default=0)
    total_nodanger = Column(Integer, CheckConstraint('total_nodanger >= 0'), default=0)
    total = Column(Integer, CheckConstraint('total >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_foulwins'))


class Freekicks(BaseSchema):
    __name__ = "Freekicks"
    __tablename__ = 'freekicks'

    id = Column(Integer, Sequence('freekick_id_seq', start=1000000), primary_key=True)

    ontarget = Column(Integer, CheckConstraint('ontarget >= 0'), default=0)
    offtarget = Column(Integer, CheckConstraint('offtarget >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_freekicks'))


class GoalkeeperActions(BaseSchema):
    __name__ = "GoalkeeperActions"
    __tablename__ = 'gk_actions'

    id = Column(Integer, Sequence('gkaction_id_seq', start=1000000), primary_key=True)

    catches = Column(Integer, CheckConstraint('catches >= 0'), default=0)
    punches = Column(Integer, CheckConstraint('punches >= 0'), default=0)
    drops = Column(Integer, CheckConstraint('drops >= 0'), default=0)
    crosses_unclaimed = Column(Integer, CheckConstraint('crosses_unclaimed >= 0'), default=0)
    distribution_success = Column(Integer, CheckConstraint('distribution_success >= 0'), default=0)
    distribution_failure = Column(Integer, CheckConstraint('distribution_failure >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_gkactions'))


class GoalkeeperAllowedGoals(BaseSchema):
    __name__ = "GoalkeeperAllowedGoals"
    __tablename__ = 'gk_allowedgoals'

    id = Column(Integer, Sequence('gkag_id_seq', start=1000000), primary_key=True)

    insidebox = Column(Integer, CheckConstraint('insidebox >= 0'), default=0)
    outsidebox = Column(Integer, CheckConstraint('outsidebox >= 0'), default=0)
    is_cleansheet = Column(Boolean, default=False)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_gkgoals'))


class GoalkeeperAllowedShots(BaseSchema):
    __name__ = "GoalkeeperAllowedShots"
    __tablename__ = 'gk_allowedshots'

    id = Column(Integer, Sequence('gkshot_id_seq', start=1000000), primary_key=True)

    insidebox = Column(Integer, CheckConstraint('insidebox >= 0'), default=0)
    outsidebox = Column(Integer, CheckConstraint('outsidebox >= 0'), default=0)
    dangerous = Column(Integer, CheckConstraint('dangerous >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_gkshots'))


class GoalkeeperSaves(BaseSchema):
    __name__ = "GoalkeeperSaves"
    __tablename__ = 'gk_saves'

    id = Column(Integer, Sequence('gksave_id_seq', start=1000000), primary_key=True)

    insidebox = Column(Integer, CheckConstraint('insidebox >= 0'), default=0)
    outsidebox = Column(Integer, CheckConstraint('outsidebox >= 0'), default=0)
    penalty = Column(Integer, CheckConstraint('penalty >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_gksaves'))


class GoalBodyparts(BaseSchema):
    __name__ = "GoalBodyparts"
    __tablename__ = 'goalbodyparts'

    id = Column(Integer, Sequence('goalbody_id_seq', start=1000000), primary_key=True)

    headed = Column(Integer, CheckConstraint('headed >= 0'), default=0)
    leftfoot = Column(Integer, CheckConstraint('leftfoot >= 0'), default=0)
    rightfoot = Column(Integer, CheckConstraint('rightfoot >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_goal_bodyparts'))


class GoalLocations(BaseSchema):
    __name__ = "GoalLocations"
    __tablename__ = 'goallocations'

    id = Column(Integer, Sequence('goallocation_id_seq', start=1000000), primary_key=True)

    insidebox = Column(Integer, CheckConstraint('insidebox >= 0'), default=0)
    outsidebox = Column(Integer, CheckConstraint('outsidebox >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_goal_locations'))


class GoalTotals(BaseSchema):
    __name__ = "GoalTotals"
    __tablename__ = 'goaltotals'

    id = Column(Integer, Sequence('goaltotal_id_seq', start=1000000), primary_key=True)

    is_firstgoal = Column(Boolean, default=False)
    is_winner = Column(Boolean, default=False)
    freekick = Column(Integer, CheckConstraint('freekick >= 0'), default=0)
    openplay = Column(Integer, CheckConstraint('openplay >= 0'), default=0)
    corners = Column(Integer, CheckConstraint('corners >= 0'), default=0)
    throwins = Column(Integer, CheckConstraint('throwins >= 0'), default=0)
    penalties = Column(Integer, CheckConstraint('penalties >= 0'), default=0)
    substitute = Column(Integer, CheckConstraint('substitute >= 0'), default=0)
    other = Column(Integer, CheckConstraint('other >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_goal_totals'))


class GoalLineClearances(BaseSchema):
    __name__ = "GoalLineClearances"
    __tablename__ = 'goallineclearances'

    id = Column(Integer, Sequence('glclears_id_seq', start=1000000), primary_key=True)

    insidebox = Column(Integer, CheckConstraint('insidebox >= 0'), default=0)
    outsidebox = Column(Integer, CheckConstraint('outsidebox >= 0'), default=0)
    totalshots = Column(Integer, CheckConstraint('totalshots >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_glclearances'))


class ImportantPlays(BaseSchema):
    __name__ = "ImportantPlays"
    __tablename__ = 'importantplays'

    id = Column(Integer, Sequence('keyplay_id_seq', start=1000000), primary_key=True)

    corners = Column(Integer, CheckConstraint('corners >= 0'), default=0)
    freekicks = Column(Integer, CheckConstraint('freekicks >= 0'), default=0)
    throwins = Column(Integer, CheckConstraint('throwins >= 0'), default=0)
    goalkicks = Column(Integer, CheckConstraint('goalkicks >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_imp_plays'))


class Passes(BaseSchema):
    __name__ = "Passes"
    __tablename__ = 'passes'

    id = Column(Integer, Sequence('pass_id_seq', start=1000000), primary_key=True)

    total_success = Column(Integer, CheckConstraint('total_success >= 0'), default=0)
    total_failure = Column(Integer, CheckConstraint('total_failure >= 0'), default=0)
    total_no_cc_success = Column(Integer, CheckConstraint('total_no_cc_success >= 0'), default=0)
    total_no_cc_failure = Column(Integer, CheckConstraint('total_no_cc_failure >= 0'), default=0)
    longball_success = Column(Integer, CheckConstraint('longball_success >= 0'), default=0)
    longball_failure = Column(Integer, CheckConstraint('longball_failure >= 0'), default=0)
    layoffs_success = Column(Integer, CheckConstraint('layoffs_success >= 0'), default=0)
    layoffs_failure = Column(Integer, CheckConstraint('layoffs_failure >= 0'), default=0)
    throughballs = Column(Integer, CheckConstraint('throughballs >= 0'), default=0)
    important_passes = Column(Integer, CheckConstraint('important_passes >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_passes'))


class PassDirections(BaseSchema):
    __name__ = "PassDirections"
    __tablename__ = 'passdirections'

    id = Column(Integer, Sequence('passdir_id_seq', start=1000000), primary_key=True)

    forward = Column(Integer, CheckConstraint('forward >= 0'), default=0)
    backward = Column(Integer, CheckConstraint('backward >= 0'), default=0)
    left_side = Column(Integer, CheckConstraint('left_side >= 0'), default=0)
    right_side = Column(Integer, CheckConstraint('right_side >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_pass_directions'))


class PassLengths(BaseSchema):
    __name__ = "PassLengths"
    __tablename__ = 'passlengths'

    id = Column(Integer, Sequence('passlen_id_seq', start=1000000), primary_key=True)

    short_success = Column(Integer, CheckConstraint('short_success >= 0'), default=0)
    short_failure = Column(Integer, CheckConstraint('short_failure >= 0'), default=0)
    long_success = Column(Integer, CheckConstraint('long_success >= 0'), default=0)
    long_failure = Column(Integer, CheckConstraint('long_failure >= 0'), default=0)
    flickon_success = Column(Integer, CheckConstraint('flickon_success >= 0'), default=0)
    flickon_failure = Column(Integer, CheckConstraint('flickon_failure >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_pass_lengths'))


class PassLocations(BaseSchema):
    __name__ = "PassLocations"
    __tablename__ = 'passlocations'

    id = Column(Integer, Sequence('passloc_id_seq', start=1000000), primary_key=True)

    ownhalf_success = Column(Integer, CheckConstraint('ownhalf_success >= 0'), default=0)
    ownhalf_failure = Column(Integer, CheckConstraint('ownhalf_failure >= 0'), default=0)
    opphalf_success = Column(Integer, CheckConstraint('opphalf_success >= 0'), default=0)
    opphalf_failure = Column(Integer, CheckConstraint('opphalf_failure >= 0'), default=0)
    defthird_success = Column(Integer, CheckConstraint('defthird_success >= 0'), default=0)
    defthird_failure = Column(Integer, CheckConstraint('defthird_failure >= 0'), default=0)
    midthird_success = Column(Integer, CheckConstraint('midthird_success >= 0'), default=0)
    midthird_failure = Column(Integer, CheckConstraint('midthird_failure >= 0'), default=0)
    finthird_success = Column(Integer, CheckConstraint('finthird_success >= 0'), default=0)
    finthird_failure = Column(Integer, CheckConstraint('finthird_failure >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_pass_locations'))


class PenaltyActions(BaseSchema):
    __name__ = "PenaltyActions"
    __tablename__ = 'penaltyactions'

    id = Column(Integer, Sequence('penact_id_seq', start=1000000), primary_key=True)

    taken = Column(Integer, CheckConstraint('taken >= 0'), default=0)
    saved = Column(Integer, CheckConstraint('saved >= 0'), default=0)
    offtarget = Column(Integer, CheckConstraint('offtarget >= 0'), default=0)
    ontarget = Column(Integer, CheckConstraint('ontarget >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_penalty_actions'))


class ShotBodyparts(BaseSchema):
    __name__ = "ShotBodyparts"
    __tablename__ = 'shotbodyparts'

    id = Column(Integer, Sequence('shotbody_id_seq', start=1000000), primary_key=True)

    head_ontarget = Column(Integer, CheckConstraint('head_ontarget >= 0'), default=0)
    head_offtarget = Column(Integer, CheckConstraint('head_offtarget >= 0'), default=0)
    left_ontarget = Column(Integer, CheckConstraint('left_ontarget >= 0'), default=0)
    left_offtarget = Column(Integer, CheckConstraint('left_offtarget >= 0'), default=0)
    right_ontarget = Column(Integer, CheckConstraint('right_ontarget >= 0'), default=0)
    right_offtarget = Column(Integer, CheckConstraint('right_offtarget >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_shotbodyparts'))


class ShotBlocks(BaseSchema):
    __name__ = "ShotBlocks"
    __tablename__ = 'shotblocks'

    id = Column(Integer, Sequence('shotblock_id_seq', start=1000000), primary_key=True)

    freekick = Column(Integer, CheckConstraint('freekick >= 0'), default=0)
    insidebox = Column(Integer, CheckConstraint('insidebox >= 0'), default=0)
    outsidebox = Column(Integer, CheckConstraint('outsidebox >= 0'), default=0)
    headed = Column(Integer, CheckConstraint('headed >= 0'), default=0)
    leftfoot = Column(Integer, CheckConstraint('leftfoot >= 0'), default=0)
    rightfoot = Column(Integer, CheckConstraint('rightfoot >= 0'), default=0)
    other = Column(Integer, CheckConstraint('other >= 0'), default=0)
    total = Column(Integer, CheckConstraint('total >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_shotblocks'))


class ShotLocations(BaseSchema):
    __name__ = "ShotLocations"
    __tablename__ = 'shotlocations'

    id = Column(Integer, Sequence('shotloc_id_seq', start=1000000), primary_key=True)

    insidebox_ontarget = Column(Integer, CheckConstraint('insidebox_ontarget >= 0'), default=0)
    insidebox_offtarget = Column(Integer, CheckConstraint('insidebox_offtarget >= 0'), default=0)
    outsidebox_ontarget = Column(Integer, CheckConstraint('outsidebox_ontarget >= 0'), default=0)
    outsidebox_offtarget = Column(Integer, CheckConstraint('outsidebox_offtarget >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_shotlocations'))


class ShotTotals(BaseSchema):
    __name__ = "ShotTotals"
    __tablename__ = 'shottotals'

    id = Column(Integer, Sequence('shottotals_id_seq', start=1000000), primary_key=True)

    ontarget = Column(Integer, CheckConstraint('ontarget >= 0'), default=0)
    offtarget = Column(Integer, CheckConstraint('offtarget >= 0'), default=0)
    dangerous = Column(Integer, CheckConstraint('dangerous >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_shottotals'))


class ShotPlays(BaseSchema):
    __name__ = "ShotPlays"
    __tablename__ = 'shotplays'

    id = Column(Integer, Sequence('shotplay_id_seq', start=1000000), primary_key=True)

    openplay_ontarget = Column(Integer, CheckConstraint('openplay_ontarget >= 0'), default=0)
    openplay_offtarget = Column(Integer, CheckConstraint('openplay_offtarget >= 0'), default=0)
    setplay_ontarget = Column(Integer, CheckConstraint('setplay_ontarget >= 0'), default=0)
    setplay_offtarget = Column(Integer, CheckConstraint('setplay_offtarget >= 0'), default=0)
    freekick_ontarget = Column(Integer, CheckConstraint('freekick_ontarget >= 0'), default=0)
    freekick_offtarget = Column(Integer, CheckConstraint('freekick_offtarget >= 0'), default=0)
    corners_ontarget = Column(Integer, CheckConstraint('corners_ontarget >= 0'), default=0)
    corners_offtarget = Column(Integer, CheckConstraint('corners_offtarget >= 0'), default=0)
    throwins_ontarget = Column(Integer, CheckConstraint('throwins_ontarget >= 0'), default=0)
    throwins_offtarget = Column(Integer, CheckConstraint('throwins_offtarget >= 0'), default=0)
    other_ontarget = Column(Integer, CheckConstraint('other_ontarget >= 0'), default=0)
    other_offtarget = Column(Integer, CheckConstraint('other_offtarget >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_shotplays'))


class Tackles(BaseSchema):
    __name__ = "Tackles"
    __tablename__ = 'tackles'

    id = Column(Integer, Sequence('tackle_id_seq', start=1000000), primary_key=True)

    won = Column(Integer, CheckConstraint('won >= 0'), default=0)
    lost = Column(Integer, CheckConstraint('lost >= 0'), default=0)
    lastman = Column(Integer, CheckConstraint('lastman >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_tackles'))


class Throwins(BaseSchema):
    __name__ = "Throwins"
    __tablename__ = 'throwins'

    id = Column(Integer, Sequence('throwin_id_seq', start=1000000), primary_key=True)

    to_teamplayer = Column(Integer, CheckConstraint('to_teamplayer >= 0'), default=0)
    to_oppplayer = Column(Integer, CheckConstraint('to_oppplayer >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_throwins'))


class Touches(BaseSchema):
    __name__ = "Touches"
    __tablename__ = 'touches'

    id = Column(Integer, Sequence('touch_id_seq', start=1000000), primary_key=True)

    dribble_overruns = Column(Integer, CheckConstraint('dribble_overruns >= 0'), default=0)
    dribble_success = Column(Integer, CheckConstraint('dribble_success >= 0'), default=0)
    dribble_failure = Column(Integer, CheckConstraint('dribble_failure >= 0'), default=0)
    balltouch_success = Column(Integer, CheckConstraint('balltouch_success >= 0'), default=0)
    balltouch_failure = Column(Integer, CheckConstraint('balltouch_failure >= 0'), default=0)
    possession_loss = Column(Integer, CheckConstraint('possession_loss >= 0'), default=0)
    total = Column(Integer, CheckConstraint('total >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_touches'))


class TouchLocations(BaseSchema):
    __name__ = "TouchLocations"
    __tablename__ = 'touchlocations'

    id = Column(Integer, Sequence('touchloc_id_seq', start=1000000), primary_key=True)

    final_third = Column(Integer, CheckConstraint('final_third >= 0'), default=0)
    oppbox = Column(Integer, CheckConstraint('oppbox >= 0'), default=0)
    oppsix = Column(Integer, CheckConstraint('oppsix >= 0'), default=0)

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('st_touchlocations'))
