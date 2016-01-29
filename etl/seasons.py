from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from models.common.overview import Seasons, Years


def create_seasons(session, start_yr, end_yr):
    """
    Adds Years and calendar and European Seasons records to database.

    :param session: Transaction session object.
    :param start_yr: Start of year interval.
    :param end_yr: End of year interval, inclusive.
    """
    def exists(model, **conditions):
        return session.query(model).filter_by(**conditions).count() != 0

    print "Creating Seasons..."

    YearRange = xrange(start_yr, end_yr+1)

    for yr in YearRange:
        if not exists(Years, yr=yr):
            session.add(Years(yr=yr))
    session.commit()
    session.flush()

    for start, end in zip(YearRange[:-1], YearRange[1:]):
        try:
            start_yr_obj = session.query(Years).filter_by(yr=start).one()
            end_yr_obj = session.query(Years).filter_by(yr=end).one()
        except (NoResultFound, MultipleResultsFound):
            continue
        # insert calendar year season record
        if not exists(Seasons, start_year=start_yr_obj, end_year=start_yr_obj):
            season_record = Seasons(start_year=start_yr_obj, end_year=start_yr_obj)
            session.add(season_record)
        # insert European season record
        if not exists(Seasons, start_year=start_yr_obj, end_year=end_yr_obj):
            season_record = Seasons(start_year=start_yr_obj, end_year=end_yr_obj)
            session.add(season_record)
    session.commit()
    print "Season creation complete."
