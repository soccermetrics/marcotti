from models.common.overview import Countries, Timezones, Surfaces
from models.common.personnel import Positions
from models.common.enums import ConfederationType, PositionType, SurfaceType
from ..base import BaseCSV


class CountryIngest(BaseCSV):

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Countries..."
        for keys in rows:
            country_name = "{name}".format(**keys).strip().decode('utf-8')
            confederation = "{confederation}".format(**keys).strip()
            if not self.record_exists(Countries, name=country_name):
                insertion_list.append(Countries(
                        name=country_name, confederation=ConfederationType.from_string(confederation)))
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Country Ingestion complete."


class TimezoneIngest(BaseCSV):

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Timezones..."
        for keys in rows:
            timezone_region = "{name}".format(**keys).strip().decode('utf-8')
            confederation = "{confederation}".format(**keys).strip()
            offset = float("{offset}".format(**keys).strip())
            if not self.record_exists(Timezones, name=timezone_region):
                insertion_list.append(Timezones(
                        name=timezone_region, offset=offset,
                        confederation=ConfederationType.from_string(confederation)))
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Timezone Ingestion complete."


class PositionIngest(BaseCSV):

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Positions..."
        for keys in rows:
            position_name = "{name}".format(**keys).strip().decode('utf-8')
            position_type = "{type}".format(**keys).strip()
            if not self.record_exists(Positions, name=position_name):
                insertion_list.append(Positions(name=position_name, type=PositionType.from_string(position_type)))
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Position Ingestion complete."


class SurfaceIngest(BaseCSV):

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Surfaces..."
        for keys in rows:
            surface_name = "{description}".format(**keys).strip().decode('utf-8')
            surface_type = "{type}".format(**keys).strip()
            if self.record_exists(Surfaces, description=surface_name):
                insertion_list.append(Surfaces(description=surface_name, type=SurfaceType.from_string(surface_type)))
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Surface Ingestion complete."
