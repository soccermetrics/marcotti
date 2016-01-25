from datetime import date

from models.common.overview import (DomesticCompetitions, InternationalCompetitions,
                                    Venues, VenueHistory, Surfaces, Countries, Timezones)
from models.common.enums import ConfederationType
from ..base import BaseCSV


class CompetitionIngest(BaseCSV):

    def parse_file(self, rows):
        insertion_list = []
        for keys in rows:
            name = self.column_unicode("Name", **keys)
            level = self.column_int("Level", **keys)
            country_name = self.column_unicode("Country", **keys)
            confederation_name = self.column_unicode("Confederation", **keys)

            if all(var is not None for var in [country_name, confederation_name]):
                print "Cannot insert Competition record: Country and Confederation defined"
                continue
            else:
                if country_name is not None:
                    country_id = self.get_id(Countries, name=country_name)
                    if country_id is not None:
                        insertion_list.append(DomesticCompetitions(name=name, level=level, country_id=country_id))
                    else:
                        print "Cannot insert Competition record: Country not found"
                        continue
                elif confederation_name is not None:
                    confederation = ConfederationType.from_string(confederation_name)
                    insertion_list.append(InternationalCompetitions(name=name, level=level,
                                                                    confederation=confederation))
                else:
                    print "Cannot insert Competition record: Neither Country nor Confederation defined"
                    continue

            if len(insertion_list) == 50:
                self.session.add_all(insertion_list)
                self.session.commit()
                insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)


class VenueIngest(BaseCSV):

    def __init__(self, session, eff_date):
        super(VenueIngest).__init__(session)
        self.effective_date = date(*tuple(int(x) for x in eff_date.split('-')))

    def parse_file(self, rows):
        print "Ingesting Venues..."
        for keys in rows:
            venue_name = self.column_unicode("Venue Name", **keys)
            city = self.column_unicode("City", **keys)
            region = self.column_unicode("Region", **keys)
            country_name = self.column_unicode("Country", **keys)
            timezone = self.column_unicode("Timezone", **keys)
            latitude = self.column_float("Latitude", **keys)
            longitude = self.column_float("Longitude", **keys)
            altitude = self.column_int("Altitude", **keys)
            config_date = self.column("Config Date", **keys)
            surface_name = self.column("Surface", **keys)
            length = self.column_int("Length", **keys)
            width = self.column_int("Width", **keys)
            capacity = self.column_int("Capacity", **keys)
            seats = self.column_int("Seats", **keys)

            effective_date = date(*tuple(int(x) for x in config_date.split('-'))) \
                if config_date is not None else self.effective_date

            country_id = self.get_id(Countries, name=country_name)
            timezone_id = self.get_id(Timezones, name=timezone)
            surface_id = self.get_id(Surfaces, description=surface_name)

            if not all(var is not None for var in [country_id, timezone_id]):
                print "Cannot insert Venue record: Country or Timezone not defined"
                continue
            if not self.record_exists(Venues, name=venue_name, city=city, country_id=country_id):
                venue_dict = {field: value for (field, value) in zip(
                    ['name', 'city', 'region', 'latitude', 'longitude', 'altitude', 'country_id', 'timezone_id'],
                    [venue_name, city, region, latitude, longitude, altitude, country_id, timezone_id])
                    if value is not None}
                venue_record = Venues(**venue_dict)
                self.session.add(venue_record)
                self.session.commit()
                if not self.record_exists(VenueHistory, venue_id=venue_record.id, date=effective_date):
                    history_dict = {field: value for (field, value) in zip(
                            ['length', 'width', 'capacity', 'seats', 'surface_id'],
                            [length, width, capacity, seats, surface_id])
                            if value is not None}
                    self.session.add(VenueHistory(venue_id=venue_record.id, date=effective_date, **history_dict))
        print "Venue Ingestion complete."
