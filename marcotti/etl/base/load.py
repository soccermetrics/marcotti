import uuid
import logging

import marcotti.models.common.suppliers as mcs
import marcotti.models.common.overview as mco
import marcotti.models.common.personnel as mcp
import marcotti.models.common.match as mcm
import marcotti.models.common.events as mce
import marcotti.models.common.statistics as stats
import marcotti.models.club as mc
from .workflows import WorkflowBase


logger = logging.getLogger(__name__)


class MarcottiLoad(WorkflowBase):
    """
    Load transformed data into database.
    """
    def record_exists(self, model, **conditions):
        return self.session.query(model).filter_by(**conditions).count() != 0

    def suppliers(self, data_frame):
        supplier_records = [mcs.Suppliers(**data_row) for idx, data_row in data_frame.iterrows()
                            if not self.record_exists(mcs.Suppliers, name=data_row['name'])]
        self.session.add_all(supplier_records)
        self.session.commit()

    def years(self, data_frame):
        year_records = [mco.Years(**data_row) for idx, data_row in data_frame.iterrows()
                        if not self.record_exists(mco.Years, yr=data_row['yr'])]
        self.session.add_all(year_records)
        self.session.commit()

    def seasons(self, data_frame):
        season_records = []
        map_records = []
        for idx, row in data_frame.iterrows():
            if 'name' not in row:
                if row['start_year'] == row['end_year']:
                    yr_obj = self.session.query(mco.Years).filter_by(yr=row['start_year']).one()
                    if not self.record_exists(mco.Seasons, start_year_id=yr_obj.id, end_year_id=yr_obj.id):
                        season_records.append(mco.Seasons(start_year=yr_obj, end_year=yr_obj))
                else:
                    start_yr_obj = self.session.query(mco.Years).filter_by(yr=row['start_year']).one()
                    end_yr_obj = self.session.query(mco.Years).filter_by(yr=row['end_year']).one()
                    if not self.record_exists(mco.Seasons, start_year_id=start_yr_obj.id, end_year_id=end_yr_obj.id):
                        season_records.append(mco.Seasons(start_year=start_yr_obj, end_year=end_yr_obj))
                self.session.add_all(season_records)
            else:
                if not self.record_exists(mcs.SeasonMap, remote_id=row['remote_id'], supplier_id=self.supplier_id):
                    map_records.append(mcs.SeasonMap(id=self.get_id(mco.Seasons, name=row['name']),
                                                     remote_id=row['remote_id'],
                                                     supplier_id=self.supplier_id))
                self.session.add_all(map_records)
        self.session.commit()

    def countries(self, data_frame):
        remote_ids = []
        country_records = []
        fields = ['name', 'code', 'confederation']
        for idx, row in data_frame.iterrows():
            country_dict = {field: row[field] for field in fields if row[field]}
            if not self.record_exists(mco.Countries, name=row['name']):
                country_records.append(mco.Countries(**country_dict))
                remote_ids.append(row['remote_id'])
        self.session.add_all(country_records)
        self.session.commit()
        map_records = [mcs.CountryMap(id=country_record.id, remote_id=remote_id, supplier_id=self.supplier_id)
                       for remote_id, country_record in zip(remote_ids, country_records) if remote_id]
        self.session.add_all(map_records)
        self.session.commit()

    def competitions(self, data_frame):
        remote_ids = []
        local_ids = []
        comp_records = []
        for idx, row in data_frame.iterrows():
            if 'country_id' in data_frame.columns:
                fields = ['name', 'level', 'country_id']
                comp_dict = {field: row[field] for field in fields if row[field]}
                if not self.record_exists(mco.DomesticCompetitions, **comp_dict):
                    comp_dict.update(id=uuid.uuid4())
                    comp_records.append(mco.DomesticCompetitions(**comp_dict))
                    remote_ids.append(row['remote_id'])
                    local_ids.append(comp_dict['id'])
            elif 'confederation' in data_frame.columns:
                fields = ['name', 'level', 'confederation']
                comp_dict = {field: row[field] for field in fields if row[field]}
                if not self.record_exists(mco.InternationalCompetitions, **comp_dict):
                    comp_dict.update(id=uuid.uuid4())
                    comp_records.append(mco.InternationalCompetitions(**comp_dict))
                    remote_ids.append(row['remote_id'])
                    local_ids.append(comp_dict['id'])
        self.session.bulk_save_objects(comp_records)
        map_records = [mcs.CompetitionMap(id=local_id, remote_id=remote_id, supplier_id=self.supplier_id)
                       for remote_id, local_id in zip(remote_ids, local_ids) if remote_id]
        self.session.bulk_save_objects(map_records)
        self.session.commit()

    def clubs(self, data_frame):
        remote_ids = []
        local_ids = []
        club_records = []
        fields = ['short_name', 'name', 'country_id']
        for idx, row in data_frame.iterrows():
            club_dict = {field: row[field] for field in fields if row[field]}
            if not self.record_exists(mc.Clubs, **club_dict):
                club_dict.update(id=uuid.uuid4())
                club_records.append(mc.Clubs(**club_dict))
                remote_ids.append(row['remote_id'])
                local_ids.append(club_dict['id'])
        self.session.bulk_save_objects(club_records)
        map_records = [mc.ClubMap(id=local_id, remote_id=remote_id, supplier_id=self.supplier_id)
                       for remote_id, local_id in zip(remote_ids, local_ids) if remote_id]
        self.session.bulk_save_objects(map_records)
        self.session.commit()

    def venues(self, data_frame):
        remote_ids = []
        local_ids = []
        venue_records = []
        history_records = []
        fields = ['name', 'city', 'region', 'latitude', 'longitude', 'altitude', 'country_id', 'timezone_id']
        history_fields = ['eff_date', 'length', 'width', 'capacity', 'seats', 'surface_id']
        for idx, row in data_frame.iterrows():
            venue_dict = {field: row[field] for field in fields if row[field]}
            if not self.record_exists(mco.Venues, **venue_dict):
                venue_dict.update(id=uuid.uuid4())
                venue_records.append(mco.Venues(**venue_dict))
                history_dict = {field: row[field] for field in history_fields if row[field]}
                history_records.append(mco.VenueHistory(venue_id=venue_dict['id'], **history_dict))
                remote_ids.append(row['remote_id'])
                local_ids.append(venue_dict['id'])
        self.session.bulk_save_objects(venue_records)
        self.session.bulk_save_objects(history_records)

        map_records = [mcs.VenueMap(id=local_id, remote_id=remote_id, supplier_id=self.supplier_id)
                       for remote_id, local_id in zip(remote_ids, local_ids) if remote_id]
        self.session.bulk_save_objects(map_records)
        self.session.commit()

    def surfaces(self, data_frame):
        surface_records = [mco.Surfaces(**row) for indx, row in data_frame.iterrows()
                           if not self.record_exists(mco.Surfaces, description=row['description'])]
        self.session.add_all(surface_records)
        self.session.commit()

    def timezones(self, data_frame):
        tz_records = [mco.Timezones(**row) for indx, row in data_frame.iterrows()
                      if not self.record_exists(mco.Timezones, name=row['name'])]
        self.session.add_all(tz_records)
        self.session.commit()

    def players(self, data_frame):
        player_set = set()
        player_records = []
        remote_countryids = []
        remote_ids = []
        local_ids = []
        fields = ['known_first_name', 'first_name', 'middle_name', 'last_name', 'second_last_name',
                  'nick_name', 'birth_date', 'order', 'country_id', 'position_id', 'remote_id',
                  'remote_country_id']

        for _, row in data_frame.iterrows():
            player_set.add(tuple([(field, row[field]) for field in fields
                                  if field in row and row[field] is not None]))
        logger.info("{} players in data feed".format(len(player_set)))
        for elements in player_set:
            player_dict = dict(elements)
            remote_id = player_dict.pop('remote_id')
            remote_country_id = player_dict.pop('remote_country_id', None)
            if not self.record_exists(mcs.PlayerMap, remote_id=remote_id):
                if not self.record_exists(mcp.Players, **player_dict):
                    player_dict.update(id=uuid.uuid4(), person_id=uuid.uuid4())
                    player_records.append(mcp.Players(**player_dict))
                    local_ids.append(player_dict['id'])
                    remote_ids.append(remote_id)
                    remote_countryids.append(remote_country_id)
                else:
                    player_id = self.session.query(mcp.Players).filter_by(**player_dict).one().id
                    local_ids.append(player_id)
                    remote_ids.append(remote_id)
            else:
                player_id = self.session.query(mcs.PlayerMap).filter_by(remote_id=remote_id).one().id
                if not self.record_exists(mcp.Players, **player_dict):
                    updated_records = self.session.query(mcp.Players).\
                        filter(mcp.Players.person_id == mcp.Persons.person_id).\
                        filter(mcp.Players.id == player_id)
                    for rec in updated_records:
                        for field, value in player_dict.items():
                            setattr(rec, field, value)
        if self.session.dirty:
            self.session.commit()

        logger.info("{} player records ingested".format(len(player_records)))
        self.session.bulk_save_objects(player_records)
        map_records = [mcs.PlayerMap(id=local_id, remote_id=remote_id, supplier_id=self.supplier_id)
                       for remote_id, local_id in zip(remote_ids, local_ids) if remote_id]
        self.session.bulk_save_objects(map_records)
        self.session.commit()

        for remote_id, player_record in zip(remote_countryids, player_records):
            if remote_id and not self.record_exists(mcs.CountryMap, remote_id=remote_id,
                                                    supplier_id=self.supplier_id):
                self.session.add(mcs.CountryMap(id=player_record.country_id, remote_id=remote_id,
                                                supplier_id=self.supplier_id))
                self.session.commit()

    def managers(self, data_frame):
        manager_records = []
        remote_ids = []
        local_ids = []
        fields = ['known_first_name', 'first_name', 'middle_name', 'last_name', 'second_last_name',
                  'nick_name', 'birth_date', 'order', 'country_id']
        for indx, row in data_frame.iterrows():
            manager_dict = {field: row[field] for field in fields if field in row and row[field]}
            if not self.record_exists(mcs.ManagerMap, remote_id=row['remote_id']):
                if not self.record_exists(mcp.Managers, **manager_dict):
                    manager_dict.update(id=uuid.uuid4(), person_id=uuid.uuid4())
                    manager_records.append(mcp.Managers(**manager_dict))
                    local_ids.append(manager_dict['id'])
                    remote_ids.append(row['remote_id'])
                else:
                    manager_id = self.session.query(mcp.Managers).filter_by(**manager_dict).one().id
                    local_ids.append(manager_id)
                    remote_ids.append(row['remote_id'])
            else:
                manager_id = self.session.query(mcs.ManagerMap).filter_by(remote_id=row['remote_id']).one().id
                if not self.record_exists(mcp.Managers, **manager_dict):
                    updated_records = self.session.query(mcp.Managers).\
                        filter(mcp.Managers.person_id == mcp.Persons.person_id).\
                        filter(mcp.Managers.id == manager_id)
                    for rec in updated_records:
                        for field, value in manager_dict.items():
                            setattr(rec, field, value)
        if self.session.dirty:
            self.session.commit()

        self.session.bulk_save_objects(manager_records)
        map_records = [mcs.ManagerMap(id=local_id, remote_id=remote_id, supplier_id=self.supplier_id)
                       for remote_id, local_id in zip(remote_ids, local_ids) if remote_id]
        self.session.bulk_save_objects(map_records)
        self.session.commit()

    def referees(self, data_frame):
        referee_records = []
        remote_ids = []
        local_ids = []
        fields = ['known_first_name', 'first_name', 'middle_name', 'last_name', 'second_last_name',
                  'nick_name', 'birth_date', 'order', 'country_id']
        for indx, row in data_frame.iterrows():
            referee_dict = {field: row[field] for field in fields if field in row and row[field]}
            if not self.record_exists(mcs.RefereeMap, remote_id=row['remote_id']):
                if not self.record_exists(mcp.Referees, **referee_dict):
                    referee_dict.update(id=uuid.uuid4(), person_id=uuid.uuid4())
                    referee_records.append(mcp.Referees(**referee_dict))
                    remote_ids.append(row['remote_id'])
                    local_ids.append(referee_dict['id'])
                else:
                    referee_id = self.session.query(mcp.Referees).filter_by(**referee_dict).one().id
                    local_ids.append(referee_id)
                    remote_ids.append(row['remote_id'])
            else:
                referee_id = self.session.query(mcs.RefereeMap).filter_by(remote_id=row['remote_id']).one().id
                if not self.record_exists(mcp.Referees, **referee_dict):
                    updated_records = self.session.query(mcp.Referees). \
                        filter(mcp.Referees.person_id == mcp.Persons.person_id). \
                        filter(mcp.Referees.id == referee_id)
                    for rec in updated_records:
                        for field, value in referee_dict.items():
                            setattr(rec, field, value)
        if self.session.dirty:
            self.session.commit()

        self.session.bulk_save_objects(referee_records)
        map_records = [mcs.RefereeMap(id=local_id, remote_id=remote_id, supplier_id=self.supplier_id)
                       for remote_id, local_id in zip(remote_ids, local_ids) if remote_id]
        self.session.bulk_save_objects(map_records)
        self.session.commit()

    def positions(self, data_frame):
        position_record = []
        for indx, row in data_frame.iterrows():
            if row['remote_id'] and self.supplier_id:
                if not self.record_exists(mcs.PositionMap, remote_id=row['remote_id'], supplier_id=self.supplier_id):
                    position_record.append(mcs.PositionMap(
                        id=self.get_id(mcp.Positions, name=row['name']),
                        remote_id=row['remote_id'], supplier_id=self.supplier_id))
            else:
                if not self.record_exists(mcp.Positions, name=row['name']):
                    position_record.append(mcp.Positions(name=row['name'], type=row['type']))
        self.session.add_all(position_record)
        self.session.commit()

    def league_matches(self, data_frame):
        condition_records = []
        match_records = []
        remote_ids = []
        local_ids = []
        fields = ['match_date', 'competition_id', 'season_id', 'venue_id', 'home_team_id', 'away_team_id',
                  'home_manager_id', 'away_manager_id', 'referee_id', 'attendance', 'matchday']
        condition_fields = ['kickoff_time', 'kickoff_temp', 'kickoff_humidity',
                            'kickoff_weather', 'halftime_weather', 'fulltime_weather']
        for idx, row in data_frame.iterrows():
            match_dict = {field: row[field] for field in fields if field in row and row[field] is not None}
            condition_dict = {field: row[field] for field in condition_fields
                              if field in row and row[field] is not None}
            if not self.record_exists(mc.ClubLeagueMatches, **match_dict):
                match_dict.update(id=uuid.uuid4())
                match_records.append(mc.ClubLeagueMatches(**match_dict))
                condition_records.append(mcm.MatchConditions(id=match_dict['id'], **condition_dict))
                remote_ids.append(row['remote_id'])
                local_ids.append(match_dict['id'])

        self.session.bulk_save_objects(match_records)
        self.session.bulk_save_objects(condition_records)

        map_records = [mcs.MatchMap(id=local_id, remote_id=remote_id, supplier_id=self.supplier_id)
                       for remote_id, local_id in zip(remote_ids, local_ids) if remote_id]
        self.session.bulk_save_objects(map_records)
        self.session.commit()

    def knockout_matches(self, data_frame):
        condition_records = []
        match_records = []
        remote_ids = []
        local_ids = []
        fields = ['match_date', 'competition_id', 'season_id', 'venue_id', 'home_team_id', 'away_team_id',
                  'home_manager_id', 'away_manager_id', 'referee_id', 'attendance', 'matchday', 'ko_round',
                  'extra_time']
        condition_fields = ['kickoff_time', 'kickoff_temp', 'kickoff_humidity',
                            'kickoff_weather', 'halftime_weather', 'fulltime_weather']
        for idx, row in data_frame.iterrows():
            match_dict = {field: row[field] for field in fields if field in row and row[field] is not None}
            condition_dict = {field: row[field] for field in condition_fields
                              if field in row and row[field] is not None}
            if not self.record_exists(mc.ClubKnockoutMatches, **match_dict):
                match_dict.update(id=uuid.uuid4())
                match_records.append(mc.ClubKnockoutMatches(**match_dict))
                condition_records.append(mcm.MatchConditions(id=match_dict['id'], **condition_dict))
                remote_ids.append(row['remote_id'])
                local_ids.append(match_dict['id'])

        self.session.bulk_save_objects(match_records)
        self.session.bulk_save_objects(condition_records)

        map_records = [mcs.MatchMap(id=local_id, remote_id=remote_id, supplier_id=self.supplier_id)
                       for remote_id, local_id in zip(remote_ids, local_ids) if remote_id]
        self.session.bulk_save_objects(map_records)
        self.session.commit()

    def match_lineups(self, data_frame):
        lineup_records = []
        fields = ['match_id', 'player_id', 'team_id', 'position_id', 'is_starting', 'is_captain', 'number']
        for idx, row in data_frame.iterrows():
            if not row['player_id']:
                continue
            lineup_dict = {field: row[field] for field in fields if row[field] is not None}
            if not self.record_exists(mc.ClubMatchLineups, **lineup_dict):
                lineup_records.append(mc.ClubMatchLineups(**lineup_dict))
        self.session.add_all(lineup_records)
        self.session.commit()

    def goals(self, data_frame):
        goal_records = []
        fields = ['lineup_id', 'team_id', 'event', 'bodypart', 'time', 'stoppage']
        for idx, row in data_frame.iterrows():
            goal_dict = {field: row[field] for field in fields if row[field] is not None}
            if not self.record_exists(mc.ClubGoals, **goal_dict):
                goal_records.append(mc.ClubGoals(**goal_dict))
        self.session.add_all(goal_records)
        self.session.commit()

    def penalties(self, data_frame):
        penalty_records = []
        fields = ['lineup_id', 'foul', 'outcome', 'time', 'stoppage']
        for idx, row in data_frame.iterrows():
            penalty_dict = {field: row[field] for field in fields if row[field] is not None}
            if not self.record_exists(mce.Penalties, **penalty_dict):
                penalty_records.append(mce.Penalties(**penalty_dict))
        self.session.add_all(penalty_records)
        self.session.commit()

    def bookables(self, data_frame):
        discipline_records = []
        fields = ['lineup_id', 'foul', 'card', 'time', 'stoppage']
        for idx, row in data_frame.iterrows():
            discipline_dict = {field: row[field] for field in fields if row[field] is not None}
            if not self.record_exists(mce.Bookables, **discipline_dict):
                discipline_records.append(mce.Bookables(**discipline_dict))
        self.session.add_all(discipline_records)
        self.session.commit()

    def substitutions(self, data_frame):
        sub_records = []
        fields = ['lineup_in_id', 'lineup_out_id', 'time', 'stoppage']
        for idx, row in data_frame.iterrows():
            sub_dict = {field: row[field] for field in fields if row[field] is not None}
            if not self.record_exists(mce.Substitutions, **sub_dict):
                sub_records.append(mce.Substitutions(**sub_dict))
        self.session.add_all(sub_records)
        self.session.commit()

    def penalty_shootouts(self, data_frame):
        shootout_records = []
        fields = ['lineup_id', 'round', 'num', 'outcome']
        for idx, row in data_frame.iterrows():
            shootout_dict = {field: row[field] for field in fields if row[field] is not None}
            if not self.record_exists(mce.PenaltyShootouts, **shootout_dict):
                shootout_records.append(mce.PenaltyShootouts(**shootout_dict))
        self.session.add_all(shootout_records)
        self.session.commit()


