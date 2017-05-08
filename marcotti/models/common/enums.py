from models.common import DeclEnum


class GroupRoundType(DeclEnum):
    """
    Enumerated names of rounds in group stages of football competitions.
    """
    group_stage = "Group Stage", "Group Stage"
    first_round = "First Round", "First Round"
    second_round = "Second Round", "Second Round"
    third_round = "Third Round", "Third Round"
    fourth_round = "Fourth Round", "Fourth Round"
    final_round = "Final Round", "Final Round"
    playoff = "Playoff Group", "Playoff Group"
    championship = "Championship Group", "Championship Group"
    promotion = "Promotion Group", "Promotion Group"
    relegation = "Relegation Group", "Relegation Group"


class KnockoutRoundType(DeclEnum):
    """
    Enumerated names of rounds in knockout stages of football competitions.
    """
    extra_prelim = "Extra Preliminary Round", "Extra Preliminary Round"
    prelim = "Preliminary Round", "Preliminary Round"
    first_qualifying = "First Qualifying Round", "First Qualifying Round"
    second_qualifying = "Second Qualifying Round", "Second Qualifying Round"
    third_qualifying = "Third Qualifying Round", "Third Qualifying Round"
    fourth_qualifying = "Fourth Qualifying Round", "Fourth Qualifying Round"
    playoff = "Playoff Round", "Playoff Round"
    first_round = "First Round", "First Round"
    second_round = "Second Round", "Second Round"
    third_round = "Third Round", "Third Round"
    fourth_round = "Fourth Round", "Fourth Round"
    fifth_round = "Fifth Round", "Fifth Round"
    sixth_round = "Sixth Round", "Sixth Round"
    seventh_round = "Seventh Round", "Seventh Round"
    eighth_round = "Eighth Round", "Eighth Round"
    round_64 = "Round of 64 (1/32)", "Round of 64 (1/32)"
    round_32 = "Round of 32 (1/16)", "Round of 32 (1/16)"
    round_16 = "Round of 16 (1/8)", "Round of 16 (1/8)"
    quarterfinal = "Quarterfinal (1/4)", "Quarterfinal (1/4)"
    semifinal = "Semi-Final (1/2)", "Semi-Final (1/2)"
    final = "Final", "Final"
    qualifying_final = "Qualifying Final", "Qualifying Final"
    prelim_final = "Preliminary Final", "Preliminary Final"
    grand_final = "Grand Final", "Grand Final"


class ConfederationType(DeclEnum):
    """
    Enumerated names of the international football confederations.
    """
    africa = "CAF", "Confederation of African Football"
    asia = "AFC", "Asian Football Confederation"
    europe = "UEFA", "Union of European Football Associations"
    north_america = "CONCACAF", "Confederation of North, Central American, and Caribbean Association Football"
    oceania = "OFC", "Oceania Football Confederation"
    south_america = "CONMEBOL", "South American Football Confederation"
    fifa = "FIFA", "International Federation of Association Football"


class PositionType(DeclEnum):
    """
    Enumerated categories of football player positions.
    """
    goalkeeper = "Goalkeeper", "Goalkeepers"
    defender = "Defender", "Defending positions"
    midfielder = "Midfielder", "Midfield positions"
    forward = "Forward", "Forward positions"
    unknown = "Unknown", "Unknown player position"


class NameOrderType(DeclEnum):
    """
    Enumerated types of naming order conventions.
    """
    western = "Western", "Western"
    middle = "Middle", "Middle"
    eastern = "Eastern", "Eastern"


class CardType(DeclEnum):
    """
    Enumerated types of disciplinary cards.
    """
    yellow = "Yellow", "Yellow"
    yellow_red = "Yellow/Red", "Yellow/Red"
    red = "Red", "Red"


class SurfaceType(DeclEnum):
    """
    Enumerated types of playing surfaces.
    """
    natural = "Natural", "Natural"
    artificial = "Artificial", "Artificial"
    hybrid = "Hybrid", "Hybrid"


class ShotOutcomeType(DeclEnum):
    """
    Enumerated types of shot outcomes.
    """
    goal = "Goal", "Goal"
    miss = "Miss", "Miss"
    save = "Save", "Save"
    wide = "Wide of post", "Wide of post"
    over = "Over crossbar", "Over crossbar"
    post = "Hit post", "Hit post"
    bar = "Hit crossbar", "Hit crossbar"


