from models.club import ClubGoals, ClubLeagueMatches, Clubs, ClubMatchLineups
from models.common.overview import Competitions, Seasons
from models.common.personnel import Players
from models.common.events import (Bookables, Penalties, Substitutions)
from models.common import enums as enums
from ..base import BaseCSV


class EventsIngest(BaseCSV):

    def __init__(self, session, competition, season):
        super(EventsIngest, self).__init__(session)

        self.competition = competition
        self.season = season

        self.competition_id = self.get_id(Competitions, name=self.competition)
        self.season_id = self.get_id(Seasons, name=self.season)
        if any(var is None for var in [self.competition_id, self.season_id]):
            raise Exception("Fatal Error: Competition and/or Season not in Marcotti database!")

    def parse_file(self, rows):
        raise NotImplementedError


class GoalIngest(EventsIngest):

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Goals..."

        for keys in rows:
            matchday = self.column_int("Matchday", **keys)
            home_team_name = self.column_unicode("Home Team", **keys)
            away_team_name = self.column_unicode("Away Team", **keys)
            scoring_team = self.column_unicode("Team", **keys)
            scorer_name = self.column_unicode("Player", **keys)
            scoring_event = self.column("Event", **keys) or "Unknown"
            bodypart_desc = self.column("Bodypart", **keys) or "Unknown"
            match_time = self.column_int("Time", **keys)
            stoppage_time = self.column_int("Stoppage", **keys) or 0

            home_team_id = self.get_id(Clubs, name=home_team_name)
            away_team_id = self.get_id(Clubs, name=away_team_name)
            goal_team_id = self.get_id(Clubs, name=scoring_team)
            player_id = self.get_id(Players, full_name=scorer_name)
            match_id = self.get_id(ClubLeagueMatches, competition_id=self.competition_id, season_id=self.season_id,
                                   matchday=matchday, home_team_id=home_team_id, away_team_id=away_team_id)
            goal_event = enums.ShotEventType.from_string(scoring_event)
            bodypart = enums.BodypartType.from_string(bodypart_desc)
            lineup_id = self.get_id(ClubMatchLineups, match_id=match_id, player_id=player_id)

            if match_id is None:
                print "Error: No match for {} vs {} in matchday {} of {} {}".format(
                    home_team_name, away_team_name, matchday, self.season, self.competition)
                continue
            if goal_team_id not in [home_team_id, away_team_id]:
                print "Scoring team {} does not match {} or {}".format(
                    scoring_team, home_team_name, away_team_name)
                continue
            if lineup_id is None:
                print "Player {} not in lineup of {} vs {}".format(scorer_name, home_team_name, away_team_name)
                continue
            goal_dict = {'lineup_id': lineup_id, 'team_id': goal_team_id, 'event': goal_event,
                         'bodypart': bodypart, 'time': match_time, 'stoppage': stoppage_time}
            if not self.record_exists(ClubGoals, **goal_dict):
                insertion_list.append(ClubGoals(**goal_dict))
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Goal Ingestion complete."


class PenaltyIngest(EventsIngest):

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Penalties..."

        for keys in rows:
            matchday = self.column_int("Matchday", **keys)
            home_team_name = self.column_unicode("Home Team", **keys)
            away_team_name = self.column_unicode("Away Team", **keys)
            penalty_taker = self.column_unicode("Penalty Taker", **keys)
            penalty_foul = self.column("Foul", **keys) or "Unknown"
            penalty_outcome = self.column("Outcome", **keys)
            match_time = self.column_int("Time", **keys)
            stoppage_time = self.column_int("Stoppage", **keys) or 0

            home_team_id = self.get_id(Clubs, name=home_team_name)
            away_team_id = self.get_id(Clubs, name=away_team_name)
            player_id = self.get_id(Players, full_name=penalty_taker)
            match_id = self.get_id(ClubLeagueMatches, competition_id=self.competition_id, season_id=self.season_id,
                                   matchday=matchday, home_team_id=home_team_id, away_team_id=away_team_id)
            foul_event = enums.FoulEventType.from_string(penalty_foul)
            outcome = enums.ShotOutcomeType.from_string(penalty_outcome)
            lineup_id = self.get_id(ClubMatchLineups, match_id=match_id, player_id=player_id)

            if match_id is None:
                print "Error: No match for {} vs {} in matchday {} of {} {}".format(
                    home_team_name, away_team_name, matchday, self.season, self.competition)
                continue
            if lineup_id is None:
                print "Player {} not in lineup of {} vs {}".format(penalty_taker, home_team_name, away_team_name)
                continue
            penalty_dict = {'lineup_id': lineup_id, 'foul': foul_event, 'outcome': outcome,
                            'time': match_time, 'stoppage': stoppage_time}
            if not self.record_exists(Penalties, **penalty_dict):
                insertion_list.append(Penalties(**penalty_dict))
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Penalty Ingestion complete."


