from copy import deepcopy

from sqlalchemy import Column, Integer, Sequence, ForeignKey, Unicode
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr, declarative_base

from models.common import BaseSchema
import models.common.suppliers as mcs
import models.common.overview as mco
import models.common.personnel as mcp
import models.common.match as mcm
import models.common.events as mce


ClubSchema = declarative_base(name="Clubs", metadata=BaseSchema.metadata,
                              class_registry=deepcopy(BaseSchema._decl_class_registry))


class Clubs(ClubSchema):
    __tablename__ = 'clubs'

    id = Column(Integer, Sequence('club_id_seq', start=10000), primary_key=True)

    name = Column(Unicode(60))

    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship('Countries', backref=backref('clubs'))

    def __repr__(self):
        return "<Club(name={0}, country={1})>".format(self.name, self.country.name)

    def __unicode__(self):
        return u"<Club(name={0}, country={1})>".format(self.name, self.country.name)


class ClubMixin(object):

    @declared_attr
    def team_id(cls):
        return Column(Integer, ForeignKey('clubs.id'))


class ClubMatchMixin(object):

    @declared_attr
    def home_team_id(cls):
        return Column(Integer, ForeignKey('clubs.id'))

    @declared_attr
    def away_team_id(cls):
        return Column(Integer, ForeignKey('clubs.id'))


class FriendlyMixin(object):

    @declared_attr
    def home_team(cls):
        return relationship('Clubs', foreign_keys="{}.home_team_id".format(cls.__name__),
                            backref=backref('home_friendly_matches'))

    @declared_attr
    def away_team(cls):
        return relationship('Clubs', foreign_keys="{}.away_team_id".format(cls.__name__),
                            backref=backref('away_friendly_matches'))


class LeagueMixin(object):

    @declared_attr
    def home_team(cls):
        return relationship('Clubs', foreign_keys="{}.home_team_id".format(cls.__name__),
                            backref=backref('home_league_matches'))

    @declared_attr
    def away_team(cls):
        return relationship('Clubs', foreign_keys="{}.away_team_id".format(cls.__name__),
                            backref=backref('away_league_matches'))


class GroupMixin(object):

    @declared_attr
    def home_team(cls):
        return relationship('Clubs', foreign_keys="{}.home_team_id".format(cls.__name__),
                            backref=backref('home_group_matches'))

    @declared_attr
    def away_team(cls):
        return relationship('Clubs', foreign_keys="{}.away_team_id".format(cls.__name__),
                            backref=backref('away_group_matches'))


class KnockoutMixin(object):

    @declared_attr
    def home_team(cls):
        return relationship('Clubs', foreign_keys="{}.home_team_id".format(cls.__name__),
                            backref=backref('home_knockout_matches'))

    @declared_attr
    def away_team(cls):
        return relationship('Clubs', foreign_keys="{}.away_team_id".format(cls.__name__),
                            backref=backref('away_knockout_matches'))


class ClubFriendlyMatches(FriendlyMixin, ClubMatchMixin, ClubSchema, mcm.Matches):
    __tablename__ = "club_friendly_matches"
    __mapper_args__ = {'polymorphic_identity': 'club_friendly'}

    id = Column(Integer, ForeignKey('matches.id'), primary_key=True)

    def __repr__(self):
        return u"<ClubFriendlyMatch(home={}, away={}, competition={}, date={})>".format(
            self.home_team.name, self.away_team.name, self.competition.name, self.date.isoformat()
        ).encode('utf-8')

    def __unicode__(self):
        return u"<ClubFriendlyMatch(home={}, away={}, competition={}, date={})>".format(
            self.home_team.name, self.away_team.name, self.competition.name, self.date.isoformat()
        )


class ClubLeagueMatches(LeagueMixin, ClubMatchMixin, ClubSchema, mcm.LeagueMatches, mcm.Matches):
    __tablename__ = "club_league_matches"
    __mapper_args__ = {'polymorphic_identity': 'league'}

    id = Column(Integer, ForeignKey('matches.id'), primary_key=True)

    def __repr__(self):
        return u"<ClubLeagueMatch(home={}, away={}, competition={}, matchday={}, date={})>".format(
            self.home_team.name, self.away_team.name, self.competition.name, self.matchday, self.date.isoformat()
        ).encode('utf-8')

    def __unicode__(self):
        return u"<ClubLeagueMatch(home={}, away={}, competition={}, matchday={}, date={})>".format(
            self.home_team.name, self.away_team.name, self.competition.name, self.matchday, self.date.isoformat()
        )


