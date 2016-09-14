from datetime import date

from sqlalchemy import (case, select, cast, Column, Integer, Numeric, Date,
                        String, Sequence, ForeignKey, Unicode)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.schema import CheckConstraint

from models.common import BaseSchema
import models.common.enums as enums


class Countries(BaseSchema):
    """
    Countries data model.

    Countries are defined as FIFA-affiliated national associations.
    """
    __tablename__ = "countries"

    id = Column(Integer, Sequence('country_id_seq', start=100), primary_key=True)
    name = Column(Unicode(60))
    code = Column(String(3))
    confederation = Column(enums.ConfederationType.db_type())

    def __repr__(self):
        return u"<Country(id={0}, name={1}, trigram={2}, confed={3})>".format(
            self.id, self.name, self.code, self.confederation.value).encode('utf-8')


class Years(BaseSchema):
    """
    Years data model.
    """
    __tablename__ = "years"

    id = Column(Integer, Sequence('year_id_seq', start=100), primary_key=True)
    yr = Column(Integer, unique=True)

    def __repr__(self):
        return "<Year(yr={0})>".format(self.yr)


class Seasons(BaseSchema):
    """
    Seasons data model.
    """
    __tablename__ = "seasons"

    id = Column(Integer, Sequence('season_id_seq', start=100), primary_key=True)

    start_year_id = Column(Integer, ForeignKey('years.id'))
    end_year_id = Column(Integer, ForeignKey('years.id'))

    start_year = relationship('Years', foreign_keys=[start_year_id])
    end_year = relationship('Years', foreign_keys=[end_year_id])

    @hybrid_property
    def name(self):
        """
        List year(s) that make up season.  Seasons over calendar year will be of form YYYY;
        seasons over two years will be of form YYYY-YYYY.
        """
        if self.start_year.yr == self.end_year.yr:
            return self.start_year.yr
        else:
            return "{0}-{1}".format(self.start_year.yr, self.end_year.yr)

    @name.expression
    def name(cls):
        """
        List year(s) that make up season.  Seasons over calendar year will be of form YYYY;
        seasons over two years will be of form YYYY-YYYY.

        This expression allows `name` to be used as a query parameter.
        """
        yr1 = select([Years.yr]).where(cls.start_year_id == Years.id).as_scalar()
        yr2 = select([Years.yr]).where(cls.end_year_id == Years.id).as_scalar()
        return cast(yr1, String) + case([(yr1 == yr2, '')], else_='-'+cast(yr2, String))

    @hybrid_property
    def reference_date(self):
        """
        Define the reference date that is used to calculate player ages.

        +------------------------+---------------------+
        | Season type            | Reference date      |
        +========================+=====================+
        | European (Split years) | 30 June             |
        +------------------------+---------------------+
        | Calendar-year          | 31 December         |
        +------------------------+---------------------+

        :return: Date object that expresses reference date.
        """
        if self.start_year.yr == self.end_year.yr:
            return date(self.end_year.yr, 12, 31)
        else:
            return date(self.end_year.yr, 6, 30)

    def __repr__(self):
        return "<Season({0})>".format(self.name)


class Competitions(BaseSchema):
    """
    Competitions common data model.
    """
    __tablename__ = 'competitions'

    id = Column(Integer, Sequence('competition_id_seq', start=1000), primary_key=True)

    name = Column(Unicode(80))
    level = Column(Integer)
    discriminator = Column('type', String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'competitions',
        'polymorphic_on': discriminator
    }


class DomesticCompetitions(Competitions):
    """
    Domestic Competitions data model, inherited from Competitions model.
    """
    __mapper_args__ = {'polymorphic_identity': 'domestic'}
    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship('Countries', backref=backref('competitions'))

    def __repr__(self):
        return u"<DomesticCompetition(name={0}, country={1}, level={2})>".format(
            self.name, self.country.name, self.level).encode('utf-8')


