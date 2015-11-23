from copy import deepcopy

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from models.common import BaseSchema
import models.common.overview as mco
import models.common.personnel as mcp
import models.common.match as mcm
import models.common.events as mce


NatlSchema = declarative_base(name="National Teams", metadata=BaseSchema.metadata,
                              class_registry=deepcopy(BaseSchema._decl_class_registry))


class NationalMixin(object):

    @declared_attr
    def team_id(cls):
        return Column(Integer, ForeignKey('countries.id'))


class NationalMatchMixin(object):

    @declared_attr
    def home_team_id(cls):
        return Column(Integer, ForeignKey('countries.id'))

    @declared_attr
    def away_team_id(cls):
        return Column(Integer, ForeignKey('countries.id'))


class FriendlyMixin(object):

    @declared_attr
    def home_team(cls):
        return relationship('Countries', foreign_keys="{}.home_team_id".format(cls.__name__),
                            backref=backref('home_friendly_matches'))

    @declared_attr
    def away_team(cls):
        return relationship('Countries', foreign_keys="{}.away_team_id".format(cls.__name__),
                            backref=backref('away_friendly_matches'))


class GroupMixin(object):

    @declared_attr
    def home_team(cls):
        return relationship('Countries', foreign_keys="{}.home_team_id".format(cls.__name__),
                            backref=backref('home_group_matches'))

    @declared_attr
    def away_team(cls):
        return relationship('Countries', foreign_keys="{}.away_team_id".format(cls.__name__),
                            backref=backref('away_group_matches'))


class KnockoutMixin(object):

    @declared_attr
    def home_team(cls):
        return relationship('Countries', foreign_keys="{}.home_team_id".format(cls.__name__),
                            backref=backref('home_knockout_matches'))

    @declared_attr
    def away_team(cls):
        return relationship('Countries', foreign_keys="{}.away_team_id".format(cls.__name__),
                            backref=backref('away_knockout_matches'))


class NationalFriendlyMatches(FriendlyMixin, NationalMatchMixin, NatlSchema, mcm.Matches):
    __tablename__ = "natl_friendly_matches"
    __mapper_args__ = {'polymorphic_identity': 'friendly'}

    id = Column(Integer, ForeignKey('friendly_matches.id'), primary_key=True)


class NationalGroupMatches(GroupMixin, NationalMatchMixin, NatlSchema, mcm.GroupMatches):
    __tablename__ = "natl_group_matches"
    __mapper_args__ = {'polymorphic_identity': 'group'}

    id = Column(Integer, ForeignKey('group_matches.id'), primary_key=True)


class NationalKnockoutMatches(KnockoutMixin, NationalMatchMixin, NatlSchema, mcm.KnockoutMatches):
    __tablename__ = "natl_knockout_matches"
    __mapper_args__ = {'polymorphic_identity': 'knockout'}

    id = Column(Integer, ForeignKey('knockout_matches.id'), primary_key=True)


class NationalMatchLineups(NationalMixin, NatlSchema, mcm.MatchLineups):
    __tablename__ = "natl_match_lineups"
    __mapper_args__ = {'polymorphic_identity': 'national'}

    id = Column(Integer, ForeignKey('lineups.id'), primary_key=True)

    team = relationship('Countries', foreign_keys="NationalMatchLineups.team_id", backref=backref("lineups"))


class NationalGoals(NationalMixin, NatlSchema, mce.Goals):
    __mapper_args__ = {'polymorphic_identity': 'national'}

    team = relationship('Countries', foreign_keys="NationalGoals.team_id", backref=backref("goals"))


class NationalPenaltyShootoutOpeners(NationalMixin, NatlSchema, mce.PenaltyShootoutOpeners):
    __mapper_args__ = {'polymorphic_identity': 'national'}

    team = relationship('Countries', foreign_keys="NationalPenaltyShootoutOpeners.team_id",
                        backref=backref("shootout_openers"))
