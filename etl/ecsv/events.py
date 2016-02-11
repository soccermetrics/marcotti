from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

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
        inserts = 0
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

            goal_event = enums.ShotEventType.from_string(scoring_event)
            bodypart = enums.BodypartType.from_string(bodypart_desc)

            try:
                home_team_id = self.get_id(Clubs, name=home_team_name)
                away_team_id = self.get_id(Clubs, name=away_team_name)
                goal_team_id = self.get_id(Clubs, name=scoring_team)
            except (NoResultFound, MultipleResultsFound):
                continue
            if goal_team_id not in [home_team_id, away_team_id]:
                print "Scoring team {} does not match {} or {}".format(
                    scoring_team, home_team_name, away_team_name)
                continue

            try:
                match_id = self.get_id(ClubLeagueMatches, competition_id=self.competition_id, season_id=self.season_id,
                                       matchday=matchday, home_team_id=home_team_id, away_team_id=away_team_id)
            except (NoResultFound, MultipleResultsFound):
                print "Error: No match for {} vs {} in matchday {} of {} {}".format(
                    home_team_name, away_team_name, matchday, self.season, self.competition)
                continue

            try:
                if ':' in scorer_name:
                    player_name, birth_date = scorer_name.split(':')
                    player_id = self.get_id(Players, full_name=player_name, birth_date=birth_date)
                else:
                    player_id = self.get_id(Players, full_name=scorer_name)
                lineup_id = self.get_id(ClubMatchLineups, match_id=match_id, player_id=player_id)
            except (NoResultFound, MultipleResultsFound):
                print "Player {} not in lineup of {} vs {}".format(scorer_name, home_team_name, away_team_name)
                continue

            goal_dict = {'lineup_id': lineup_id, 'team_id': goal_team_id, 'event': goal_event,
                         'bodypart': bodypart, 'time': match_time, 'stoppage': stoppage_time}
            if not self.record_exists(ClubGoals, **goal_dict):
                insertion_list.append(ClubGoals(**goal_dict))
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    inserts += 50
                    print "{} goals inserted".format(inserts)
                    insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
            self.session.commit()
        print "Goal Ingestion complete."


class PenaltyIngest(EventsIngest):

    def parse_file(self, rows):
        inserts = 0
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

            foul_event = enums.FoulEventType.from_string(penalty_foul)
            outcome = enums.ShotOutcomeType.from_string(penalty_outcome)

            try:
                home_team_id = self.get_id(Clubs, name=home_team_name)
                away_team_id = self.get_id(Clubs, name=away_team_name)
            except (NoResultFound, MultipleResultsFound):
                continue

            try:
                match_id = self.get_id(ClubLeagueMatches, competition_id=self.competition_id, season_id=self.season_id,
                                       matchday=matchday, home_team_id=home_team_id, away_team_id=away_team_id)
            except (NoResultFound, MultipleResultsFound):
                print "Error: No match for {} vs {} in matchday {} of {} {}".format(
                    home_team_name, away_team_name, matchday, self.season, self.competition)
                continue

            try:
                if ':' in penalty_taker:
                    player_name, birth_date = penalty_taker.split(':')
                    player_id = self.get_id(Players, full_name=player_name, birth_date=birth_date)
                else:
                    player_id = self.get_id(Players, full_name=penalty_taker)
                lineup_id = self.get_id(ClubMatchLineups, match_id=match_id, player_id=player_id)
            except (NoResultFound, MultipleResultsFound):
                print "Player {} not in lineup of {} vs {}".format(penalty_taker, home_team_name, away_team_name)
                continue

            penalty_dict = {'lineup_id': lineup_id, 'foul': foul_event, 'outcome': outcome,
                            'time': match_time, 'stoppage': stoppage_time}
            if not self.record_exists(Penalties, **penalty_dict):
                insertion_list.append(Penalties(**penalty_dict))
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    inserts += 50
                    print "{} penalties inserted".format(inserts)
                    insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
            self.session.commit()
        print "Penalty Ingestion complete."


