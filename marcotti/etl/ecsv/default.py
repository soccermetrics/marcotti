from .base import BaseCSV, extract


class CSVExtractor(BaseCSV):

    @extract
    def suppliers(self, *args, **kwargs):
        return [dict(name=self.column_unicode("Name", **keys)) for keys in kwargs.get('data')]

    @staticmethod
    def years(start_yr, end_yr):
        return [dict(yr=yr) for yr in range(start_yr, end_yr+1)]

    @staticmethod
    def seasons(start_yr, end_yr):
        year_range = range(start_yr, end_yr+1)
        return [dict(start_year=yr, end_year=yr) for yr in year_range] + \
            [dict(start_year=start, end_year=end) for start, end in zip(year_range[:-1], year_range[1:])]

    @extract
    def countries(self, *args, **kwargs):
        return [dict(remote_id=self.column("ID", **keys),
                     name=self.column_unicode("Name", **keys),
                     code=self.column("Code", **keys),
                     confed=self.column("Confederation", **keys))
                for keys in kwargs.get('data')]

    @extract
    def competitions(self, *args, **kwargs):
        return [dict(remote_id=self.column("ID", **keys),
                     name=self.column_unicode("Name", **keys),
                     level=self.column_int("Level", **keys),
                     country=self.column_unicode("Country", **keys),
                     confed=self.column("Confederation", **keys))
                for keys in kwargs.get('data')]

    @extract
    def venues(self, *args, **kwargs):
        return [dict(remote_id=self.column("ID", **keys),
                     name=self.column_unicode("Venue Name", **keys),
                     city=self.column_unicode("City", **keys),
                     region=self.column_unicode("Region", **keys),
                     country=self.column_unicode("Country", **keys),
                     timezone=self.column_unicode("Timezone", **keys),
                     latitude=self.column_float("Latitude", **keys),
                     longitude=self.column_float("Longitude", **keys),
                     altitude=self.column_int("Altitude", **keys),
                     config_date=self.column("Config Date", **keys),
                     surface=self.column_unicode("Surface", **keys),
                     length=self.column_int("Length", **keys),
                     width=self.column_int("Width", **keys),
                     capacity=self.column_int("Capacity", **keys),
                     seats=self.column_int("Seats", **keys))
                for keys in kwargs.get('data')]

    @extract
    def surfaces(self, *args, **kwargs):
        return [dict(description=self.column_unicode("Description", **keys),
                     surface_type=self.column("Type", **keys))
                for keys in kwargs.get('data')]

    @extract
    def timezones(self, *args, **kwargs):
        return [dict(name=self.column_unicode("Name", **keys),
                     confed=self.column("Confederation", **keys),
                     offset=self.column_float("Offset", **keys))
                for keys in kwargs.get('data')]

    @extract
    def clubs(self, *args, **kwargs):
        return [dict(remote_id=self.column("ID", **keys),
                     name=self.column_unicode("Name", **keys),
                     short_name=self.column_unicode("Short Name", **keys),
                     country=self.column_unicode("Country", **keys))
                for keys in kwargs.get('data')]

    @extract
    def managers(self, *args, **kwargs):
        return [dict(remote_id=self.column("ID", **keys),
                     first_name=self.column_unicode("First Name", **keys),
                     known_first_name=self.column_unicode("Known First Name", **keys),
                     middle_name=self.column_unicode("Middle Name", **keys),
                     last_name=self.column_unicode("Last Name", **keys),
                     second_last_name=self.column_unicode("Second Last Name", **keys),
                     nick_name=self.column_unicode("Nickname", **keys),
                     name_order=self.column("Name Order", **keys) or "Western",
                     dob=self.column("Birthdate", **keys),
                     country=self.column_unicode("Country", **keys))
                for keys in kwargs.get('data')]

    @extract
    def referees(self, *args, **kwargs):
        return [dict(remote_id=self.column("ID", **keys),
                     first_name=self.column_unicode("First Name", **keys),
                     known_first_name=self.column_unicode("Known First Name", **keys),
                     middle_name=self.column_unicode("Middle Name", **keys),
                     last_name=self.column_unicode("Last Name", **keys),
                     second_last_name=self.column_unicode("Second Last Name", **keys),
                     nick_name=self.column_unicode("Nickname", **keys),
                     name_order=self.column("Name Order", **keys) or "Western",
                     dob=self.column("Birthdate", **keys),
                     country=self.column_unicode("Country", **keys))
                for keys in kwargs.get('data')]

    @extract
    def players(self, *args, **kwargs):
        return [dict(remote_id=self.column("ID", **keys),
                     first_name=self.column_unicode("First Name", **keys),
                     known_first_name=self.column_unicode("Known First Name", **keys),
                     middle_name=self.column_unicode("Middle Name", **keys),
                     last_name=self.column_unicode("Last Name", **keys),
                     second_last_name=self.column_unicode("Second Last Name", **keys),
                     nick_name=self.column_unicode("Nickname", **keys),
                     name_order=self.column("Name Order", **keys) or "Western",
                     dob=self.column("Birthdate", **keys),
                     country=self.column_unicode("Country", **keys),
                     position_name=self.column_unicode("Position", **keys),
                     eff_date=self.column("Effective Date", **keys),
                     height=self.column_float("Height", **keys),
                     weight=self.column_int("Weight", **keys))
                for keys in kwargs.get('data')]

    @extract
    def positions(self, *args, **kwargs):
        return [dict(remote_id=self.column("ID", **keys),
                     name=self.column_unicode("Name", **keys),
                     position_type=self.column("Type", **keys))
                for keys in kwargs.get('data')]

    @extract
    def league_matches(self, *args, **kwargs):
        return [dict(remote_id=self.column("ID", **keys),
                     competition=self.column_unicode("Competition", **keys),
                     season=self.column("Season", **keys),
                     date=self.column("Match Date", **keys),
                     match_time=self.column("KO Time", **keys),
                     matchday=self.column_int("Matchday", **keys),
                     venue=self.column_unicode("Venue", **keys),
                     home_team=self.column_unicode("Home Team", **keys),
                     away_team=self.column_unicode("Away Team", **keys),
                     home_manager=self.column_unicode("Home Manager", **keys),
                     away_manager=self.column_unicode("Away Manager", **keys),
                     referee=self.column_unicode("Referee", **keys),
                     attendance=self.column_int("Attendance", **keys),
                     kickoff_temp=self.column_float("KO Temp", **keys),
                     kickoff_humid=self.column_float("KO Humidity", **keys),
                     half_1=self.column_int("1st Half", **keys),
                     half_2=self.column_int("2nd Half", **keys),
                     kickoff_wx=self.column("KO Wx", **keys),
                     halftime_wx=self.column("HT Wx", **keys),
                     fulltime_wx=self.column("FT Wx", **keys))
                for keys in kwargs.get('data')]

    @extract
    def group_matches(self, *args, **kwargs):
        return [dict(remote_id=self.column("ID", **keys),
                     competition=self.column_unicode("Competition", **keys),
                     season=self.column("Season", **keys),
                     date=self.column("Match Date", **keys),
                     match_time=self.column("KO Time", **keys),
                     round=self.column("Group Round", **keys),
                     group=self.column("Group", **keys),
                     matchday=self.column_int("Matchday", **keys),
                     venue=self.column_unicode("Venue", **keys),
                     home_team=self.column_unicode("Home Team", **keys),
                     away_team=self.column_unicode("Away Team", **keys),
                     home_manager=self.column_unicode("Home Manager", **keys),
                     away_manager=self.column_unicode("Away Manager", **keys),
                     referee=self.column_unicode("Referee", **keys),
                     attendance=self.column_int("Attendance", **keys),
                     kickoff_temp=self.column_float("KO Temp", **keys),
                     kickoff_humid=self.column_float("KO Humidity", **keys),
                     half_1=self.column_int("1st Half", **keys),
                     half_2=self.column_int("2nd Half", **keys),
                     kickoff_wx=self.column("KO Wx", **keys),
                     halftime_wx=self.column("HT Wx", **keys),
                     fulltime_wx=self.column("FT Wx", **keys))
                for keys in kwargs.get('data')]

    @extract
    def knockout_matches(self, *args, **kwargs):
        return [dict(remote_id=self.column("ID", **keys),
                     competition=self.column_unicode("Competition", **keys),
                     season=self.column("Season", **keys),
                     date=self.column("Match Date", **keys),
                     match_time=self.column("KO Time", **keys),
                     round=self.column("Knockout Round", **keys),
                     matchday=self.column_int("Matchday", **keys),
                     venue=self.column_unicode("Venue", **keys),
                     home_team=self.column_unicode("Home Team", **keys),
                     away_team=self.column_unicode("Away Team", **keys),
                     home_manager=self.column_unicode("Home Manager", **keys),
                     away_manager=self.column_unicode("Away Manager", **keys),
                     referee=self.column_unicode("Referee", **keys),
                     attendance=self.column_int("Attendance", **keys),
                     kickoff_temp=self.column_float("KO Temp", **keys),
                     kickoff_humid=self.column_float("KO Humidity", **keys),
                     kickoff_wx=self.column("KO Wx", **keys),
                     halftime_wx=self.column("HT Wx", **keys),
                     fulltime_wx=self.column("FT Wx", **keys),
                     half_1=self.column_int("1st Half", **keys),
                     half_2=self.column_int("2nd Half", **keys),
                     extra_1=self.column_int("1st Extra", **keys),
                     extra_2=self.column_int("2nd Extra", **keys),
                     extra_time=self.column_bool("Extra Time", **keys))
                for keys in kwargs.get('data')]

    @extract
    def match_lineups(self, *args, **kwargs):
        return [dict(remote_match_id=self.column("Match ID", **keys),
                     player_team=self.column_unicode("Player's Team", **keys),
                     player_name=self.column_unicode("Player", **keys),
                     starter=self.column_bool("Starting", **keys),
                     captain=self.column_bool("Captain", **keys))
                for keys in kwargs.get('data')]

    @extract
    def goals(self, *args, **kwargs):
        return [dict(remote_match_id=self.column("Match ID", **keys),
                     scoring_team=self.column_unicode("Scoring Team", **keys),
                     scorer=self.column_unicode("Player", **keys),
                     scoring_event=self.column("Event", **keys) or "Unknown",
                     bodypart_desc=self.column("Bodypart", **keys) or "Unknown",
                     match_time=self.column_int("Time", **keys),
                     stoppage_time=self.column_int("Stoppage", **keys) or 0)
                for keys in kwargs.get('data')]

    @extract
    def penalties(self, *args, **kwargs):
        return [dict(remote_match_id=self.column("Match ID", **keys),
                     penalty_taker=self.column_unicode("Player", **keys),
                     penalty_foul=self.column("Foul", **keys) or "Unknown",
                     penalty_outcome=self.column("Outcome", **keys),
                     match_time=self.column_int("Time", **keys),
                     stoppage_time=self.column_int("Stoppage", **keys) or 0)
                for keys in kwargs.get('data')]

    @extract
    def bookables(self, *args, **kwargs):
        return [dict(remote_match_id=self.column("Match ID", **keys),
                     player=self.column_unicode("Player", **keys),
                     foul_desc=self.column("Foul", **keys) or "Unknown",
                     card_type=self.column("Card", **keys),
                     match_time=self.column_int("Time", **keys),
                     stoppage_time=self.column_int("Stoppage", **keys) or 0)
                for keys in kwargs.get('data')]

    @extract
    def substitutions(self, *args, **kwargs):
        return [dict(remote_match_id=self.column("Match ID", **keys),
                     in_player_name=self.column_unicode("Player In", **keys),
                     out_player_name=self.column("Player Out", **keys),
                     match_time=self.column_int("Time", **keys),
                     stoppage_time=self.column_int("Stoppage", **keys) or 0)
                for keys in kwargs.get('data')]

    @extract
    def penalty_shootouts(self, *args, **kwargs):
        return [dict(remote_match_id=self.column("Match ID", **keys),
                     penalty_taker=self.column_unicode("Player", **keys),
                     penalty_number=self.column("Number", **keys),
                     penalty_outcome=self.column("Outcome", **keys))
                for keys in kwargs.get('data')]


