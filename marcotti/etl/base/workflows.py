from datetime import date

import pandas as pd
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound

from marcottievents.models.common.suppliers import Suppliers


class ETL(object):
    """
    Top-level ETL workflow.

    Receive extracted data from XML and/or CSV sources, transform/validate it, and load it to database.
    """

    def __init__(self, **kwargs):
        self.supplier = kwargs.get('supplier')
        self.transformer = kwargs.get('transform')(kwargs.get('session'), self.supplier)
        self.loader = kwargs.get('load')(kwargs.get('session'), self.supplier)

    def workflow(self, entity, *data):
        """
        Implement ETL workflow for a specific data entity:

        1. Combine data extracted from data sources.
        2. Transform and validate combined data into IDs and enums in the Marcotti database.
        3. Load transformed data into the database if it is not already there.

        :param entity: Data model name
        :param data: Data payloads from XML and/or CSV sources, in lists of dictionaries
        """
        getattr(self.loader, entity)(getattr(self.transformer, entity)(self.combiner(*data)))

    @staticmethod
    def combiner(*data_dicts):
        """
        Combine data from primary and supplemental data sources using unique ID of primary records.

        Returns a Pandas DataFrame of the combined data.

        :param data_dicts: List of data payloads from data sources, primary source first in list.
        :return: DataFrame of combined data.
        """
        data_frames = [pd.DataFrame(data) for data in data_dicts]
        if len(data_frames) > 1:
            new_frames = [data_frame.dropna(axis=1, how='all') for data_frame in data_frames]
            return pd.merge(*new_frames, on=['remote_id'])
        return data_frames[0]


class WorkflowBase(object):

    def __init__(self, session, supplier):
        self.session = session
        self.supplier_id = self.get_id(Suppliers, name=supplier) if supplier else None

    def get_id(self, model, **conditions):
        try:
            record_id = self.session.query(model).filter_by(**conditions).one().id
        except NoResultFound as ex:
            print "{} has no records in Marcotti database for: {}".format(model.__name__, conditions)
            return None
        except MultipleResultsFound as ex:
            print "{} has multiple records in Marcotti database for: {}".format(model.__name__, conditions)
            return None
        return record_id

    @staticmethod
    def make_date_object(iso_date):
        """
        Convert ISO date string into datetime.date object.

        :param iso_date: Date string in ISO 8601 format.
        :return: :class:`datetime.date` object.
        """
        try:
            yr, mo, da = [int(x) for x in iso_date.split('-')]
            return date(yr, mo, da)
        except ValueError:
            return None
