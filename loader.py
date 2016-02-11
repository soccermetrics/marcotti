from etl import get_local_handles, ingest_feeds
from etl.ecsv import CSV_ETL_CLASSES
from local import LocalConfig
from interface import Marcotti


if __name__ == "__main__":
    settings = LocalConfig()
    marcotti = Marcotti(settings)
    with marcotti.create_session() as sess:
        for group in ['Supplier', 'Overview', 'Personnel', 'Match']:
            for entity, datafile in settings.CSV_DATA.get(group, []):
                if group in ['Supplier', 'Overview', 'Personnel']:
                    if entity == 'Venues':
                        params = (sess, settings.VENUE_EFF_DATE)
                    elif entity in ['Competitions', 'Clubs', 'Players', 'Positions']:
                        params = (sess, settings.DATA_SUPPLIER)
                    else:
                        params = (sess,)
                else:
                    params = (sess, settings.COMPETITION_NAME, settings.SEASON_NAME)
                    if entity == 'PlayerStats':
                        params += (settings.DATA_SUPPLIER,)
                if type(CSV_ETL_CLASSES[group][entity]) is list:
                    for etl_class in CSV_ETL_CLASSES[group][entity]:
                        ingest_feeds(get_local_handles, settings.CSV_DATA_DIR, datafile, etl_class(*params))
                else:
                    ingest_feeds(get_local_handles, settings.CSV_DATA_DIR, datafile,
                                 CSV_ETL_CLASSES[group][entity](*params))
