# -*- coding: utf-8 -*-
import os
import time
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import Float
from utils.utils import SqlInsertingError
import utils.share as share


"""
Methods to load, save and process data in the database.
"""

#
def save_queue_raw(db, alert=None):
    """
    :param db:
    :param alert: Most of the info to save in the alert log. Instance of the class Alert from alert.py
    :param alert_data: Data related to the alert request sending.
    :return:
    """

    if alert is None:
        share.logger.warning("No alert data to save...")
        return None

    try:
        result = None
        cn = db.engine.connect()

        # Insert into telemetry_alerts_log table
        meta = MetaData(db.engine)
        table = Table('test_queue_raw', meta,
                Column('Id', Integer(), primary_key=True),
                Column('raw_data', String))
        meta.create_all()

        sql_insert = table.insert().values(raw_data=alert)
        print(str(sql_insert))
        share.logger.info("Saving into DB...")
        result = cn.execute(sql_insert)
        can_alert_id = result.inserted_primary_key[0]
        cn.close()
        return int(can_alert_id)

    except Exception as e:
        share.logger.critical(e)
        cn.close()
        raise e

