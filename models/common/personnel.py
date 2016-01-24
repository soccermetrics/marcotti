from sqlalchemy import Column, Integer, Numeric, String, Sequence, Date, ForeignKey, Unicode
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy.orm import relationship, backref
from sqlalchemy.schema import CheckConstraint
from sqlalchemy.sql.expression import cast, case

from models.common import BaseSchema
import models.common.enums as enums


class Positions(BaseSchema):
    """
    Football player position data model.
    """
    __tablename__ = 'positions'

    id = Column(Integer, Sequence('position_id_seq', start=10), primary_key=True)
    name = Column(Unicode(20), nullable=False)
    type = Column(enums.PositionType.db_type())

    def __repr__(self):
        return u"<Position(name={0}, type={1})>".format(self.name, self.type.value)


class Persons(BaseSchema):
    """
    Persons common data model.   This model is subclassed by other Personnel data models.
    """
    __tablename__ = 'persons'

    id = Column(Integer, Sequence('person_id_seq', start=100000), primary_key=True)
    first_name = Column(Unicode(40), nullable=False)
    middle_name = Column(Unicode(40))
    last_name = Column(Unicode(40), nullable=False)
    second_last_name = Column(Unicode(40))
    nick_name = Column(Unicode(40))
    birth_date = Column(Date, nullable=False)
    order = Column(enums.NameOrderType.db_type(), default=enums.NameOrderType.western)
    type = Column(String)

    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship('Countries', backref=backref('persons'))

    __mapper_args__ = {
        'polymorphic_identity': 'persons',
        'polymorphic_on': type
    }

    @hybrid_property
    def full_name(self):
        """
        The person's commonly known full name, following naming order conventions.

        If a person has a nickname, that name becomes the person's full name.

        :return: Person's full name.
        """
        if self.nick_name is not None:
            return self.nick_name
        else:
            if self.order == enums.NameOrderType.western:
                return u"{} {}".format(self.first_name, self.last_name)
            elif self.order == enums.NameOrderType.middle:
                return u"{} {} {}".format(self.first_name, self.middle_name, self.last_name)
            elif self.order == enums.NameOrderType.eastern:
                return u"{} {}".format(self.last_name, self.first_name)

    @full_name.expression
    def full_name(cls):
        """
        The person's commonly known full name, following naming order conventions.

        If a person has a nickname, that name becomes the person's full name.

        :return: Person's full name.
        """
        return case(
                [(cls.nick_name != None, cls.nick_name)],
                else_=case(
                    [(cls.order == enums.NameOrderType.middle,
                      cls.first_name + ' ' + cls.middle_name + ' ' + cls.last_name),
                     (cls.order == enums.NameOrderType.eastern,
                      cls.last_name + ' ' + cls.first_name)],
                    else_=cls.first_name + ' ' + cls.last_name
                ))

    @hybrid_property
    def official_name(self):
        """
        The person's legal name, following naming order conventions and with middle names included.

        :return: Person's legal name.
        """
        if self.order == enums.NameOrderType.eastern:
            return u"{} {}".format(self.last_name, self.first_name)
        else:
            return u" ".join([getattr(self, field) for field in
                              ['first_name', 'middle_name', 'last_name', 'second_last_name']
                              if getattr(self, field) is not None])

    @hybrid_method
    def exact_age(self, reference):
        """
        Player's exact age (years + days) relative to a reference date.

        :param reference: Date object of reference date.
        :return: Player's age expressed as a (Year, day) tuple
        """
        delta = reference - self.birth_date
        years = int(delta.days/365.25)
        days = int(delta.days - years*365.25 + 0.5)
        return (years, days)

    @hybrid_method
    def age(self, reference):
        """
        Player's age relative to a reference date.

        :param reference: Date object of reference date.
        :return: Integer value of player's age.
        """
        delta = reference - self.birth_date
        return int(delta.days/365.25)

    @age.expression
    def age(cls, reference):
        """
        Person's age relative to a reference date.

        :param reference: Date object of reference date.
        :return: Integer value of person's age.
        """
        return cast((reference - cls.birth_date)/365.25 - 0.5, Integer)

    def __repr__(self):
        return u"<Person(name={}, country={}, DOB={})>".format(
            self.full_name, self.country.name, self.birth_date.isoformat()).encode('utf-8')


class Players(Persons):
    """
    Players data model.

    Inherits Persons model.
    """
    __tablename__ = 'players'
    __mapper_args__ = {'polymorphic_identity': 'players'}

    player_id = Column(Integer, Sequence('player_id_seq', start=100000), primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))

    position_id = Column(Integer, ForeignKey('positions.id'))
    position = relationship('Positions', backref=backref('players'))

    def __repr__(self):
        return u"<Player(name={}, DOB={}, country={}, position={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name, self.position.name).encode('utf-8')

    def __unicode__(self):
        return u"<Player(name={}, DOB={}, country={}, position={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name, self.position.name)


class PlayerHistory(BaseSchema):
    """
    Player physical history data model.
    """
    __tablename__ = 'player_histories'

    id = Column(Integer, Sequence('player_id_seq', start=1000000), primary_key=True)
    player_id = Column(Integer, ForeignKey('players.player_id'))
    date = Column(Date, doc="Effective date of player physical record")
    height = Column(Numeric(3, 2), CheckConstraint('height >= 0 AND height <= 2.50'), nullable=False,
                    doc="Height of player in meters")
    weight = Column(Numeric(3, 0), CheckConstraint('weight >= 0 AND weight <= 150'), nullable=False,
                    doc="Weight of player in kilograms")

    player = relationship('Players', backref=backref('history'))

    def __repr__(self):
        return u"<PlayerHistory(name={}, date={}, height={:.2f}, weight={:d})>".format(
            self.player.full_name, self.date.isoformat(), self.height, self.weight).encode('utf-8')

    def __unicode__(self):
        return u"<PlayerHistory(name={}, date={}, height={:.2f}, weight={:d})>".format(
            self.player.full_name, self.date.isoformat(), self.height, self.weight)


class Managers(Persons):
    """
    Managers data model.

    Inherits Persons model.
    """
    __tablename__ = 'managers'
    __mapper_args__ = {'polymorphic_identity': 'managers'}

    manager_id = Column(Integer, Sequence('manager_id_seq', start=10000), primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))

    def __repr__(self):
        return u"<Manager(name={}, DOB={}, country={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name).decode('utf-8')

    def __unicode__(self):
        return u"<Manager(name={}, DOB={}, country={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name)


class Referees(Persons):
    """
    Referees data model.

    Inherits Persons model.
    """
    __tablename__ = 'referees'
    __mapper_args__ = {'polymorphic_identity': 'referees'}

    referee_id = Column(Integer, Sequence('referee_id_seq', start=10000), primary_key=True)
    person_id = Column(Integer, ForeignKey('persons.id'))

    def __repr__(self):
        return u"<Referee(name={}, DOB={}, country={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name).encode('utf-8')

    def __unicode__(self):
        return u"<Referee(name={}, DOB={}, country={})>".format(
            self.full_name, self.birth_date.isoformat(), self.country.name)
