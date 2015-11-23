from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.orm import relationship, backref

from models.common import BaseSchema
import models.common.enums as enums


class MatchTimeMixin(object):
    time = Column(Integer, CheckConstraint('time > 0 AND time <= 120'), nullable=False)
    stoppage = Column(Integer, CheckConstraint('stoppage >= 0 AND stoppage < 20'), default=0)


class Goals(MatchTimeMixin, BaseSchema):
    __tablename__ = "goals"

    id = Column(Integer, Sequence('goal_id_seq', start=100000), primary_key=True)

    domain = Column(String)
    bodypart = Column(enums.BodypartType.db_type())
    event = Column(enums.ShotEventType.db_type())

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('goals'))

    __mapper_args__ = {
        'polymorphic_identity': 'goals',
        'polymorphic_on': domain
    }


class Penalties(MatchTimeMixin, BaseSchema):
    __tablename__ = "penalties"

    id = Column(Integer, Sequence('penalty_id_seq', start=100000), primary_key=True)

    foul = Column(enums.FoulEventType.db_type())
    outcome = Column(enums.ShotOutcomeType.db_type())

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('penalties'))


class Bookables(MatchTimeMixin, BaseSchema):
    __tablename__ = "bookable_offenses"

    id = Column(Integer, Sequence('bookable_id_seq', start=100000), primary_key=True)

    foul = Column(enums.FoulEventType.db_type())
    card = Column(enums.CardType.db_type())

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('bookables'))


class Substitutions(MatchTimeMixin, BaseSchema):
    __tablename__ = "substitutions"

    id = Column(Integer, Sequence('substitution_id_seq', start=100000), primary_key=True)

    lineup_in_id = Column(Integer, ForeignKey('lineups.id'), nullable=True)
    lineup_out_id = Column(Integer, ForeignKey('lineups.id'))

    lineup_in = relationship('MatchLineups', foreign_keys=[lineup_in_id], backref=backref('subbed_in'))
    lineup_out = relationship('MatchLineups', foreign_keys=[lineup_in_id], backref=backref('subbed_out'))


class PenaltyShootouts(BaseSchema):
    __tablename__ = "penalty_shootouts"

    id = Column(Integer, Sequence('shootout_id_seq', start=100000), primary_key=True)

    round = Column(Integer)
    outcome = Column(enums.ShotOutcomeType.db_type())

    lineup_id = Column(Integer, ForeignKey('lineups.id'))
    lineup = relationship('MatchLineups', backref=backref('shootouts'))


class PenaltyShootoutOpeners(BaseSchema):
    __tablename__ = "penalty_shootout_openers"

    match_id = Column(Integer, ForeignKey('matches.id'), primary_key=True)
    domain = Column(String)

    __mapper_args__ = {
        'polymorphic_identity': 'penalty_shootout_openers',
        'polymorphic_on': domain
    }