class CSVStatsExtractor(BaseCSV):

    def player_data(self, data_row):
        return dict(remote_player_id=self.column("Player ID", **data_row),
                    remote_player_team_id=self.column("Team Id", **data_row),
                    remote_opposing_team_id=self.column("Opposition Id", **data_row),
                    match_date=self.column("Date", **data_row),
                    locale=self.column("Venue", **data_row),
                    )

    @extract
    def assists(self, *args, **kwargs):
        return [dict(totals=self.column_int("Assists", **keys),
                     corners=self.column_int("Goal Assist Corner", **keys),
                     freekicks=self.column_int("Goal Assist Free Kick", **keys),
                     throwins=self.column_int("Goal Assist Throw In", **keys),
                     goalkicks=self.column_int("Goal Assist Goal Kick", **keys),
                     setpieces=self.column_int("Goal Assist Set Piece", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def clearances(self, *args, **kwargs):
        return [dict(total=self.column_int("Total Clearances", **keys),
                     headed=self.column_int("Headed Clearances", **keys),
                     other=self.column_int("Other Clearances", **keys),
                     goalline=self.column_int("Clearances Off the Line", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def corners(self, *args, **kwargs):
        return [dict(totals=self.column_int("Corners Taken incl short corners", **keys),
                     short=self.column_int("Short Corners", **keys),
                     box_success=self.column_int("Successful Corners into Box", **keys),
                     box_failure=self.column_int("Unsuccessful Corners into Box", **keys),
                     left_success=self.column_int("Successful Corners Left", **keys),
                     left_failure=self.column_int("Unsuccessful Corners Left", **keys),
                     right_success=self.column_int("Successful Corners Right", **keys),
                     right_failure=self.column_int("Unsuccessful Corners Right", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def corner_crosses(self, *args, **kwargs):
        return [dict(total_success=self.column_int("Successful Crosses Corners", **keys),
                     total_failure=self.column_int("Unsuccessful Crosses Corners", **keys),
                     air_success=self.column_int("Successful Crosses Corners in the air", **keys),
                     air_failure=self.column_int("Unsuccessful Crosses Corners in the air", **keys),
                     left_success=self.column_int("Successful Crosses Corners Left", **keys),
                     left_failure=self.column_int("Unsuccessful Crosses Corners Left", **keys),
                     right_success=self.column_int("Successful Crosses Corners Right", **keys),
                     right_failure=self.column_int("Unsuccessful Crosses Corners Right", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def crosses(self, *args, **kwargs):
        return [dict(air_success=self.column_int("Successful crosses in the air", **keys),
                     air_failure=self.column_int("Unsuccessful crosses in the air", **keys),
                     openplay_success=self.column_int("Successful open play crosses", **keys),
                     openplay_failure=self.column_int("Unsuccessful open play crosses", **keys),
                     left_success=self.column_int("Successful Crosses Left", **keys),
                     left_failure=self.column_int("Unsuccessful Crosses Left", **keys),
                     right_success=self.column_int("Successful Crosses Right", **keys),
                     right_failure=self.column_int("Unsuccessful Crosses Right", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def defensives(self, *args, **kwargs):
        return [dict(blocks=self.column_int("Blocks", **keys),
                     intercepts=self.column_int("Interceptions", **keys),
                     recovers=self.column_int("Recoveries", **keys),
                     corners=self.column_int("Corners Conceded", **keys),
                     fouls=self.column_int("Total Fouls Conceded", **keys),
                     challenges_lost=self.column_int("Challenge Lost", **keys),
                     handballs=self.column_int("Handballs Conceded", **keys),
                     penalties=self.column_int("Penalties Conceded", **keys),
                     errs_goals=self.column_int("Error leading to Goal", **keys),
                     errs_shots=self.column_int("Error leading to Attempt", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def discipline(self, *args, **kwargs):
        return [dict(yellows=self.column_int("Yellow Cards", **keys),
                     reds=self.column_int("Red Cards", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def duels(self, *args, **kwargs):
        return [dict(total_won=self.column_int("Duels won", **keys),
                     total_lost=self.column_int("Duels lost", **keys),
                     aerial_won=self.column_int("Aerial Duels won", **keys),
                     aerial_lost=self.column_int("Aerial Duels lost", **keys),
                     ground_won=self.column_int("Ground Duels won", **keys),
                     ground_lost=self.column_int("Ground Duels lost", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def foul_wins(self, *args, **kwargs):
        return [dict(total=self.column_int("Total Fouls Won", **keys),
                     total_danger=self.column_int("Fouls Won in Danger Area inc pens", **keys),
                     total_penalty=self.column_int("Foul Won Penalty", **keys),
                     total_nodanger=self.column_int("Fouls Won not in danger area", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def freekicks(self, *args, **kwargs):
        return [dict(ontarget=self.column_int("Direct Free-kick On Target", **keys),
                     offtarget=self.column_int("Direct Free-kick Off Target", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def gk_actions(self, *args, **kwargs):
        return [dict(catches=self.column_int("Catches", **keys),
                     punches=self.column_int("Punches", **keys),
                     drops=self.column_int("Drops", **keys),
                     crosses_noclaim=self.column_int("Crosses not Claimed", **keys),
                     distrib_success=self.column_int("GK Successful Distribution", **keys),
                     distrib_failure=self.column_int("GK Unsuccessful Distribution", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def gk_allowed_goals(self, *args, **kwargs):
        return [dict(insidebox=self.column_int("Goals Conceded Inside Box", **keys),
                     outsidebox=self.column_int("Goals Conceded Outside Box", **keys),
                     is_cleansheet=self.column_bool("Clean Sheets", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def gk_allowed_shots(self, *args, **kwargs):
        return [dict(insidebox=self.column_int("Shots On Conceded Inside Box", **keys),
                     outsidebox=self.column_int("Shots On Conceded Outside Box", **keys),
                     bigchances=self.column_int("Big Chances Faced", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def gk_saves(self, *args, **kwargs):
        return [dict(insidebox=self.column_int("Saves Made from Inside Box", **keys),
                     outsidebox=self.column_int("Saves Made from Outside Box", **keys),
                     penalty=self.column_int("Saves from Penalty", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def goal_bodyparts(self, *args, **kwargs):
        return [dict(headed=self.column_int("Headed Goals", **keys),
                     left_foot=self.column_int("Left Foot Goals", **keys),
                     right_foot=self.column_int("Right Foot Goals", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def goal_locations(self, *args, **kwargs):
        return [dict(insidebox=self.column_int("Goals from Inside Box", **keys),
                     outsidebox=self.column_int("Goals from Outside Box", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def goal_totals(self, *args, **kwargs):
        return [dict(is_firstgoal=self.column_bool("First Goal", **keys),
                     is_winner=self.column_bool("Winning Goal", **keys),
                     freekick=self.column_int("Goals from Direct Free Kick", **keys),
                     openplay=self.column_int("Goals Open Play", **keys),
                     corners=self.column_int("Goals from Corners", **keys),
                     throwins=self.column_int("Goals from Throws", **keys),
                     penalties=self.column_int("Goals from penalties", **keys),
                     substitute=self.column_int("Goals as a substitute", **keys),
                     other=self.column_int("Other Goals", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def goalline_clearances(self, *args, **kwargs):
        return [dict(insidebox=self.column_int("Shots Cleared off Line Inside Area", **keys),
                     outsidebox=self.column_int("Shots Cleared off Line Outside Area", **keys),
                     totalshots=self.column_int("Shots Cleared off Line", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def important_plays(self, *args, **kwargs):
        return [dict(corners=self.column_int("Key Corner", **keys),
                     freekicks=self.column_int("Key Free Kick", **keys),
                     throwins=self.column_int("Key Throw In", **keys),
                     goalkicks=self.column_int("Key Goal Kick", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def pass_directions(self, *args, **kwargs):
        return [dict(pass_forward=self.column_int("Pass Forward", **keys),
                     pass_backward=self.column_int("Pass Backward", **keys),
                     pass_left=self.column_int("Pass Left", **keys),
                     pass_right=self.column_int("Pass Right", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def pass_lengths(self, *args, **kwargs):
        return [dict(short_success=self.column_int("Successful Short Passes", **keys),
                     short_failure=self.column_int("Unsuccessful Short Passes", **keys),
                     long_success=self.column_int("Successful Long Passes", **keys),
                     long_failure=self.column_int("Unsuccessful Long Passes", **keys),
                     flickon_success=self.column_int("Successful Flick-Ons", **keys),
                     flickon_failure=self.column_int("Unsuccessful Flick-Ons", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def pass_locations(self, *args, **kwargs):
        return [dict(ownhalf_success=self.column_int("Successful Passes Own Half", **keys),
                     ownhalf_failure=self.column_int("Unsuccessful Passes Own Half", **keys),
                     opphalf_success=self.column_int("Successful Passes Opposition Half", **keys),
                     opphalf_failure=self.column_int("Unsuccessful Passes Opposition Half", **keys),
                     defthird_success=self.column_int("Successful Passes Defensive third", **keys),
                     defthird_failure=self.column_int("Unsuccessful Passes Defensive third", **keys),
                     midthird_success=self.column_int("Successful Passes Middle third", **keys),
                     midthird_failure=self.column_int("Unsuccessful Passes Middle third", **keys),
                     finthird_success=self.column_int("Successful Passes Final third", **keys),
                     finthird_failure=self.column_int("Unsuccessful Passes Final third", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def pass_totals(self, *args, **kwargs):
        return [dict(total_success=self.column_int("Total Successful Passes All", **keys),
                     total_failure=self.column_int("Total Unsuccessful Passes All", **keys),
                     total_no_cc_success=self.column_int("Total Successful Passes Excl Crosses Corners", **keys),
                     total_no_cc_failure=self.column_int("Total Unsuccessful Passes Excl Crosses Corners", **keys),
                     longball_success=self.column_int("Successful Long Balls", **keys),
                     longball_failure=self.column_int("Unsuccessful Long Balls", **keys),
                     layoffs_success=self.column_int("Successful Lay-Offs", **keys),
                     layoffs_failure=self.column_int("Unsuccessful Lay-Offs", **keys),
                     throughballs=self.column_int("Through Ball", **keys),
                     keypasses=self.column_int("Key Passes", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def penalty_actions(self, *args, **kwargs):
        return [dict(taken=self.column_int("Penalties Taken", **keys),
                     saved=self.column_int("Penalties Saved", **keys),
                     offtarget=self.column_int("Penalties Off Target", **keys),
                     ontarget=self.column_int("Attempts from Penalties on target", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def shot_blocks(self, *args, **kwargs):
        return [dict(freekick=self.column_int("Blocked Direct Free-kick", **keys),
                     insidebox=self.column_int("Blocked Shots from Inside Box", **keys),
                     outsidebox=self.column_int("Blocked Shots Outside Box", **keys),
                     headed=self.column_int("Headed Blocked Shots", **keys),
                     leftfoot=self.column_int("Left Foot Blocked Shots", **keys),
                     rightfoot=self.column_int("Right Foot Blocked Shots", **keys),
                     other=self.column_int("Other Blocked Shots", **keys),
                     total=self.column_int("Blocked Shots", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def shot_bodyparts(self, *args, **kwargs):
        return [dict(head_ontarget=self.column_int("Headed Shots On Target", **keys),
                     head_offtarget=self.column_int("Headed Shots Off Target", **keys),
                     left_ontarget=self.column_int("Left Foot Shots On Target", **keys),
                     left_offtarget=self.column_int("Left Foot Shots Off Target", **keys),
                     right_ontarget=self.column_int("Right Foot Shots On Target", **keys),
                     right_offtarget=self.column_int("Right Foot Shots Off Target", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def shot_locations(self, *args, **kwargs):
        return [dict(insidebox_ontarget=self.column_int("Shots On from Inside Box", **keys),
                     insidebox_offtarget=self.column_int("Shots Off from Inside Box", **keys),
                     outsidebox_ontarget=self.column_int("Shots On Target Outside Box", **keys),
                     outsidebox_offtarget=self.column_int("Shots Off Target Outside Box", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def shot_plays(self, *args, **kwargs):
        return [dict(openplay_ontarget=self.column_int("Attempts Open Play on target", **keys),
                     openplay_offtarget=self.column_int("Attempts Open Play off target", **keys),
                     setplay_ontarget=self.column_int("Attempts from Set Play on target", **keys),
                     setplay_offtarget=self.column_int("Attempts from Set Play off target", **keys),
                     freekick_ontarget=self.column_int("Attempts from Direct Free Kick on target", **keys),
                     freekick_offtarget=self.column_int("Attempts from Direct Free Kick off target", **keys),
                     corners_ontarget=self.column_int("Attempts from Corners on target", **keys),
                     corners_offtarget=self.column_int("Attempts from Corners off target", **keys),
                     throwins_ontarget=self.column_int("Attempts from Throws on target", **keys),
                     throwins_offtarget=self.column_int("Attempts from Throws off target", **keys),
                     other_ontarget=self.column_int("Other Shots On Target", **keys),
                     other_offtarget=self.column_int("Other Shots Off Target", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def shot_totals(self, *args, **kwargs):
        return [dict(ontarget=self.column_int("Shots On Target inc goals", **keys),
                     offtarget=self.column_int("Shots Off Target inc woodwork", **keys),
                     bigchances=self.column_int("Big Chances", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def tackles(self, *args, **kwargs):
        return [dict(won=self.column_int("Tackles Won", **keys),
                     lost=self.column_int("Tackles Lost", **keys),
                     lastman=self.column_int("Last Man Tackle", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def throwins(self, *args, **kwargs):
        return [dict(teamplayer=self.column_int("Throw Ins to Own Player", **keys),
                     oppplayer=self.column_int("Throw Ins to Opposition Player", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def touches(self, *args, **kwargs):
        return [dict(dribble_overruns=self.column_int("Take-Ons Overrun", **keys),
                     dribble_success=self.column_int("Successful Dribbles", **keys),
                     dribble_failure=self.column_int("Unsuccessful Dribbles", **keys),
                     balltouch_success=self.column_int("Successful Ball Touch", **keys),
                     balltouch_failure=self.column_int("Unsuccessful Ball Touch", **keys),
                     possession_loss=self.column_int("Dispossessed", **keys),
                     total=self.column_int("Touches", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]

    @extract
    def touch_locations(self, *args, **kwargs):
        return [dict(finalthird=self.column_int("Touches open play final third", **keys),
                     oppbox=self.column_int("Touches open play opp box", **keys),
                     oppsix=self.column_int("Touches open play opp six yards", **keys),
                     **self.player_data(keys))
                for keys in kwargs.get('data')]
