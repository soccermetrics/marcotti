from datetime import date

from sqlalchemy.orm.exc import NoResultFound

from models.common.suppliers import Suppliers, PlayerMap, PositionMap
from models.common.overview import Countries
from models.common.personnel import Persons, Managers, Referees, Players, Positions, PlayerHistory
from models.common.enums import NameOrderType
from ..base import BaseCSV


class PersonIngest(BaseCSV):

    def get_person_data(self, **keys):
        first_name = self.column_unicode("First Name", **keys)
        middle_name = self.column_unicode("Middle Name", **keys)
        last_name = self.column_unicode("Last Name", **keys)
        second_last_name = self.column_unicode("Second Last Name", **keys)
        nickname = self.column_unicode("Nickname", **keys)
        date_of_birth = self.column("DOB", **keys)
        order = self.column("Name Order", **keys) or "Western"

        name_order = NameOrderType.from_string(order)
        birth_date = date(*tuple(int(x) for x in date_of_birth.split('-')))

        person_dict = {field: value for (field, value) in zip(
            ['first_name', 'middle_name', 'last_name', 'second_last_name', 'nick_name', 'birth_date', 'order'],
            [first_name, middle_name, last_name, second_last_name, nickname, birth_date, name_order])
                if value is not None}
        return person_dict


class PlayerIngest(PersonIngest):

    def __init__(self, session, supplier):
        super(PlayerIngest, self).__init__(session)
        self.supplier_id = self.get_id(Suppliers, name=supplier)

    def parse_file(self, rows):
        print "Ingesting Players..."
        for keys in rows:
            person_tuple = self.get_person_data(**keys)
            remote_id = self.column_int("ID", **keys)
            position = self.column_unicode("Position", **keys)
            country_name = self.column_unicode("Country", **keys)

            try:
                country_id = self.session.query(Countries).filter_by(name=country_name).first().id
            except NoResultFound:
                print u"Country {} does not exist in Marcotti database".format(country_name)
                continue

            try:
                position_id = self.session.query(Positions).filter_by(name=position).first().id
            except NoResultFound:
                print u"Position {} does not exist in Marcotti database".format(position)
                continue

            if not self.record_exists(Players, **person_tuple):
                try:
                    person_id = self.session.query(Persons).filter_by(**person_tuple).first().id
                    player_record = Players(person_id=person_id, position_id=position_id)
                except NoResultFound:
                    player_record = Players(country_id=country_id, position_id=position_id, **person_tuple)
                self.session.add(player_record)
                self.session.commit()
                self.session.add(PlayerMap(id=player_record.id, remote_id=remote_id,
                                           supplier_id=self.supplier_id))
        print "Player Ingestion complete."


class PlayerHistoryIngest(BaseCSV):

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Player History..."
        for keys in rows:
            full_name = self.column_unicode("Player Name", **keys)
            eff_date = self.column("Effective Date", **keys)
            height = self.column_float("Height", **keys)
            weight = self.column_int("Weight", **keys)

            effective_date = date(*tuple(int(x) for x in eff_date.split('-')))

            if self.record_exists(Players, full_name=full_name):
                player_id = self.session.query(Players).filter_by(full_name=full_name).first().player_id
                if not self.record_exists(PlayerHistory, player_id=player_id, date=effective_date):
                    insertion_list.append(PlayerHistory(player_id=player_id, date=effective_date, height=height,
                                                        weight=weight))
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    insertion_list = []
        self.session.add_all(insertion_list)
        print "Player History Ingestion complete."


class ManagerIngest(PersonIngest):

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Managers..."
        for keys in rows:
            person_tuple = self.get_person_data(**keys)
            country_name = self.column_unicode("Country", **keys)

            try:
                country_id = self.session.query(Countries).filter_by(name=country_name).first().id
            except NoResultFound:
                print u"Country {} does not exist in Marcotti database".format(country_name)
                continue

            if not self.record_exists(Managers, **person_tuple):
                try:
                    person_id = self.session.query(Persons).filter_by(**person_tuple).first().id
                    insertion_list.append(Managers(person_id=person_id))
                except NoResultFound:
                    insertion_list.append(Managers(country_id=country_id, **person_tuple))
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Manager Ingestion complete."


class RefereeIngest(PersonIngest):

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Managers..."
        for keys in rows:
            person_tuple = self.get_person_data(**keys)
            country_name = self.column_unicode("Country", **keys)

            try:
                country_id = self.session.query(Countries).filter_by(name=country_name).first().id
            except NoResultFound:
                print u"Country {} does not exist in Marcotti database".format(country_name)
                continue

            if not self.record_exists(Referees, **person_tuple):
                try:
                    person_id = self.session.query(Persons).filter_by(**person_tuple).first().id
                    insertion_list.append(Referees(person_id=person_id))
                except NoResultFound:
                    insertion_list.append(Referees(country_id=country_id, **person_tuple))
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Referee Ingestion complete."


class PositionMapIngest(BaseCSV):

    def __init__(self, session, supplier):
        super(PositionMapIngest, self).__init__(session)
        self.supplier_id = self.get_id(Suppliers, name=supplier)

    def parse_file(self, rows):
        for keys in rows:
            remote_id = self.column_int("ID", **keys)
            position = self.column_unicode("Position", **keys)

            local_id = self.get_id(Positions, name=position)

            mapper_dict = dict(id=local_id, remote_id=remote_id, supplier_id=self.supplier_id)
            if not self.record_exists(PositionMap, **mapper_dict):
                self.session.add(PositionMap(**mapper_dict))
        print "Position Mapper Ingest complete."
