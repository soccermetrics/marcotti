import pandas as pd

import marcotti.models.club as mc
import marcotti.models.common.enums as enums
import marcotti.models.common.overview as mco
import marcotti.models.common.personnel as mcp
import marcotti.models.common.suppliers as mcs
from .workflows import WorkflowBase


class MarcottiTransform(WorkflowBase):
    """
    Transform and validate extracted data.
    """

    @staticmethod
    def suppliers(data_frame):
        return data_frame

    @staticmethod
    def years(data_frame):
        return data_frame

    @staticmethod
    def seasons(data_frame):
        return data_frame

    def competitions(self, data_frame):
        if 'country' in data_frame.columns:
            transformed_field = 'country'
            lambdafunc = lambda x: pd.Series(self.get_id(mco.Countries, name=x[transformed_field]))
            id_frame = data_frame.apply(lambdafunc, axis=1)
            id_frame.columns = ['country_id']
        elif 'confed' in data_frame.columns:
            transformed_field = 'confed'
            lambdafunc = lambda x: pd.Series(enums.ConfederationType.from_string(x[transformed_field]))
            id_frame = data_frame.apply(lambdafunc, axis=1)
            id_frame.columns = ['confederation']
        else:
            raise KeyError("Cannot insert Competition record: No Country or Confederation data present")
        return data_frame.join(id_frame).drop(transformed_field, axis=1)

    def countries(self, data_frame):
        lambdafunc = lambda x: pd.Series(enums.ConfederationType.from_string(x['confed']))
        id_frame = data_frame.apply(lambdafunc, axis=1)
        id_frame.columns = ['confederation']
        joined_frame = data_frame.join(id_frame).drop('confed', axis=1)
        return joined_frame

    def clubs(self, data_frame):
        if 'country' in data_frame.columns:
            lambdafunc = lambda x: pd.Series(self.get_id(mco.Countries, name=x['country']))
            id_frame = data_frame.apply(lambdafunc, axis=1)
            id_frame.columns = ['country_id']
        else:
            raise KeyError("Cannot insert Club record: No Country data present")
        return data_frame.join(id_frame)

    def venues(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.get_id(mco.Countries, name=x['country']),
            self.get_id(mco.Timezones, name=x['timezone']),
            self.get_id(mco.Surfaces, description=x['surface']),
            self.make_date_object(x['config_date'])
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['country_id', 'timezone_id', 'surface_id', 'eff_date']
        joined_frame = data_frame.join(ids_frame).drop(['country', 'timezone', 'surface', 'config_date'], axis=1)
        new_frame = joined_frame.where((pd.notnull(joined_frame)), None)
        return new_frame

    def timezones(self, data_frame):
        lambdafunc = lambda x: pd.Series(enums.ConfederationType.from_string(x['confed']))
        id_frame = data_frame.apply(lambdafunc, axis=1)
        id_frame.columns = ['confederation']
        joined_frame = data_frame.join(id_frame).drop('confed', axis=1)
        return joined_frame

    def positions(self, data_frame):
        lambdafunc = lambda x: pd.Series(enums.PositionType.from_string(x['position_type']))
        id_frame = data_frame.apply(lambdafunc, axis=1)
        id_frame.columns = ['type']
        joined_frame = data_frame.join(id_frame).drop('position_type', axis=1)
        return joined_frame

    def surfaces(self, data_frame):
        lambdafunc = lambda x: pd.Series(enums.SurfaceType.from_string(x['surface_type']))
        id_frame = data_frame.apply(lambdafunc, axis=1)
        id_frame.columns = ['type']
        joined_frame = data_frame.join(id_frame).drop('surface_type', axis=1)
        return joined_frame

    def players(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.make_date_object(x['dob']),
            enums.NameOrderType.from_string(x['name_order'] or 'Western'),
            self.get_id(mco.Countries, name=x['country']),
            self.get_id(mcs.PositionMap, remote_id=x['remote_position_id'], supplier_id=self.supplier_id)
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['birth_date', 'order', 'country_id', 'position_id']
        joined_frame = data_frame.join(ids_frame).drop(
            ['dob', 'name_order', 'country', 'remote_position_id'], axis=1)
        return joined_frame

    def managers(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.make_date_object(x['dob']),
            enums.NameOrderType.from_string(x['name_order'] or 'Western'),
            self.get_id(mco.Countries, name=x['country'])
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['birth_date', 'order', 'country_id']
        joined_frame = data_frame.join(ids_frame).drop(['dob', 'name_order', 'country'], axis=1)
        return joined_frame

    def referees(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.make_date_object(x['dob']),
            enums.NameOrderType.from_string(x['name_order'] or 'Western'),
            self.get_id(mco.Countries, name=x['country'])
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['birth_date', 'order', 'country_id']
        joined_frame = data_frame.join(ids_frame).drop(['dob', 'name_order', 'country'], axis=1)
        return joined_frame

    def league_matches(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.get_id(mco.Competitions, name=x['competition']),
            self.get_id(mco.Seasons, name=x['season']),
            self.get_id(mco.Venues, name=x['venue']),
            self.get_id(mc.Clubs, name=x['home_team']),
            self.get_id(mc.Clubs, name=x['away_team']),
            self.get_id(mcp.Managers, full_name=x['home_manager']),
            self.get_id(mcp.Managers, full_name=x['away_manager']),
            self.get_id(mcp.Referees, full_name=x['referee']),
            self.make_date_object(x['date']),
            enums.WeatherConditionType.from_string(x['kickoff_wx']) if x['kickoff_wx'] else None,
            enums.WeatherConditionType.from_string(x['halftime_wx']) if x['halftime_wx'] else None,
            enums.WeatherConditionType.from_string(x['fulltime_wx']) if x['fulltime_wx'] else None
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['competition_id', 'season_id', 'venue_id', 'home_team_id', 'away_team_id',
                             'home_manager_id', 'away_manager_id', 'referee_id', 'match_date',
                             'kickoff_weather', 'halftime_weather', 'fulltime_weather']
        columns_to_drop = ['competition', 'season', 'venue', 'home_team', 'away_team', 'home_manager',
                           'away_manager', 'referee', 'date', 'kickoff_wx', 'halftime_wx', 'fulltime_wx']
        return data_frame.join(ids_frame).drop(columns_to_drop, axis=1)

    def knockout_matches(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.get_id(mco.Competitions, name=x['competition']),
            self.get_id(mco.Seasons, name=x['season']),
            self.get_id(mco.Venues, name=x['venue']),
            self.get_id(mc.Clubs, name=x['home_team']),
            self.get_id(mc.Clubs, name=x['away_team']),
            self.get_id(mcp.Managers, full_name=x['home_manager']),
            self.get_id(mcp.Managers, full_name=x['away_manager']),
            self.get_id(mcp.Referees, full_name=x['referee']),
            enums.KnockoutRoundType.from_string(x['round']),
            self.make_date_object(x['date']),
            enums.WeatherConditionType.from_string(x['kickoff_wx']) if x['kickoff_wx'] else None,
            enums.WeatherConditionType.from_string(x['halftime_wx']) if x['halftime_wx'] else None,
            enums.WeatherConditionType.from_string(x['fulltime_wx']) if x['fulltime_wx'] else None
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['competition_id', 'season_id', 'venue_id', 'home_team_id', 'away_team_id',
                             'home_manager_id', 'away_manager_id', 'referee_id', 'ko_round', 'match_date',
                             'kickoff_weather', 'halftime_weather', 'fulltime_weather']
        columns_to_drop = ['competition', 'season', 'venue', 'home_team', 'away_team', 'home_manager',
                           'away_manager', 'referee', 'date', 'round', 'kickoff_wx', 'halftime_wx', 'fulltime_wx']
        return data_frame.join(ids_frame).drop(columns_to_drop, axis=1)

    def group_matches(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.get_id(mco.Competitions, name=x['competition']),
            self.get_id(mco.Seasons, name=x['season']),
            self.get_id(mco.Venues, name=x['venue']),
            self.get_id(mc.Clubs, name=x['home_team']),
            self.get_id(mc.Clubs, name=x['away_team']),
            self.get_id(mcp.Managers, full_name=x['home_manager']),
            self.get_id(mcp.Managers, full_name=x['away_manager']),
            self.get_id(mcp.Referees, full_name=x['referee']),
            enums.GroupRoundType.from_string(x['round']),
            self.make_date_object(x['date']),
            enums.WeatherConditionType.from_string(x['kickoff_wx']) if x['kickoff_wx'] else None,
            enums.WeatherConditionType.from_string(x['halftime_wx']) if x['halftime_wx'] else None,
            enums.WeatherConditionType.from_string(x['fulltime_wx']) if x['fulltime_wx'] else None
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['competition_id', 'season_id', 'venue_id', 'home_team_id', 'away_team_id',
                             'home_manager_id', 'away_manager_id', 'referee_id', 'group_round', 'match_date',
                             'kickoff_weather', 'halftime_weather', 'fulltime_weather']
        columns_to_drop = ['competition', 'season', 'venue', 'home_team', 'away_team', 'home_manager',
                           'away_manager', 'referee', 'date', 'round', 'kickoff_wx', 'halftime_wx', 'fulltime_wx']
        return data_frame.join(ids_frame).drop(columns_to_drop, axis=1)

    def match_lineups(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.get_id(mc.ClubLeagueMatches,
                        competition_id=self.get_id(mco.Competitions, name=x['competition']),
                        season_id=self.get_id(mco.Seasons, name=x['season']),
                        matchday=x['matchday'],
                        home_team_id=self.get_id(mc.Clubs, name=x['home_team']),
                        away_team_id=self.get_id(mc.Clubs, name=x['away_team'])),
            self.get_id(mc.Clubs, name=x['player_team']),
            self.get_id(mcp.Players, full_name=x['player_name'])
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['match_id', 'team_id', 'player_id']
        columns_to_drop = ['competition', 'season', 'matchday', 'home_team', 'away_team']
        return data_frame.join(ids_frame).drop(columns_to_drop, axis=1)

    def goals(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.get_id(mc.ClubMatchLineups,
                        match_id=self.get_id(mcs.MatchMap, remote_id=x['remote_match_id'],
                                             supplier_id=self.supplier_id),
                        player_id=self.get_id(mcp.Players, full_name=x['scorer'])),
            self.get_id(mc.Clubs, name=x['scoring_team']),
            enums.ShotEventType.from_string(x['scoring_event']),
            enums.BodypartType.from_string(x['bodypart_desc'])
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['lineup_id', 'team_id', 'event', 'bodypart']
        columns_to_drop = ['remote_match_id', 'scorer', 'scoring_team', 'scoring_event', 'bodypart_desc']
        return data_frame.join(ids_frame).drop(columns_to_drop, axis=1)

    def penalties(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.get_id(mc.ClubMatchLineups,
                        match_id=self.get_id(mcs.MatchMap, remote_id=x['remote_match_id'],
                                             supplier_id=self.supplier_id),
                        player_id=self.get_id(mcp.Players, full_name=x['penalty_taker'])),
            enums.FoulEventType.from_string(x['penalty_foul']),
            enums.ShotOutcomeType.from_string(x['penalty_outcome'])
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['lineup_id', 'foul', 'outcome']
        columns_to_drop = ['remote_match_id', 'penalty_taker', 'penalty_foul', 'penalty_outcome']
        return data_frame.join(ids_frame).drop(columns_to_drop, axis=1)

    def bookables(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.get_id(mc.ClubMatchLineups,
                        match_id=self.get_id(mcs.MatchMap, remote_id=x['remote_match_id'],
                                             supplier_id=self.supplier_id),
                        player_id=self.get_id(mcp.Players, full_name=x['player'])),
            enums.FoulEventType.from_string(x['foul_desc']),
            enums.CardType.from_string(x['card_type'])
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['lineup_id', 'foul', 'card']
        columns_to_drop = ['remote_match_id', 'player', 'foul_desc', 'card_type']
        return data_frame.join(ids_frame).drop(columns_to_drop, axis=1)

    def substitutions(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.get_id(mc.ClubMatchLineups,
                        match_id=self.get_id(mcs.MatchMap, remote_id=x['remote_match_id'],
                                             supplier_id=self.supplier_id),
                        player_id=self.get_id(mcp.Players, full_name=x['in_player_name'])),
            self.get_id(mc.ClubMatchLineups,
                        match_id=self.get_id(mcs.MatchMap, remote_id=x['remote_match_id'],
                                             supplier_id=self.supplier_id),
                        player_id=self.get_id(mcp.Players, full_name=x['out_player_name']))
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['lineup_in_id', 'lineup_out_id']
        columns_to_drop = ['remote_match_id', 'in_player_name', 'out_player_name']
        return data_frame.join(ids_frame).drop(columns_to_drop, axis=1)

    def penalty_shootouts(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.get_id(mc.ClubMatchLineups,
                        match_id=self.get_id(mcs.MatchMap, remote_id=x['remote_match_id'], supplier_id=self.supplier_id),
                        player_id=self.get_id(mcp.Players, full_name=x['penalty_taker'])),
            enums.ShotOutcomeType.from_string(x['penalty_outcome'])
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['lineup_id', 'outcome']
        columns_to_drop = ['remote_match_id', 'penalty_taker', 'penalty_outcome']
        return data_frame.join(ids_frame).drop(columns_to_drop, axis=1)


class MarcottiStatsTransform(MarcottiTransform):

    categories = ['assists', 'clearances', 'corner_crosses', 'corners', 'crosses', 'defensives',
                  'discipline', 'duels', 'foul_wins', 'freekicks', 'gk_actions', 'gk_allowed_goals',
                  'gk_allowed_shots', 'gk_saves', 'goal_bodyparts', 'goal_locations', 'goal_totals',
                  'goalline_clearances', 'important_plays', 'pass_directions', 'pass_lengths',
                  'pass_locations', 'pass_totals', 'penalty_actions', 'shot_blocks', 'shot_bodyparts',
                  'shot_locations', 'shot_plays', 'shot_totals', 'tackles', 'throwins', 'touch_locations',
                  'touches']

    def __init__(self, session, supplier):
        super(MarcottiStatsTransform, self).__init__(session, supplier)
        for category in MarcottiStatsTransform.categories:
            add_stats_fn(category)


def add_stats_fn(category):
    def fn(self, data_frame):
        lambdafunc = lambda x: pd.Series([
            self.get_id(mcs.PlayerMap, remote_id=x['remote_player_id'], supplier_id=self.supplier_id),
            self.get_id(mc.ClubMap, remote_id=x['remote_player_team_id'], supplier_id=self.supplier_id),
            self.get_id(mc.ClubMap, remote_id=x['remote_opposing_team_id'], supplier_id=self.supplier_id)
        ])
        ids_frame = data_frame.apply(lambdafunc, axis=1)
        ids_frame.columns = ['player_id', 'player_team_id', 'opposing_team_id']
        columns_to_drop = ['remote_player_id', 'remote_player_team_id', 'remote_opposing_team_id']
        inter_frame = data_frame.join(ids_frame).drop(columns_to_drop, axis=1)
        outerlambdafunc = lambda x: pd.Series([
            self.get_id(mc.ClubMatchLineups,
                        match_id=self.get_id(
                            mc.ClubLeagueMatches,
                            home_team_id=x['player_team_id'] if x['locale'] == 'Home' else x['opposing_team_id'],
                            away_team_id=x['opposing_team_id'] if x['locale'] == 'Away' else x['player_team_id'],
                            date=x['match_date']),
                        player_id=x['player_id'])
        ])
        outerids_frame = inter_frame.apply(outerlambdafunc, axis=1)
        outerids_frame.columns = ['lineup_id']
        more_columns_to_drop = ['player_team_id', 'opposing_team_id', 'match_date', 'locale', 'player_id']
        return inter_frame.join(outerids_frame).drop(more_columns_to_drop, axis=1)

    setattr(MarcottiStatsTransform, category, fn)

    fn.__name__ = category
    fn.__doc__ = "Data transformation for {} method".format(category)