class BookableIngest(EventsIngest):

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Bookable Events..."

        for keys in rows:
            matchday = self.column_int("Matchday", **keys)
            home_team_name = self.column_unicode("Home Team", **keys)
            away_team_name = self.column_unicode("Away Team", **keys)
            player_name = self.column_unicode("Player", **keys)
            foul = self.column("Foul", **keys) or "Unknown"
            card = self.column("Card", **keys)
            match_time = self.column_int("Time", **keys)
            stoppage_time = self.column_int("Stoppage", **keys) or 0

            home_team_id = self.get_id(Clubs, name=home_team_name)
            away_team_id = self.get_id(Clubs, name=away_team_name)
            player_id = self.get_id(Players, full_name=player_name)
            match_id = self.get_id(ClubLeagueMatches, competition_id=self.competition_id, season_id=self.season_id,
                                   matchday=matchday, home_team_id=home_team_id, away_team_id=away_team_id)
            foul_event = enums.FoulEventType.from_string(foul)
            card_type = enums.CardType.from_string(card)
            lineup_id = self.get_id(ClubMatchLineups, match_id=match_id, player_id=player_id)

            if match_id is None:
                print "Error: No match for {} vs {} in matchday {} of {} {}".format(
                    home_team_name, away_team_name, matchday, self.season, self.competition)
                continue
            if lineup_id is None:
                print "Player {} not in lineup of {} vs {}".format(player_name, home_team_name, away_team_name)
                continue
            booking_dict = {'lineup_id': lineup_id, 'foul': foul_event, 'card': card_type,
                            'time': match_time, 'stoppage': stoppage_time}
            if not self.record_exists(Bookables, **booking_dict):
                insertion_list.append(Bookables(**booking_dict))
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Bookable Event Ingestion complete."


class SubstitutionIngest(EventsIngest):

    def parse_file(self, rows):
        insertion_list = []
        print "Ingesting Substitutions..."
        for keys in rows:
            matchday = self.column_int("Matchday", **keys)
            home_team_name = self.column_unicode("Home Team", **keys)
            away_team_name = self.column_unicode("Away Team", **keys)
            in_player_name = self.column_unicode("Player In", **keys)
            out_player_name = self.column_unicode("Player Out", **keys)
            match_time = self.column_int("Time", **keys)
            stoppage_time = self.column_int("Stoppage", **keys) or 0

            home_team_id = self.get_id(Clubs, name=home_team_name)
            away_team_id = self.get_id(Clubs, name=away_team_name)
            in_player_id = self.get_id(Players, full_name=in_player_name)
            out_player_id = self.get_id(Players, full_name=out_player_name)
            match_id = self.get_id(ClubLeagueMatches, competition_id=self.competition_id, season_id=self.season_id,
                                   matchday=matchday, home_team_id=home_team_id, away_team_id=away_team_id)
            in_lineup_id = self.get_id(ClubMatchLineups, match_id=match_id, player_id=in_player_id)
            out_lineup_id = self.get_id(ClubMatchLineups, match_id=match_id, player_id=out_player_id)

            if match_id is None:
                print "Error: No match for {} vs {} in matchday {} of {} {}".format(
                    home_team_name, away_team_name, matchday, self.season, self.competition)
                continue
            if out_lineup_id is None:
                print "Player {} not in lineup of {} vs {}".format(out_player_name, home_team_name, away_team_name)
                continue
            if in_lineup_id is None:
                print "No player entering - player {} is being withdrawn from {} vs {}".format(
                    out_player_name, home_team_name, away_team_name)
            substitution_dict = {field: value for field, value in zip(
                ['lineup_in_id', 'lineup_out_id', 'time', 'stoppage'],
                [in_lineup_id, out_lineup_id, match_time, stoppage_time])
                if value is not None}
            if not self.record_exists(Substitutions, **substitution_dict):
                insertion_list.append(Substitutions(**substitution_dict))
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
        print "Substitution Ingestion complete."