class BodypartType(DeclEnum):
    """
    Enumerated types of body parts.
    """
    left_foot = "Left foot", "Left foot"
    right_foot = "Right foot", "Right foot"
    foot = "Foot", "Foot"
    head = "Head", "Head"
    chest = "Chest", "Chest"
    other = "Other", "Other body part"
    unknown = "Unknown", "Unknown"


class ShotEventType(DeclEnum):
    """
    Enumerated types of shot events.
    """
    unknown = "Unknown", "Unknown"
    cross_fk = "Cross from free kick", "Cross from free kick"
    cross_ck = "Cross from corner kick", "Cross from corner kick"
    cross_throw = "Cross from throw-in", "Cross from throw-in"
    cross_open_play = "Cross from open play", "Cross from open play"
    olympic = "Direct from corner kick", "Direct from corner kick"
    free_kick = "Direct from free kick", "Direct from free kick"
    flick_ck = "Flick on from corner kick", "Flick on from corner kick"
    flick_fk = "Flick on from direct free kick", "Flick on from direct free kick"
    flick_ifk = "Flick on from indirect free kick", "Flick on from indirect free kick"
    flick_throw = "Flick on from throw-in", "Flick on from throw-in"
    one_v_one = "Through pass creates 1-v-1", "Through pass creates 1-v-1"
    scramble = "Contested scramble", "Contested scramble"
    redirected = "Close-range re-direction", "Close-range re-direction"
    deflection = "Deflected shot", "Deflected shot"
    shot_6_box = "Shot inside goal area", "Shot inside goal area"
    shot_18_box = "Shot inside penalty area", "Shot inside penalty area"
    shot_outside = "Shot outside penalty area", "Shot outside penalty area"
    rebound = "Shot following rebound", "Shot following rebound"
    giveaway = "Shot following defensive giveaway", "Shot following defensive giveaway"
    round_keeper = "Maneuver around goalkeeper", "Maneuver around goalkeeper"


class FoulEventType(DeclEnum):
    """
    Enumerated types of foul events.
    """
    unknown = "Unknown", "Unknown"
    handball = "Handball", "Handball"
    holding = "Holding", "Holding"
    off_ball = "Off-ball infraction", "Off-ball infraction"
    dangerous = "Dangerous play", "Dangerous play"
    reckless = "Reckless challenge", "Reckless challenge"
    over_celebration = "Excessive celebration", "Excessive celebration"
    simulation = "Simulation", "Simulation"
    dissent = "Dissent", "Dissent"
    repeated_fouling = "Persistent infringement", "Persistent infringement"
    delay_restart = "Delaying restart", "Delaying restart"
    encroachment = "Dead ball encroachment", "Dead ball encroachment"
    field_unauthorized = "Unauthorized field entry/exit", "Unauthorized field entry/exit"
    serious_foul_play = "Serious foul play", "Serious foul play"
    violent_conduct = "Violent conduct", "Violent conduct"
    verbal_abuse = "Offensive/abusive language or gestures", "Offensive/abusive language or gestures"
    spitting = "Spitting", "Spitting"
    professional = "Professional foul", "Professional foul"
    unsporting = "Unsporting behavior", "Unsporting behavior"
    handball_block_goal = "Handball denied obvious scoring opportunity", "Handball denied obvious scoring opportunity"


class WeatherConditionType(DeclEnum):
    """
    Enumerated types of NWS/NOAA weather conditions.
    """
    clear = "Clear", "Clear"
    partly_cloudy = "Partly Cloudy", "Partly Cloudy"
    mostly_cloudy = "Mostly Cloudy", "Mostly Cloudy"
    few_clouds = "Few Clouds", "Few Clouds"
    dry_hot = "Hot and Dry", "Hot and Dry"
    humid_hot = "Hot and Humid", "Hot and Humid"
    overcast = "Overcast", "Overcast"
    fog = "Fog/Mist", "Fog/Mist"
    light_rain = "Light Rain", "Light Rain"
    rain = "Rain", "Rain"
    heavy_rain = "Heavy Rain", "Heavy Rain"
    windy_clear = "Clear and Windy", "Clear and Windy"
    windy_mostly_cloudy = "Mostly Cloudy and Windy", "Mostly Cloudy and Windy"
    windy_partly_cloudy = "Partly Cloudy and Windy", "Partly Cloudy and Windy"
    windy_overcast = "Overcast and Windy", "Overcast and Windy"
    flurries = "Snow Flurries", "Snow Flurries"
    light_snow = "Light Snow", "Light Snow"
    heavy_snow = "Heavy Snow", "Heavy Snow"
