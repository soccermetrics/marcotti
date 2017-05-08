from sqlalchemy import Column, Integer, Unicode, ForeignKey, Sequence
from sqlalchemy.orm import relationship, backref

from marcotti.models.common import BaseSchema


class Suppliers(BaseSchema):
    __tablename__ = "suppliers"

    id = Column(Integer, Sequence('supplier_id_seq', start=1000), primary_key=True)
    name = Column(Unicode(40), nullable=False)

    def __repr__(self):
        return u"<Supplier(id={0}, name={1})>".format(self.id, self.name).encode('utf-8')


class CompetitionMap(BaseSchema):
    __tablename__ = "competition_mapper"

    id = Column(Integer, ForeignKey('competitions.id'), primary_key=True)
    remote_id = Column(Integer, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('competitions'))

    def __repr__(self):
        return "<CompetitionMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class MatchMap(BaseSchema):
    __tablename__ = "match_mapper"

    id = Column(Integer, ForeignKey('matches.id'), primary_key=True)
    remote_id = Column(Integer, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('matches'))

    def __repr__(self):
        return "<MatchMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class PlayerMap(BaseSchema):
    __tablename__ = "player_mapper"

    id = Column(Integer, ForeignKey('players.id'), primary_key=True)
    remote_id = Column(Integer, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('players'))

    def __repr__(self):
        return "<PlayerMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class PositionMap(BaseSchema):
    __tablename__ = "position_mapper"

    id = Column(Integer, ForeignKey('positions.id'), primary_key=True)
    remote_id = Column(Integer, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('positions'))

    def __repr__(self):
        return "<PositionMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)


class SeasonMap(BaseSchema):
    __tablename__ = "season_mapper"

    id = Column(Integer, ForeignKey('seasons.id'), primary_key=True)
    remote_id = Column(Integer, nullable=False, primary_key=True)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), primary_key=True)

    supplier = relationship('Suppliers', backref=backref('seasons'))

    def __repr__(self):
        return "<SeasonMap(local={}, remote={}, supplier={})>".format(
            self.id, self.remote_id, self.supplier.name)
