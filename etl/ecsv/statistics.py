from models.common import statistics as stats
from models.club import ClubLeagueMatches, ClubMap
from models.common.suppliers import Suppliers, PlayerMap
from models.common.match import MatchLineups
from models.common.overview import Competitions, Seasons

from ..base import BaseCSV


class MatchStatIngest(BaseCSV):

    def __init__(self, session, competition, season, supplier):
        super(MatchStatIngest, self).__init__(session)
        self.competition_id = self.get_id(Competitions, name=competition)
        self.season_id = self.get_id(Seasons, name=season)
        self.supplier_id = self.get_id(Suppliers, name=supplier)
        if any(var is None for var in [self.competition_id, self.season_id]):
            raise Exception("Fatal Error: Competition and/or Season not in Marcotti database!")

    @staticmethod
    def is_empty_record(*args):
        """Check for sparseness of statistical record.

        If all quantities of a statistical record are zero, return True.

        If at least one quantity of statistical record is nonzero, return False.
        """
        return not any([arg for arg in args])

    def identify_player(self, **keys):
        """Identify lineup player corresponding to row of stat data."""
        player_id_remote = self.column_int("Player ID", **keys)
        match_date = self.column("Date", **keys)
        locale = self.column("Venue", **keys)
        player_team_id_remote = self.column_int("Team Id", **keys)
        opposing_team_id_remote = self.column_int("Opposition Id", **keys)

        player_id = self.get_id(PlayerMap, remote_id=player_id_remote, supplier_id=self.supplier_id)
        player_team_id = self.get_id(ClubMap, remote_id=player_team_id_remote, supplier_id=self.supplier_id)
        opposing_team_id = self.get_id(ClubMap, remote_id=opposing_team_id_remote, supplier_id=self.supplier_id)

        home_team_id, away_team_id = (player_team_id, opposing_team_id) \
            if locale == "Home" else (opposing_team_id, player_team_id)

        match_id = self.get_id(ClubLeagueMatches, home_team_id=home_team_id,
                               away_team_id=away_team_id, date=match_date)
        lineup_id = self.get_id(MatchLineups, match_id=match_id, player_id=player_id)

        return lineup_id

    def parse_file(self, rows):
        raise NotImplementedError