class BookableIngest(EventsIngest):

    def parse_file(self, rows):
        inserts = 0
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

            foul_event = enums.FoulEventType.from_string(foul)
            card_type = enums.CardType.from_string(card)

            try:
                home_team_id = self.get_id(Clubs, name=home_team_name)
                away_team_id = self.get_id(Clubs, name=away_team_name)
            except (NoResultFound, MultipleResultsFound):
                continue

            try:
                match_id = self.get_id(ClubLeagueMatches, competition_id=self.competition_id, season_id=self.season_id,
                                       matchday=matchday, home_team_id=home_team_id, away_team_id=away_team_id)
            except (NoResultFound, MultipleResultsFound):
                print "Error: No match for {} vs {} in matchday {} of {} {}".format(
                    home_team_name, away_team_name, matchday, self.season, self.competition)
                continue

            try:
                if ':' in player_name:
                    player_name, birth_date = player_name.split(':')
                    player_id = self.get_id(Players, full_name=player_name, birth_date=birth_date)
                else:
                    player_id = self.get_id(Players, full_name=player_name)
                lineup_id = self.get_id(ClubMatchLineups, match_id=match_id, player_id=player_id)
            except (NoResultFound, MultipleResultsFound):
                print "Player {} not in lineup of {} vs {}".format(player_name, home_team_name, away_team_name)
                continue

            booking_dict = {'lineup_id': lineup_id, 'foul': foul_event, 'card': card_type,
                            'time': match_time, 'stoppage': stoppage_time}
            if not self.record_exists(Bookables, **booking_dict):
                insertion_list.append(Bookables(**booking_dict))
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    inserts += 50
                    print "{} bookable events inserted".format(inserts)
                    insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
            self.session.commit()
        print "Bookable Event Ingestion complete."


class SubstitutionIngest(EventsIngest):

    def parse_file(self, rows):
        inserts = 0
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

            try:
                home_team_id = self.get_id(Clubs, name=home_team_name)
                away_team_id = self.get_id(Clubs, name=away_team_name)
            except (NoResultFound, MultipleResultsFound):
                continue

            try:
                match_id = self.get_id(ClubLeagueMatches, competition_id=self.competition_id, season_id=self.season_id,
                                       matchday=matchday, home_team_id=home_team_id, away_team_id=away_team_id)
            except (NoResultFound, MultipleResultsFound):
                print "Error: No match for {} vs {} in matchday {} of {} {}".format(
                    home_team_name, away_team_name, matchday, self.season, self.competition)
                continue

            try:
                if ':' in out_player_name:
                    player_name, birth_date = out_player_name.split(':')
                    out_player_id = self.get_id(Players, full_name=player_name, birth_date=birth_date)
                else:
                    out_player_id = self.get_id(Players, full_name=out_player_name)
                out_lineup_id = self.get_id(ClubMatchLineups, match_id=match_id, player_id=out_player_id)
            except (NoResultFound, MultipleResultsFound):
                print "Player {} not in lineup of {} vs {}".format(out_player_name, home_team_name, away_team_name)
                continue

            try:
                if ':' in in_player_name:
                    player_name, birth_date = in_player_name.split(':')
                    in_player_id = self.get_id(Players, full_name=player_name, birth_date=birth_date)
                else:
                    in_player_id = self.get_id(Players, full_name=in_player_name)
                in_lineup_id = self.get_id(ClubMatchLineups, match_id=match_id, player_id=in_player_id)
            except (TypeError, NoResultFound):
                print "No player entering - player {} is being withdrawn from {} vs {}".format(
                    out_player_name, home_team_name, away_team_name)
            except MultipleResultsFound:
                print "Multiple player or lineup records for {}".format(in_player_name)
                continue

            sub_fields = ['lineup_in_id', 'lineup_out_id', 'time', 'stoppage']
            sub_values = [in_lineup_id, out_lineup_id, match_time, stoppage_time]
            substitution_dict = {field: value for field, value in zip(sub_fields, sub_values) if value is not None}
            if not self.record_exists(Substitutions, **substitution_dict):
                insertion_list.append(Substitutions(**substitution_dict))
                if len(insertion_list) == 50:
                    self.session.add_all(insertion_list)
                    self.session.commit()
                    inserts += 50
                    print "{} substitutions inserted".format(inserts)
                    insertion_list = []
        if len(insertion_list) != 0:
            self.session.add_all(insertion_list)
            self.session.commit()
        print "Substitution Ingestion complete."
