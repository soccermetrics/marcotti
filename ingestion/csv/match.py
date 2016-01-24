from datetime import date, time

from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from models.common.overview import (Competitions, Seasons, Venues)
from models.common.personnel import (Players, Managers, Referees)
from models.common.match import MatchConditions
from models.common.enums import WeatherConditionType
from models.club import ClubLeagueMatches, ClubMatchLineups, Clubs
from ..base import BaseCSV


class MatchIngest(BaseCSV):

    def __init__(self, session, competition, season):
        super(MatchIngest, self).__init__(session)

        self.competition = competition
        self.season = season

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Matches..."
        for keys in rows:
            match_date = date(*tuple(int(x) for x in self.column("Match Date", **keys).split('-')))
            matchday = self.column_int("Matchday", **keys)
            venue_name = self.column_unicode("Venue", **keys)
            home_team_name = self.column_unicode("Home Team", **keys)
            away_team_name = self.column_unicode("Away Team", **keys)
            home_manager_name = self.column_unicode("Home Manager", **keys)
            away_manager_name = self.column_unicode("Away Manager", **keys)
            referee_name = self.column_unicode("Referee", **keys)
            attendance = self.column_int("Attendance", **keys)
            half_1 = self.column_int("1st Half", **keys)
            half_2 = self.column_int("2nd Half", **keys)
            ko_time = time(*tuple(int(x) for x in self.column("KO Time", **keys).split(':')))
            ko_temp = self.column_float("KO Temp", **keys)
            ko_humid = self.column_float("KO Humidity", **keys)
            ko_wx_desc = self.column("KO Wx", **keys)
            ht_wx_desc = self.column("HT Wx", **keys)
            ft_wx_desc = self.column("FT Wx", **keys)

            ko_weather = WeatherConditionType.from_string(ko_wx_desc) if ko_wx_desc is not None else None
            ht_weather = WeatherConditionType.from_string(ht_wx_desc) if ht_wx_desc is not None else None
            ft_weather = WeatherConditionType.from_string(ft_wx_desc) if ft_wx_desc is not None else None

            try:
                competition_id = self.get_id(Competitions, name=self.competition)
                season_id = self.get_id(Seasons, name=self.season)
                venue_id = self.get_id(Venues, name=venue_name)
                home_team_id = self.get_id(Clubs, name=home_team_name)
                away_team_id = self.get_id(Clubs, name=away_team_name)
                home_manager_id = self.get_id(Managers, full_name=home_manager_name)
                away_manager_id = self.get_id(Managers, full_name=away_manager_name)
                referee_id = self.get_id(Referees, full_name=referee_name)
            except (NoResultFound, MultipleResultsFound):
                continue

            league_dict = {'competition_id': competition_id, 'season_id': season_id, 'matchday': matchday,
                           'home_team_id': home_team_id, 'away_team_id': away_team_id}
            if not self.record_exists(ClubLeagueMatches, **league_dict):
                match_record = ClubLeagueMatches(date=match_date, first_half_length=half_1,
                                                 second_half_length=half_2, attendance=attendance,
                                                 venue_id=venue_id, home_manager_id=home_manager_id,
                                                 away_manager_id=away_manager_id, referee_id=referee_id,
                                                 **league_dict)
                match_condition_record = MatchConditions(match=match_record, kickoff_time=ko_time,
                                                         kickoff_temp=ko_temp, kickoff_humidity=ko_humid,
                                                         kickoff_weather=ko_weather, halftime_weather=ht_weather,
                                                         fulltime_weather=ft_weather)
                insertion_list.append(match_condition_record)
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Match Ingestion complete."


class MatchLineupIngest(BaseCSV):

    def __init__(self, session, competition, season):
        super(MatchLineupIngest, self).__init__(session)

        self.competition = competition
        self.season = season

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Match Lineups..."
        for keys in rows:
            matchday = self.column_int("Matchday", **keys)
            home_team = self.column_unicode("Home Team")
            away_team = self.column_unicode("Away Team")
            player_team = self.column_unicode("Player's Team")
            player_name = self.column_unicode("Player")
            start_flag = self.column_bool("Starting")
            capt_flag = self.column_bool("Captain")

            try:
                competition_id = self.get_id(Competitions, name=self.competition)
                season_id = self.get_id(Seasons, name=self.season)
                home_team_id = self.get_id(Clubs, name=home_team)
                away_team_id = self.get_id(Clubs, name=away_team)
                player_team_id = self.get_id(Clubs, name=player_team)
                if ':' in player_name:
                    player_name, birth_date = player_name.split(':')
                    player_id = self.get_id(Players, full_name=player_name, birth_date=birth_date)
                else:
                    player_id = self.get_id(Players, full_name=player_name)
                position_id = self.session.query(Players).get(player_id).position_id
                match_id = self.get_id(ClubLeagueMatches, competition_id=competition_id, season_id=season_id,
                                       matchday=matchday, home_team_id=home_team_id, away_team_id=away_team_id)
            except (NoResultFound, MultipleResultsFound):
                continue

            if self.record_exists(ClubMatchLineups, match_id=match_id, team_id=player_team_id, player_id=player_id):
                insertion_list.append(ClubMatchLineups, match_id=match_id, team_id=player_team_id,
                                      player_id=player_id, position_id=position_id, is_starting=start_flag,
                                      is_captain=capt_flag)
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Match Ingestion complete."