class ClubGroupMatches(GroupMixin, ClubMatchMixin, ClubSchema, mcm.GroupMatches, mcm.Matches):
    __tablename__ = "club_group_matches"
    __mapper_args__ = {'polymorphic_identity': 'club_group'}

    id = Column(Integer, ForeignKey('matches.id'), primary_key=True)

    def __repr__(self):
        return u"<ClubGroupMatch(home={}, away={}, competition={}, round={}, group={}, matchday={}, date={})>".format(
            self.home_team.name, self.away_team.name, self.competition.name, self.group_round.value,
            self.group, self.matchday, self.date.isoformat()
        ).encode('utf-8')

    def __unicode__(self):
        return u"<ClubGroupMatch(home={}, away={}, competition={}, round={}, group={}, matchday={}, date={})>".format(
            self.home_team.name, self.away_team.name, self.competition.name, self.group_round.value,
            self.group, self.matchday, self.date.isoformat()
        )


class ClubKnockoutMatches(KnockoutMixin, ClubMatchMixin, ClubSchema, mcm.KnockoutMatches, mcm.Matches):
    __tablename__ = "club_knockout_matches"
    __mapper_args__ = {'polymorphic_identity': 'club_knockout'}

    id = Column(Integer, ForeignKey('matches.id'), primary_key=True)

    def __repr__(self):
        return u"<ClubKnockoutMatch(home={}, away={}, competition={}, round={}, matchday={}, date={})>".format(
            self.home_team.name, self.away_team.name, self.competition.name,
            self.ko_round.value, self.matchday, self.date.isoformat()
        ).encode('utf-8')

    def __unicode__(self):
        return u"<ClubKnockoutMatch(home={}, away={}, competition={}, round={}, matchday={}, date={})>".format(
            self.home_team.name, self.away_team.name, self.competition.name,
            self.ko_round.value, self.matchday, self.date.isoformat()
        )


class ClubMatchLineups(ClubMixin, ClubSchema, mcm.MatchLineups):
    __tablename__ = "club_match_lineups"
    __mapper_args__ = {'polymorphic_identity': 'club'}

    id = Column(Integer, ForeignKey('lineups.id'), primary_key=True)

    team = relationship('Clubs', foreign_keys="ClubMatchLineups.team_id", backref=backref("lineups"))

    def __repr__(self):
        return u"<ClubMatchLineup(match={}, player={}, team={}, position={}, starter={}, captain={})>".format(
            self.match_id, self.full_name, self.team.name, self.position.name, self.is_starting, self.is_captain
        ).encode('utf-8')

    def __unicode__(self):
        return u"<ClubMatchLineup(match={}, player={}, team={}, position={}, starter={}, captain={})>".format(
            self.match_id, self.full_name, self.team.name, self.position.name, self.is_starting, self.is_captain
        )


class ClubGoals(ClubMixin, ClubSchema, mce.Goals):
    __tablename__ = 'club_goals'
    __mapper_args__ = {'polymorphic_identity': 'club'}

    id = Column(Integer, ForeignKey('goals.id'), primary_key=True)

    team = relationship('Clubs', foreign_keys="ClubGoals.team_id", backref=backref("goals"))


class ClubPenaltyShootoutOpeners(ClubMixin, ClubSchema, mce.PenaltyShootoutOpeners):
    __tablename__ = 'club_penalty_shootout_openers'
    __mapper_args__ = {'polymorphic_identity': 'club'}

    match_id = Column(Integer, ForeignKey('penalty_shootout_openers.match_id'), primary_key=True)

    team = relationship('Clubs', foreign_keys="ClubPenaltyShootoutOpeners.team_id",
                        backref=backref("shootout_openers"))

    def __repr__(self):
        return u"<ClubPenaltyShootoutOpener(match={}, team={})>".format(self.match_id, self.team.name).decode('utf-8')

    def __unicode__(self):
        return u"<ClubPenaltyShootoutOpener(match={}, team={})>".format(self.match_id, self.team.name)


class ClubMap(ClubSchema):
    __tablename__ = "club_mapper"

    id = Column(Integer, ForeignKey('clubs.id'), primary_key=True)
    remote_id = Column(Integer, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('clubs'))

    def __repr__(self):
        return "<ClubMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)
