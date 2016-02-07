from interface import Marcotti
from models.config.local import LocalConfig
from etl import get_local_handles, ingest_feeds
from etl.ecsv import CSV_ETL_CLASSES


if __name__ == "__main__":
    settings = LocalConfig()
    marcotti = Marcotti(settings)
    with marcotti.create_session() as sess:
        for group in ['Overview', 'Personnel', 'Match']:
            for entity, datafile in settings.CSV_DATA[group]:
                if group in ['Overview', 'Personnel']:
                    if entity == 'Venues':
                        params = (sess, settings.VENUE_EFF_DATE)
                    else:
                        params = (sess,)
                else:
                    params = (sess, settings.COMPETITION_NAME, settings.SEASON_NAME)
                if CSV_ETL_CLASSES[group][entity] is list:
                    for etl_class in CSV_ETL_CLASSES[group][entity]:
                        ingest_feeds(get_local_handles, settings.CSV_DATA_DIR, datafile, etl_class(*params))
                else:
                    ingest_feeds(get_local_handles, settings.CSV_DATA_DIR, datafile,
                                 CSV_ETL_CLASSES[group][entity](*params))
