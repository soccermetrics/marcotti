import overview
import personnel
import match
import events
import statistics


CSV_ETL_CLASSES = {
    'Overview': {
        'Competitions': overview.CompetitionIngest,
        'Clubs': overview.ClubIngest,
        'Venues': overview.VenueIngest
    },
    'Personnel': {
        'Players': personnel.PlayerIngest,
        'Managers': personnel.ManagerIngest,
        'Referees': personnel.RefereeIngest
    },
    'Match': {
        'Matches': match.MatchIngest,
        'Lineups': match.MatchLineupIngest,
        'Goals': events.GoalIngest,
        'Penalties': events.PenaltyIngest,
        'Bookables': events.BookableIngest,
        'Substitutions': events.SubstitutionIngest,
        'PlayerStats': [
            statistics.AssistsIngest,
            statistics.ClearancesIngest,
            statistics.CornerCrossesIngest,
            statistics.CornersIngest,
            statistics.CrossesIngest,
            statistics.DefensivesIngest,
            statistics.DisciplineIngest,
            statistics.DuelsIngest,
            statistics.FoulWinsIngest,
            statistics.FreeKicksIngest,
            statistics.GKActionsIngest,
            statistics.GKAllowedGoalsIngest,
            statistics.GKAllowedShotsIngest,
            statistics.GKSavesIngest,
            statistics.GoalBodyPartsIngest,
            statistics.GoalLineClearancesIngest,
            statistics.GoalLocationsIngest,
            statistics.GoalTotalsIngest,
            statistics.ImportantPlaysIngest,
            statistics.MatchStatIngest,
            statistics.PassDirectionsIngest,
            statistics.PassLengthsIngest,
            statistics.PassLocationsIngest,
            statistics.PassTotalsIngest,
            statistics.PenaltyActionsIngest,
            statistics.ShotBlocksIngest,
            statistics.ShotBodyPartsIngest,
            statistics.ShotLocationsIngest,
            statistics.ShotPlaysIngest,
            statistics.TacklesIngest,
            statistics.ThrowinsIngest,
            statistics.TouchesIngest,
            statistics.TouchLocationsIngest
        ]
    }
}