class MarcottiStatLoad(MarcottiLoad):

    @staticmethod
    def is_empty_record(*args):
        """Check for sparseness of statistical record.

        If all quantities of a statistical record are zero, return True.

        If at least one quantity of statistical record is nonzero, return False.
        """
        return not any([arg for arg in args])

    def load_stat_record(self, model, df, field_list):
        """
        Bulk load non-zero records of match statistics data models.
        
        :param model: Data model object
        :param df: Pandas dataframe containing match data
        :param field_list: List of fields in data model
        """
        stat_records = []
        for idx, row in df.iterrows():
            if not self.is_empty_record(*tuple([row[field] for field in field_list])):
                field_list.append('lineup_id')
                stat_dict = {field: row[field] for field in field_list if row[field]}
                stat_records.append(model(**stat_dict))
        self.session.bulk_save_objects(stat_records)
        print("{} {} records from {} lineup records".format(len(stat_records), model.__name__, len(df)))
        self.session.commit()

    def assists(self, data_frame):
        model = stats.Assists
        fields = ['corners', 'freekicks', 'throwins', 'goalkicks', 'setpieces', 'total']
        self.load_stat_record(model, data_frame, fields)

    def clearances(self, data_frame):
        model = stats.Clearances
        fields = ['headed', 'goalline', 'other', 'total']
        self.load_stat_record(model, data_frame, fields)

    def corners(self, data_frame):
        model = stats.Corners
        fields = ['penbox_success', 'penbox_failure', 'left_success', 'left_failure',
                  'right_success', 'right_failure', 'short', 'total']
        self.load_stat_record(model, data_frame, fields)

    def corner_crosses(self, data_frame):
        model = stats.CornerCrosses
        fields = ['total_success', 'total_failure', 'air_success', 'air_failure',
                  'left_success', 'left_failure', 'right_success', 'right_failure']
        self.load_stat_record(model, data_frame, fields)

    def crosses(self, data_frame):
        model = stats.Crosses
        fields = ['air_success', 'air_failure', 'openplay_success', 'openplay_failure',
                  'left_success', 'left_failure', 'right_success', 'right_failure']
        self.load_stat_record(model, data_frame, fields)

    def defensives(self, data_frame):
        model = stats.Defensives
        fields = ['blocks', 'interceptions', 'recoveries', 'corners_conceded', 'fouls_conceded',
                  'challenges_lost', 'handballs_conceded', 'penalties_conceded', 'error_goals', 'error_shots']
        self.load_stat_record(model, data_frame, fields)

    def discipline(self, data_frame):
        model = stats.Discipline
        fields = ['yellows', 'reds']
        self.load_stat_record(model, data_frame, fields)

    def duels(self, data_frame):
        model = stats.Duels
        fields = ['total_won', 'total_lost', 'aerial_won', 'aerial_lost', 'ground_won', 'ground_lost']
        self.load_stat_record(model, data_frame, fields)

    def foul_wins(self, data_frame):
        model = stats.FoulWins
        fields = ['total', 'total_danger', 'total_penalty', 'total_nodanger']
        self.load_stat_record(model, data_frame, fields)

    def freekicks(self, data_frame):
        model = stats.Freekicks
        fields = ['ontarget', 'offtarget']
        self.load_stat_record(model, data_frame, fields)

    def gk_actions(self, data_frame):
        model = stats.GoalkeeperActions
        fields = ['catches', 'punches', 'drops', 'crosses_unclaimed',
                  'distribution_success', 'distribution_failure']
        self.load_stat_record(model, data_frame, fields)

    def gk_allowed_goals(self, data_frame):
        model = stats.GoalkeeperAllowedGoals
        fields = ['insidebox', 'outsidebox', 'is_cleansheet']
        self.load_stat_record(model, data_frame, fields)

    def gk_allowed_shots(self, data_frame):
        model = stats.GoalkeeperAllowedShots
        fields = ['insidebox', 'outsidebox', 'dangerous']
        self.load_stat_record(model, data_frame, fields)

    def gk_saves(self, data_frame):
        model = stats.GoalkeeperSaves
        fields = ['insidebox', 'outsidebox', 'penalty']
        self.load_stat_record(model, data_frame, fields)

    def goal_bodyparts(self, data_frame):
        model = stats.GoalBodyparts
        fields = ['headed', 'leftfoot', 'rightfoot']
        self.load_stat_record(model, data_frame, fields)

    def goal_locations(self, data_frame):
        model = stats.GoalLocations
        fields = ['insidebox', 'outsidebox']
        self.load_stat_record(model, data_frame, fields)

    def goal_totals(self, data_frame):
        model = stats.GoalTotals
        fields = ['is_firstgoal', 'is_winner', 'freekick', 'openplay', 'corners',
                  'throwins', 'penalties', 'substitute', 'other']
        self.load_stat_record(model, data_frame, fields)

    def goalline_clearances(self, data_frame):
        model = stats.GoalLineClearances
        fields = ['insidebox', 'outsidebox', 'totalshots']
        self.load_stat_record(model, data_frame, fields)

    def important_plays(self, data_frame):
        model = stats.ImportantPlays
        fields = ['corners', 'freekicks', 'throwins', 'goalkicks']
        self.load_stat_record(model, data_frame, fields)

    def pass_directions(self, data_frame):
        model = stats.PassDirections
        fields = ['forward', 'backward', 'left_side', 'right_side']
        self.load_stat_record(model, data_frame, fields)

    def pass_lengths(self, data_frame):
        model = stats.PassLengths
        fields = ['short_success', 'short_failure', 'long_success',
                  'long_failure', 'flickon_success', 'flickon_failure']
        self.load_stat_record(model, data_frame, fields)

    def pass_locations(self, data_frame):
        model = stats.PassLocations
        fields = ['ownhalf_success', 'ownhalf_failure', 'opphalf_success', 'opphalf_failure',
                  'defthird_success', 'defthird_failure', 'midthird_success', 'midthird_failure',
                  'finthird_success', 'finthird_failure']
        self.load_stat_record(model, data_frame, fields)

    def pass_totals(self, data_frame):
        model = stats.Passes
        fields = ['total_success', 'total_failure', 'total_no_cc_success', 'total_no_cc_failure',
                  'longball_success', 'longball_failure', 'layoffs_success', 'layoffs_failure',
                  'throughballs', 'important_passes']
        self.load_stat_record(model, data_frame, fields)

    def penalty_actions(self, data_frame):
        model = stats.PenaltyActions
        fields = ['ontarget', 'offtarget', 'taken', 'saved']
        self.load_stat_record(model, data_frame, fields)

    def shot_blocks(self, data_frame):
        model = stats.ShotBlocks
        fields = ['insidebox', 'outsidebox', 'freekick', 'headed', 'leftfoot', 'rightfoot', 'other', 'total']
        self.load_stat_record(model, data_frame, fields)

    def shot_bodyparts(self, data_frame):
        model = stats.ShotBodyparts
        fields = ['head_ontarget', 'head_offtarget', 'left_ontarget',
                  'left_offtarget', 'right_ontarget', 'right_offtarget']
        self.load_stat_record(model, data_frame, fields)

    def shot_locations(self, data_frame):
        model = stats.ShotLocations
        fields = ['insidebox_ontarget', 'insidebox_offtarget', 'outsidebox_ontarget', 'outsidebox_offtarget']
        self.load_stat_record(model, data_frame, fields)

    def shot_plays(self, data_frame):
        model = stats.ShotPlays
        fields = ['openplay_ontarget', 'openplay_offtarget', 'setplay_ontarget', 'setplay_offtarget',
                  'freekick_ontarget', 'freekick_offtarget', 'corners_ontarget', 'corners_offtarget',
                  'throwins_ontarget', 'throwins_offtarget', 'other_ontarget', 'other_offtarget']
        self.load_stat_record(model, data_frame, fields)

    def shot_totals(self, data_frame):
        model = stats.ShotTotals
        fields = ['ontarget', 'offtarget', 'dangerous']
        self.load_stat_record(model, data_frame, fields)

    def tackles(self, data_frame):
        model = stats.Tackles
        fields = ['won', 'lost', 'lastman']
        self.load_stat_record(model, data_frame, fields)

    def throwins(self, data_frame):
        model = stats.Throwins
        fields = ['to_teamplayer', 'top_oppplayer']
        self.load_stat_record(model, data_frame, fields)

    def touch_locations(self, data_frame):
        model = stats.TouchLocations
        fields = ['oppbox', 'oppsix', 'final_third']
        self.load_stat_record(model, data_frame, fields)

    def touches(self, data_frame):
        model = stats.Touches
        fields = ['dribble_overruns', 'dribble_success', 'dribble_failure',
                  'balltouch_success', 'balltouch_failure', 'possession_loss',
                  'total']
        self.load_stat_record(model, data_frame, fields)
