# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine


class Database:
    def __init__(self,
                 db_name=os.environ['ETRANS_DB'],
                 username=os.environ['ETRANS_USERNAME'],
                 pw=os.environ['ETRANS_PW'],
                 host=os.environ['ETRANS_HOST'],
                 port=int(os.environ['ETRANS_PORT'])):

        self.engine = create_engine('mssql+pymssql://{}:{}@{}:{}/{}'.format(username, pw, host, port, db_name))


if __name__ == '__main__':
    db = Database()