class AssistsIngest(MatchStatIngest):

    model = stats.Assists

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)

            totals = self.column_int("Assists", **keys)
            corners = self.column_int("Goal Assist Corner", **keys)
            freekicks = self.column_int("Goal Assist Free Kick", **keys)
            throwins = self.column_int("Goal Assist Throw In", **keys)
            goalkicks = self.column_int("Goal Assist Goal Kick", **keys)
            setpieces = self.column_int("Goal Assist Set Piece", **keys)

            if not self.is_empty_record(totals, corners, freekicks, throwins, goalkicks, setpieces):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(lineup_id=lineup_id, corners=corners, freekicks=freekicks,
                                             throwins=throwins, goalkicks=goalkicks, setpieces=setpieces,
                                             total=totals)
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class ClearancesIngest(MatchStatIngest):

    model = stats.Clearances

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)

            total = self.column_int("Total Clearances", **keys)
            headed = self.column_int("Headed Clearances", **keys)
            other = self.column_int("Other Clearances", **keys)
            goalline = self.column_int("Clearances Off the Line", **keys)

            if not self.is_empty_record(total, headed, other, goalline):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(lineup_id=lineup_id, headed=headed, goalline=goalline,
                                             other=other, total=total)
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class CornersIngest(MatchStatIngest):

    model = stats.Corners

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)

            totals = self.column_int("Corners Taken incl short corners", **keys)
            short = self.column_int("Short Corners", **keys)
            box_success = self.column_int("Successful Corners into Box", **keys)
            box_failure = self.column_int("Unsuccessful Corners into Box", **keys)
            left_success = self.column_int("Successful Corners Left", **keys)
            left_failure = self.column_int("Unsuccessful Corners Left", **keys)
            right_success = self.column_int("Successful Corners Right", **keys)
            right_failure = self.column_int("Unsuccessful Corners Right", **keys)

            if not self.is_empty_record(totals, short, box_success, box_failure,
                                        left_success, left_failure, right_success, right_failure):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(lineup_id=lineup_id, penbox_success=box_success,
                                             penbox_failure=box_failure, left_success=left_success,
                                             left_failure=left_failure, right_success=right_success,
                                             right_failure=right_failure, short=short, total=totals)
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class CornerCrossesIngest(MatchStatIngest):

    model = stats.CornerCrosses

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)

            total_success = self.column_int("Successful Crosses Corners", **keys)
            total_failure = self.column_int("Unsuccessful Crosses Corners", **keys)
            air_success = self.column_int("Successful Crosses Corners in the air", **keys)
            air_failure = self.column_int("Unsuccessful Crosses Corners in the air", **keys)
            left_success = self.column_int("Successful Crosses Corners Left", **keys)
            left_failure = self.column_int("Unsuccessful Crosses Corners Left", **keys)
            right_success = self.column_int("Successful Crosses Corners Right", **keys)
            right_failure = self.column_int("Unsuccessful Crosses Corners Right", **keys)

            if not self.is_empty_record(total_success, total_failure, air_success,
                                        air_failure, left_success, left_failure, right_success, right_failure):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(lineup_id=lineup_id, total_success=total_success,
                                             total_failure=total_failure, air_success=air_success,
                                             air_failure=air_failure, left_success=left_success,
                                             left_failure=left_failure, right_success=right_success,
                                             right_failure=right_failure)
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class CrossesIngest(MatchStatIngest):

    model = stats.Crosses

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)

            air_success = self.column_int("Successful crosses in the air", **keys)
            air_failure = self.column_int("Unsuccessful crosses in the air", **keys)
            openplay_success = self.column_int("Successful open play crosses", **keys)
            openplay_failure = self.column_int("Unsuccessful open play crosses", **keys)
            left_success = self.column_int("Successful Crosses Left", **keys)
            left_failure = self.column_int("Unsuccessful Crosses Left", **keys)
            right_success = self.column_int("Successful Crosses Right", **keys)
            right_failure = self.column_int("Unsuccessful Crosses Right", **keys)

            if not self.is_empty_record(air_success, air_failure, openplay_success,
                                        openplay_failure, left_success, left_failure, right_success,
                                        right_failure):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "air_success": air_success,
                        "air_failure": air_failure,
                        "openplay_success": openplay_success,
                        "openplay_failure": openplay_failure,
                        "left_success": left_success,
                        "left_failure": left_failure,
                        "right_success": right_success,
                        "right_failure": right_failure})
                    self.session.add(stat_record)
                dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class DefensivesIngest(MatchStatIngest):

    model = stats.Defensives

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)

            blocks = self.column_int("Blocks", **keys)
            intercepts = self.column_int("Interceptions", **keys)
            recovers = self.column_int("Recoveries", **keys)
            corners = self.column_int("Corners Conceded", **keys)
            fouls = self.column_int("Total Fouls Conceded", **keys)
            challenges_lost = self.column_int("Challenge Lost", **keys)
            handballs = self.column_int("Handballs Conceded", **keys)
            penalties = self.column_int("Penalties Conceded", **keys)
            errs_goals = self.column_int("Error leading to Goal", **keys)
            errs_shots = self.column_int("Error leading to Attempt", **keys)

            if not self.is_empty_record(blocks, intercepts, recovers, corners, fouls,
                                        challenges_lost, handballs, penalties, errs_goals, errs_shots):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "blocks": blocks,
                        "interceptions": intercepts,
                        "recoveries": recovers,
                        "corners_conceded": corners,
                        "fouls_conceded": fouls,
                        "challenges_lost": challenges_lost,
                        "handballs_conceded": handballs,
                        "penalties_conceded": penalties,
                        "error_goals": errs_goals,
                        "error_shots": errs_shots})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class DisciplineIngest(MatchStatIngest):

    model = stats.Discipline

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)

            yellows = self.column_int("Yellow Cards", **keys)
            reds = self.column_int("Red Cards", **keys)

            if not self.is_empty_record(yellows, reds):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "yellows": yellows,
                        "reds": reds})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class DuelsIngest(MatchStatIngest):

    model = stats.Duels

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            total_won = self.column_int("Duels won", **keys)
            total_lost = self.column_int("Duels lost", **keys)
            aerial_won = self.column_int("Aerial Duels won", **keys)
            aerial_lost = self.column_int("Aerial Duels lost", **keys)
            ground_won = self.column_int("Ground Duels won", **keys)
            ground_lost = self.column_int("Ground Duels lost", **keys)

            if not self.is_empty_record(total_won, total_lost, aerial_won, aerial_lost, ground_won, ground_lost):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "total_won": total_won,
                        "total_lost": total_lost,
                        "aerial_won": aerial_won,
                        "aerial_lost": aerial_lost,
                        "ground_won": ground_won,
                        "ground_lost": ground_lost})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class FoulWinsIngest(MatchStatIngest):

    model = stats.FoulWins

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            total = self.column_int("Total Fouls Won", **keys)
            total_danger = self.column_int("Fouls Won in Danger Area inc pens", **keys)
            total_penalty = self.column_int("Foul Won Penalty", **keys)
            total_nodanger = self.column_int("Fouls Won not in danger area", **keys)

            if not self.is_empty_record(total, total_danger, total_penalty, total_nodanger):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "total": total, 
                        "total_danger": total_danger,
                        "total_penalty": total_penalty,
                        "total_nodanger": total_nodanger})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class FreeKicksIngest(MatchStatIngest):

    model = stats.Freekicks

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            ontarget = self.column_int("Direct Free-kick On Target", **keys)
            offtarget = self.column_int("Direct Free-kick Off Target", **keys)

            if not self.is_empty_record(ontarget, offtarget):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "ontarget": ontarget, 
                        "offtarget": offtarget})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class GKAllowedGoalsIngest(MatchStatIngest):

    model = stats.GoalkeeperAllowedGoals

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            insidebox = self.column_int("Goals Conceded Inside Box", **keys)
            outsidebox = self.column_int("Goals Conceded Outside Box", **keys)
            is_cleansheet = self.column_bool("Clean Sheets", **keys)

            if not self.is_empty_record(insidebox, outsidebox) or is_cleansheet:

                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "insidebox": insidebox, 
                        "outsidebox": outsidebox,
                        "is_cleansheet": is_cleansheet})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class GKSavesIngest(MatchStatIngest):

    model = stats.GoalkeeperSaves

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            insidebox = self.column_int("Saves Made from Inside Box", **keys)
            outsidebox = self.column_int("Saves Made from Outside Box", **keys)
            penalty = self.column_int("Saves from Penalty", **keys)

            if not self.is_empty_record(insidebox, outsidebox, penalty):

                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "insidebox": insidebox,
                        "outsidebox": outsidebox,
                        "penalty": penalty})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class GKAllowedShotsIngest(MatchStatIngest):

    model = stats.GoalkeeperAllowedShots

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            insidebox = self.column_int("Shots On Conceded Inside Box", **keys)
            outsidebox = self.column_int("Shots On Conceded Outside Box", **keys)
            bigchances = self.column_int("Big Chances Faced", **keys)

            if not self.is_empty_record(insidebox, outsidebox, bigchances):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "insidebox": insidebox,
                        "outsidebox": outsidebox,
                        "dangerous": bigchances})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class GKActionsIngest(MatchStatIngest):

    model = stats.GoalkeeperActions

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            catches = self.column_int("Catches", **keys)
            punches = self.column_int("Punches", **keys)
            drops = self.column_int("Drops", **keys)
            crosses_noclaim = self.column_int("Crosses not Claimed", **keys)
            distrib_success = self.column_int("GK Successful Distribution", **keys)
            distrib_failure = self.column_int("GK Unsuccessful Distribution", **keys)

            if not self.is_empty_record(catches, punches, drops, crosses_noclaim,
                                        distrib_success, distrib_failure):

                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "catches": catches,
                        "punches": punches,
                        "drops": drops,
                        "crosses_unclaimed": crosses_noclaim,
                        "distribution_success": distrib_success,
                        "distribution_failure": distrib_failure})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class GoalBodyPartsIngest(MatchStatIngest):

    model = stats.GoalBodyparts

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)

        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            headed = self.column_int("Headed Goals", **keys)
            left_foot = self.column_int("Left Foot Goals", **keys)
            right_foot = self.column_int("Right Foot Goals", **keys)

            if not self.is_empty_record(headed, left_foot, right_foot):

                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "headed": headed,
                        "leftfoot": left_foot,
                        "rightfoot": right_foot})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class GoalLocationsIngest(MatchStatIngest):

    model = stats.GoalLocations

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            insidebox = self.column_int("Goals from Inside Box", **keys)
            outsidebox = self.column_int("Goals from Outside Box", **keys)

            if not self.is_empty_record(insidebox, outsidebox):

                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "insidebox": insidebox,
                        "outsidebox": outsidebox})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class GoalTotalsIngest(MatchStatIngest):

    model = stats.GoalTotals

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)

        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            is_firstgoal = self.column_bool("First Goal", **keys)
            is_winner = self.column_bool("Winning Goal", **keys)
            freekick = self.column_int("Goals from Direct Free Kick", **keys)
            openplay = self.column_int("Goals Open Play", **keys)
            corners = self.column_int("Goals from Corners", **keys)
            throwins = self.column_int("Goals from Throws", **keys)
            penalties = self.column_int("Goals from penalties", **keys)
            substitute = self.column_int("Goals as a substitute", **keys)
            other = self.column_int("Other Goals", **keys)

            if not self.is_empty_record(freekick, openplay, corners, throwins,
                                        penalties, substitute, other) or is_firstgoal or is_winner:

                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "is_firstgoal": is_firstgoal,
                        "is_winner": is_winner,
                        "freekick": freekick,
                        "openplay": openplay,
                        "corners": corners,
                        "throwins": throwins,
                        "penalties": penalties,
                        "substitute": substitute,
                        "other": other})
                    self.session.add(stat_record)
                    dcounter += 1

            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class GoalLineClearancesIngest(MatchStatIngest):

    model = stats.GoalLineClearances

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            insidebox = self.column_int("Shots Cleared off Line Inside Area", **keys)
            outsidebox = self.column_int("Shots Cleared off Line Outside Area", **keys)
            totalshots = self.column_int("Shots Cleared off Line", **keys)

            if not self.is_empty_record(insidebox, outsidebox, totalshots):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "insidebox": insidebox,
                        "outsidebox": outsidebox,
                        "totalshots": totalshots})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class ImportantPlaysIngest(MatchStatIngest):

    model = stats.ImportantPlays

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            corners = self.column_int("Key Corner", **keys)
            freekicks = self.column_int("Key Free Kick", **keys)
            throwins = self.column_int("Key Throw In", **keys)
            goalkicks = self.column_int("Key Goal Kick", **keys)

            if not self.is_empty_record(corners, freekicks, throwins, goalkicks):

                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "corners": corners,
                        "freekicks": freekicks,
                        "throwins": throwins,
                        "goalkicks": goalkicks})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class PassDirectionsIngest(MatchStatIngest):

    model = stats.PassDirections

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            pass_forward = self.column_int("Pass Forward", **keys)
            pass_backward = self.column_int("Pass Backward", **keys)
            pass_left = self.column_int("Pass Left", **keys)
            pass_right = self.column_int("Pass Right", **keys)

            if not self.is_empty_record(pass_forward, pass_backward, pass_left, pass_right):

                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "forward": pass_forward,
                        "backward": pass_backward,
                        "left_side": pass_left,
                        "right_side": pass_right})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class PassLengthsIngest(MatchStatIngest):

    model = stats.PassLengths

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            short_success = self.column_int("Successful Short Passes", **keys)
            short_failure = self.column_int("Unsuccessful Short Passes", **keys)
            long_success = self.column_int("Successful Long Passes", **keys)
            long_failure = self.column_int("Unsuccessful Long Passes", **keys)
            flickon_success = self.column_int("Successful Flick-Ons", **keys)
            flickon_failure = self.column_int("Unsuccessful Flick-Ons", **keys)

            if not self.is_empty_record(short_success, short_failure, long_success,
                                        long_failure, flickon_success, flickon_failure):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "short_success": short_success,
                        "short_failure": short_failure,
                        "long_success": long_success,
                        "long_failure": long_failure,
                        "flickon_success": flickon_success,
                        "flickon_failure": flickon_failure})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class PassLocationsIngest(MatchStatIngest):

    model = stats.PassLocations

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            ownhalf_success = self.column_int("Successful Passes Own Half", **keys)
            ownhalf_failure = self.column_int("Unsuccessful Passes Own Half", **keys)
            opphalf_success = self.column_int("Successful Passes Opposition Half", **keys)
            opphalf_failure = self.column_int("Unsuccessful Passes Opposition Half", **keys)
            defthird_success = self.column_int("Successful Passes Defensive third", **keys)
            defthird_failure = self.column_int("Unsuccessful Passes Defensive third", **keys)
            midthird_success = self.column_int("Successful Passes Middle third", **keys)
            midthird_failure = self.column_int("Unsuccessful Passes Middle third", **keys)
            finthird_success = self.column_int("Successful Passes Final third", **keys)
            finthird_failure = self.column_int("Unsuccessful Passes Final third", **keys)

            if not self.is_empty_record(ownhalf_success, ownhalf_failure,
                                        opphalf_success, opphalf_failure, defthird_success,
                                        defthird_failure, midthird_success, midthird_failure,
                                        finthird_success, finthird_failure):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "ownhalf_success": ownhalf_success,
                        "ownhalf_failure": ownhalf_failure,
                        "opphalf_success": opphalf_success,
                        "opphalf_failure": opphalf_failure,
                        "defthird_success": defthird_success,
                        "defthird_failure": defthird_failure,
                        "midthird_success": midthird_success,
                        "midthird_failure": midthird_failure,
                        "finthird_success": finthird_success,
                        "finthird_failure": finthird_failure})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class PassTotalsIngest(MatchStatIngest):

    model = stats.Passes

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            total_success = self.column_int("Total Successful Passes All", **keys)
            total_failure = self.column_int("Total Unsuccessful Passes All", **keys)
            total_no_cc_success = self.column_int("Total Successful Passes Excl Crosses Corners", **keys)
            total_no_cc_failure = self.column_int("Total Unsuccessful Passes Excl Crosses Corners", **keys)
            longball_success = self.column_int("Successful Long Balls", **keys)
            longball_failure = self.column_int("Unsuccessful Long Balls", **keys)
            layoffs_success = self.column_int("Successful Lay-Offs", **keys)
            layoffs_failure = self.column_int("Unsuccessful Lay-Offs", **keys)
            throughballs = self.column_int("Through Ball", **keys)
            keypasses = self.column_int("Key Passes", **keys)

            if not self.is_empty_record(total_success, total_failure,
                                        total_no_cc_success, total_no_cc_failure, longball_success,
                                        longball_failure, layoffs_success, layoffs_failure,
                                        throughballs, keypasses):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "total_success": total_success,
                        "total_failure": total_failure,
                        "total_no_cc_success": total_no_cc_success,
                        "total_no_cc_failure": total_no_cc_failure,
                        "longball_success": longball_success,
                        "longball_failure": longball_failure,
                        "layoffs_success": layoffs_success,
                        "layoffs_failure": layoffs_failure,
                        "throughballs": throughballs,
                        "important_passes": keypasses})
                    self.session.add(stat_record)
                    dcounter += 1

            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class PenaltyActionsIngest(MatchStatIngest):

    model = stats.PenaltyActions

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            taken = self.column_int("Penalties Taken", **keys)
            saved = self.column_int("Penalties Saved", **keys)
            offtarget = self.column_int("Penalties Off Target", **keys)
            ontarget = self.column_int("Attempts from Penalties on target", **keys)

            if not self.is_empty_record(taken, saved, offtarget, ontarget):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "taken": taken,
                        "saved": saved,
                        "offtarget": offtarget,
                        "ontarget": ontarget})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class ShotBodyPartsIngest(MatchStatIngest):

    model = stats.ShotBodyparts

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            head_ontarget = self.column_int("Headed Shots On Target", **keys)
            head_offtarget = self.column_int("Headed Shots Off Target", **keys)
            left_ontarget = self.column_int("Left Foot Shots On Target", **keys)
            left_offtarget = self.column_int("Left Foot Shots Off Target", **keys)
            right_ontarget = self.column_int("Right Foot Shots On Target", **keys)
            right_offtarget = self.column_int("Right Foot Shots Off Target", **keys)

            if not self.is_empty_record(head_ontarget, head_offtarget, left_ontarget,
                                        left_offtarget, right_ontarget, right_offtarget):

                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "head_ontarget": head_ontarget,
                        "head_offtarget": head_offtarget,
                        "left_ontarget": left_ontarget,
                        "left_offtarget": left_offtarget,
                        "right_ontarget": right_ontarget,
                        "right_offtarget": right_offtarget})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class ShotBlocksIngest(MatchStatIngest):

    model = stats.ShotBlocks

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            freekick = self.column_int("Blocked Direct Free-kick", **keys)
            insidebox = self.column_int("Blocked Shots from Inside Box", **keys)
            outsidebox = self.column_int("Blocked Shots Outside Box", **keys)
            headed = self.column_int("Headed Blocked Shots", **keys)
            leftfoot = self.column_int("Left Foot Blocked Shots", **keys)
            rightfoot = self.column_int("Right Foot Blocked Shots", **keys)
            other = self.column_int("Other Blocked Shots", **keys)
            total = self.column_int("Blocked Shots", **keys)

            if not self.is_empty_record(freekick, insidebox, outsidebox, headed,
                                        leftfoot, rightfoot, other, total):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "freekick": freekick,
                        "insidebox": insidebox,
                        "outsidebox": outsidebox,
                        "headed": headed,
                        "leftfoot": leftfoot,
                        "rightfoot": rightfoot,
                        "other": other,
                        "total": total})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class ShotLocationsIngest(MatchStatIngest):

    model = stats.ShotLocations

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            insidebox_ontarget = self.column_int("Shots On from Inside Box", **keys)
            insidebox_offtarget = self.column_int("Shots Off from Inside Box", **keys)
            outsidebox_ontarget = self.column_int("Shots On Target Outside Box", **keys)
            outsidebox_offtarget = self.column_int("Shots Off Target Outside Box", **keys)

            if not self.is_empty_record(insidebox_ontarget, insidebox_offtarget,
                                        outsidebox_ontarget, outsidebox_offtarget):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "insidebox_ontarget": insidebox_ontarget,
                        "insidebox_offtarget": insidebox_offtarget,
                        "outsidebox_ontarget": outsidebox_ontarget,
                        "outsidebox_offtarget": outsidebox_offtarget})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class ShotPlaysIngest(MatchStatIngest):

    model = stats.ShotPlays

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            openplay_ontarget = self.column_int("Attempts Open Play on target", **keys)
            openplay_offtarget = self.column_int("Attempts Open Play off target", **keys)
            setplay_ontarget = self.column_int("Attempts from Set Play on target", **keys)
            setplay_offtarget = self.column_int("Attempts from Set Play off target", **keys)
            freekick_ontarget = self.column_int("Attempts from Direct Free Kick on target", **keys)
            freekick_offtarget = self.column_int("Attempts from Direct Free Kick off target", **keys)
            corners_ontarget = self.column_int("Attempts from Corners on target", **keys)
            corners_offtarget = self.column_int("Attempts from Corners off target", **keys)
            throwins_ontarget = self.column_int("Attempts from Throws on target", **keys)
            throwins_offtarget = self.column_int("Attempts from Throws off target", **keys)
            other_ontarget = self.column_int("Other Shots On Target", **keys)
            other_offtarget = self.column_int("Other Shots Off Target", **keys)

            if not self.is_empty_record(openplay_ontarget, openplay_offtarget,
                                        setplay_ontarget, setplay_offtarget, freekick_ontarget,
                                        freekick_offtarget, corners_ontarget, corners_offtarget,
                                        throwins_ontarget, throwins_offtarget, other_ontarget,
                                        other_offtarget):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "openplay_ontarget": openplay_ontarget,
                        "openplay_offtarget": openplay_offtarget,
                        "setplay_ontarget": setplay_ontarget,
                        "setplay_offtarget": setplay_offtarget,
                        "freekick_ontarget": freekick_ontarget,
                        "freekick_offtarget": freekick_offtarget,
                        "corners_ontarget": corners_ontarget,
                        "corners_offtarget": corners_offtarget,
                        "throwins_ontarget": throwins_ontarget,
                        "throwins_offtarget": throwins_offtarget,
                        "other_ontarget": other_ontarget,
                        "other_offtarget": other_offtarget})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class ShotTotalsIngest(MatchStatIngest):

    model = stats.ShotTotals

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            ontarget = self.column_int("Shots On Target inc goals", **keys)
            offtarget = self.column_int("Shots Off Target inc woodwork", **keys)
            bigchances = self.column_int("Big Chances", **keys)

            if not self.is_empty_record(ontarget, offtarget, bigchances):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "ontarget": ontarget,
                        "offtarget": offtarget,
                        "dangerous": bigchances})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class TacklesIngest(MatchStatIngest):

    model = stats.Tackles

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            won = self.column_int("Tackles Won", **keys)
            lost = self.column_int("Tackles Lost", **keys)
            lastman = self.column_int("Last Man Tackle", **keys)

            if not self.is_empty_record(won, lost, lastman):

                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "won": won,
                        "lost": lost,
                        "lastman": lastman})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class ThrowinsIngest(MatchStatIngest):

    model = stats.Throwins

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            teamplayer = self.column_int("Throw Ins to Own Player", **keys)
            oppplayer = self.column_int("Throw Ins to Opposition Player", **keys)

            if not self.is_empty_record(teamplayer, oppplayer):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "to_teamplayer": teamplayer,
                        "to_oppplayer": oppplayer})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class TouchesIngest(MatchStatIngest):

    model = stats.Touches

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            dribble_overruns = self.column_int("Take-Ons Overrun", **keys)
            dribble_success = self.column_int("Successful Dribbles", **keys)
            dribble_failure = self.column_int("Unsuccessful Dribbles", **keys)
            balltouch_success = self.column_int("Successful Ball Touch", **keys)
            balltouch_failure = self.column_int("Unsuccessful Ball Touch", **keys)
            possession_loss = self.column_int("Dispossessed", **keys)
            total = self.column_int("Touches", **keys)

            if not self.is_empty_record(dribble_overruns, dribble_success,
                                        dribble_failure, balltouch_success, balltouch_failure,
                                        possession_loss, total):

                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "dribble_overruns": dribble_overruns,
                        "dribble_success": dribble_success,
                        "dribble_failure": dribble_failure,
                        "balltouch_success": balltouch_success,
                        "balltouch_failure": balltouch_failure,
                        "possession_loss": possession_loss,
                        "total": total})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()


class TouchLocationsIngest(MatchStatIngest):

    model = stats.TouchLocations

    def parse_file(self, rows):
        print "Processing {}".format(self.__class__.__name__)
        counter = 0
        dcounter = 0
        for keys in rows:
            lineup_id = self.identify_player(**keys)
            finalthird = self.column_int("Touches open play final third", **keys)
            oppbox = self.column_int("Touches open play opp box", **keys)
            oppsix = self.column_int("Touches open play opp six yards", **keys)

            if not self.is_empty_record(finalthird, oppbox, oppsix):
                if not self.record_exists(self.model, lineup_id=lineup_id):
                    stat_record = self.model(**{
                        "lineup_id": lineup_id,
                        "final_third": finalthird,
                        "oppbox": oppbox,
                        "oppsix": oppsix})
                    self.session.add(stat_record)
                    dcounter += 1
            counter += 1
            if not counter % 500:
                print "{} records".format(counter)
        print "{} {} records from {} lineup records".format(dcounter, self.model.__name__, counter)
        self.session.commit()
