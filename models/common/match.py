from sqlalchemy import (Column, Integer, Numeric, Date, Time,
                        String, Sequence, ForeignKey, Boolean)
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr

from models.common import BaseSchema
import models.common.enums as enums


class Matches(BaseSchema):
    """
    Matches common data model.
    """
    __tablename__ = "matches"

    id = Column(Integer, Sequence('match_id_seq', start=1000000), primary_key=True)

    date = Column(Date)
    first_half_length = Column(Integer, CheckConstraint('first_half_length > 0'), default=45)
    second_half_length = Column(Integer, CheckConstraint('second_half_length >= 0'), default=45)
    first_extra_length = Column(Integer, CheckConstraint('first_extra_length >= 0'), default=0)
    second_extra_length = Column(Integer, CheckConstraint('second_extra_length >= 0'), default=0)
    attendance = Column(Integer, CheckConstraint('attendance >= 0'), default=0)
    phase = Column(String)

    competition_id = Column(Integer, ForeignKey('competitions.id'))
    season_id = Column(Integer, ForeignKey('seasons.id'))
    venue_id = Column(Integer, ForeignKey('venues.id'))
    referee_id = Column(Integer, ForeignKey('referees.referee_id'))
    home_manager_id = Column(Integer, ForeignKey('managers.manager_id'))
    away_manager_id = Column(Integer, ForeignKey('managers.manager_id'))

    competition = relationship('Competitions', backref=backref('matches', lazy='dynamic'))
    season = relationship('Seasons', backref=backref('matches'))
    venue = relationship('Venues', backref=backref('matches', lazy='dynamic'))
    referee = relationship('Referees', backref=backref('matches'))
    home_manager = relationship('Managers', foreign_keys=[home_manager_id], backref=backref('home_matches'))
    away_manager = relationship('Managers', foreign_keys=[away_manager_id], backref=backref('away_matches'))

    __mapper_args__ = {
        'polymorphic_identity': 'matches',
        'polymorphic_on': phase
    }


class MatchConditions(BaseSchema):
    __tablename__ = 'match_conditions'

    id = Column(Integer, ForeignKey('matches.id'), primary_key=True)

    kickoff_time = Column(Time)
    kickoff_temp = Column(Numeric(3, 1), CheckConstraint('kickoff_temp >= -15.0 AND kickoff_temp <= 50.0'))
    kickoff_weather = Column(enums.WeatherConditionType.db_type())
    halftime_weather = Column(enums.WeatherConditionType.db_type())
    fulltime_weather = Column(enums.WeatherConditionType.db_type())

    match = relationship('Matches', backref=backref('conditions'))

    def __repr__(self):
        return "<MatchCondition(id={}, kickoff={}, temp={}, kickoff_weather={})>".format(
            self.id, self.kickoff_time.strftime("%H:%M"), self.kickoff_temp, self.kickoff_weather.value
        )


class LeagueMatches(BaseSchema):
    """
    League Matches data model.

    Inherited from Matches model.
    """
    __abstract__ = True

    matchday = Column(Integer)


class GroupMatches(BaseSchema):
    """
    Group Matches data model.

    Inherited from Matches model.
    """
    __abstract__ = True

    matchday = Column(Integer)
    group = Column(String(length=2))

    @declared_attr
    def group_round_id(cls):
        return Column(Integer, ForeignKey('group_rounds.id'))

    @declared_attr
    def group_round(cls):
        return relationship('GroupRounds')


class KnockoutMatches(BaseSchema):
    """
    Knockout Matches data model.

    Inherited from Matches model.
    """
    __abstract__ = True

    matchday = Column(Integer)
    extra_time = Column(Boolean, default=False)

    @declared_attr
    def ko_round_id(cls):
        return Column(Integer, ForeignKey('knockout_rounds.id'))

    @declared_attr
    def ko_round(cls):
        return relationship('KnockoutRounds')


class MatchLineups(BaseSchema):
    """
    Match Lineups common data model.
    """
    __tablename__ = 'lineups'

    id = Column(Integer, Sequence('lineup_id_seq', start=1000000), primary_key=True)

    is_starting = Column(Boolean, default=False)
    is_captain = Column(Boolean, default=False)
    type = Column(String)

    match_id = Column(Integer, ForeignKey('matches.id'))
    player_id = Column(Integer, ForeignKey('players.player_id'))
    position_id = Column(Integer, ForeignKey('positions.id'))

    match = relationship('Matches', backref=backref('lineups'))
    player = relationship('Players', backref=backref('lineups'))
    position = relationship('Positions')

    __mapper_args__ = {
        'polymorphic_identity': 'lineups',
        'polymorphic_on': type
    }