class InternationalCompetitions(Competitions):
    """
    International Competitions data model, inherited from Competitions model.
    """
    __mapper_args__ = {'polymorphic_identity': 'international'}

    confederation = Column(enums.ConfederationType.db_type())

    def __repr__(self):
        return u"<InternationalCompetition(name={0}, confederation={1})>".format(
            self.name, self.confederation.value).encode('utf-8')


class Venues(BaseSchema):
    __tablename__ = 'venues'

    id = Column(Integer, Sequence('venue_id_seq', start=1000), primary_key=True)

    name = Column(Unicode(60), doc="The name of the match venue")
    city = Column(Unicode(60), doc="Name of city/locality where venue resides")
    region = Column(Unicode(60), doc="Name of administrative region (state, province, etc) where venue resides")
    latitude = Column(Numeric(9, 6), CheckConstraint("latitude >= -90.000000 AND latitude <= 90.000000"),
                      default=0.000000, doc="Venue latitude in decimal degrees")
    longitude = Column(Numeric(9, 6), CheckConstraint("longitude >= -180.000000 AND longitude <= 180.000000"),
                       default=0.000000, doc="Venue longitude in decimal degrees")
    altitude = Column(Integer, CheckConstraint("altitude >= -200 AND altitude <= 4500"),
                      default=0, doc="Venue altitude in meters")

    country_id = Column(Integer, ForeignKey('countries.id'))
    country = relationship('Countries', backref=backref('venues'))
    timezone_id = Column(Integer, ForeignKey('timezones.id'))
    timezone = relationship('Timezones', backref=backref('venues'))

    def __repr__(self):
        return u"<Venue(name={0}, city={1}, country={2})>".format(
            self.name, self.city, self.country.name).encode('utf-8')


class VenueHistory(BaseSchema):
    __tablename__ = 'venue_histories'

    id = Column(Integer, Sequence('venuehist_id_seq', start=10000), primary_key=True)

    date = Column(Date, doc="Effective date of venue configuration")
    length = Column(Integer, CheckConstraint("length >= 90 AND length <= 120"),
                    default=105, doc="Length of venue playing surface in meters")
    width = Column(Integer, CheckConstraint("width >= 45 AND width <= 90"),
                   default=68, doc="Width of venue playing surface in meters")
    capacity = Column(Integer, CheckConstraint("capacity >= 0"),
                      default=0, doc="Total venue capacity (seated and unseated)")
    seats = Column(Integer, CheckConstraint("seats >= 0"),
                   default=0, doc="Total seats at venue")

    venue_id = Column(Integer, ForeignKey('venues.id'))
    venue = relationship('Venues', backref=backref('histories'))
    surface_id = Column(Integer, ForeignKey('surfaces.id'))
    surface = relationship('Surfaces', backref=backref('venues'))

    def __repr__(self):
        return u"<VenueHistory(name={0}, date={1}, length={2}, width={3}, capacity={4})>".format(
            self.venue.name, self.date.isoformat(), self.length, self.width, self.capacity).encode('utf-8')


class Timezones(BaseSchema):
    __tablename__ = 'timezones'

    id = Column(Integer, Sequence('timezone_id_seq', start=1000), primary_key=True)

    name = Column(Unicode(80), doc="Name of the time zone geographic region", nullable=False)
    offset = Column(Numeric(4, 2), doc="Offset of the time zone region from UTC, in decimal hours", nullable=False)
    confederation = Column(enums.ConfederationType.db_type())

    def __repr__(self):
        return u"<Timezone(name={0}, offset={1:+1.2f}, confederation={2})>".format(
           self.name, self.offset, self.confederation.value).encode('utf-8')


class Surfaces(BaseSchema):
    __tablename__ = 'surfaces'

    id = Column(Integer, Sequence('surface_id_seq', start=10), primary_key=True)

    description = Column(Unicode(60), nullable=False)
    type = Column(enums.SurfaceType.db_type())

    def __repr__(self):
        return u"<Surface(description={0}, type={1})>".format(
            self.description, self.type.description).encode('utf-8')
