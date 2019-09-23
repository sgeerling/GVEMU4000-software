from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
import logging

###############################################################################
#                  Begin of Logging block
###############################################################################
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler() # Log for display
f_handler = logging.FileHandler('test.log', mode='a') # Log for file
formattc = logging.Formatter('[%(asctime)s](%(levelname)s %(name)s) eBot: %(message)s',
                             datefmt='%d%m%y-%H:%M:%S')
formattf = logging.Formatter('[%(asctime)s](%(levelname)s %(name)s) eBot: %(message)s',
                             datefmt='%d%m%y-%H:%M:%S')
c_handler.setFormatter(formattc)
f_handler.setFormatter(formattf)
logger.setLevel(logging.DEBUG)
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.info('sqlite3 module loaded!')
###############################################################################
#                  End of Logging block
###############################################################################

# Global Variables
SQLITE                  = 'sqlite'

# Table Names
SERIAL_IN  = 'serial_in'
SERIAL_OUT = 'serial_out'
INET_IN    = 'inet_in'
INET_OUT   = 'inet_out'

class MyDatabase:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html
    DB_ENGINE = {
        SQLITE: 'sqlite:///{DB}'
    }

    # Main DB Connection Ref Obj
    db_engine = None
    def __init__(self, dbtype, username='', password='', dbname=''):
        dbtype = dbtype.lower()
        if dbtype in self.DB_ENGINE.keys():
            engine_url = self.DB_ENGINE[dbtype].format(DB=dbname)
            self.db_engine = create_engine(engine_url)
            logger.info("DB engine connected OK =)")
            logger.info(self.db_engine)
        else:
            logger.error("DBType is not found in DB_ENGINE")

    def create_db_tables(self):
        metadata = MetaData()
        users = Table(SERIAL_IN, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('tstamp', String),
                      Column('msg', String),
                      )

        users = Table(SERIAL_OUT, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('tstamp', String),
                      Column('msg', String),
                      Column('sent', Integer)
                      )

        users = Table(INET_IN, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('tstamp', String),
                      Column('msg', String),
                      )

        users = Table(INET_OUT, metadata,
                      Column('id', Integer, primary_key=True),
                      Column('tstamp', String),
                      Column('msg', String),
                      Column('sent', Integer)
                      )
        try:
            metadata.create_all(self.db_engine)
            logger.info("Tables created")
        except Exception as e:
            logger.error("Error occurred during Table creation!")
            logger.error("Exception raised:",exc_info = True)


    def execute_query(self, query=''):
        if query == '' : return
        with self.db_engine.connect() as connection:
            try:
                res = connection.execute(query)
                return res
            except Exception as e:
                logger.error("Error occurred during query")
                logger.error("Exception raised:",exc_info = True)

    def execute_query_get_id(self, query=''):
        if query == '' : return
        query_id = "SELECT last_insert_rowid();"
        with self.db_engine.connect() as connection:
            try:
                res = connection.execute(query)
                res = connection.execute(query_id)
            except Exception as e:
                logger.error("Error occurred during query")
                logger.error("Exception raised:",exc_info = True)
            else:
                for row in res:
                    insert_id = row[0] # what if no answer??
                res.close()
        return insert_id

    def print_all_data(self, table='', query=''):
        query = query if query != '' else "SELECT * FROM '{}';".format(table)
        with self.db_engine.connect() as connection:
            try:
                result = connection.execute(query)
            except Exception as e:
                logger.error("Error occurred during query")
                logger.error("Exception raised:",exc_info = True)
            else:
                for row in result:
                    print(row) # print(row[0], row[1], row[2])
                result.close()
        print("\n")

    def execute_query_get_data(self, query=''):
        if query == '' : return
        with self.db_engine.connect() as connection:
            try:
                res = connection.execute(query)
            except Exception as e:
                logger.error("Error occurred during query")
                logger.error("Exception raised:",exc_info = True)
            else:
                data = []
                for row in res:
                    data += [row]# what if no answer??
                res.close()
                return data

    def insert_si(self, timestamp, message):
        # insert incomming msg from serial 5. Currently we are just
        # working with serial 5 on the BBB.
        query = "INSERT INTO {}(tstamp, msg)".format(SERIAL_IN)
        query += " VALUES ('{}','{}');".format(timestamp,message)
        return self.execute_query_get_id(query)

    def insert_ii(self, timestamp, message):
        query = "INSERT INTO {}(tstamp, msg)".format(INET_IN)
        query += " VALUES ('{}','{}');".format(timestamp,message)
        return self.execute_query_get_id(query)

    def insert_io(self, timestamp, message):
        query = "INSERT INTO {}(tstamp, msg, sent)".format(INET_OUT)
        query += " VALUES ('{}','{}',0);".format(timestamp,message)
        return self.execute_query_get_id(query)

    def insert_so(self, timestamp, message):
        query = "INSERT INTO {}(tstamp, msg, sent)".format(SERIAL_OUT)
        query += " VALUES ('{}','{}',0);".format(timestamp,message)
        return self.execute_query_get_id(query)

    def updae_io_sended(self, id):
        query = "UPDATE {} set sent=1 WHERE id={}"\
            .format(INET_OUT, id)
        self.execute_query(query)
        #self.print_all_data(USERS)


    def updae_so_sended(self, id):
        query = "UPDATE {} set sent=1 WHERE id={}"\
            .format(SERIAL_OUT, id)
        self.execute_query(query)

    def select_io_unsended(self):
        query = "SELECT * FROM {table} where sent = 0;".format(table = INET_OUT)
        return self.execute_query_get_data(query)

    def select_so_unsended(self):
        query = "SELECT * FROM {table} where sent = 0;".format(table = SERIAL_OUT)
        return self.execute_query_get_data(query)

    # def sample_query(self):
    #     # Sample Query
    #     query = "SELECT first_name, last_name FROM {TBL_USR} WHERE " \
    #             "last_name LIKE 'M%';".format(TBL_USR=USERS)
    #     self.print_all_data(query=query)
    #     # Sample Query Joining
    #     query = "SELECT u.last_name as last_name, " \
    #             "a.email as email, a.address as address " \
    #             "FROM {TBL_USR} AS u " \
    #             "LEFT JOIN {TBL_ADDR} as a " \
    #             "WHERE u.id=a.user_id AND u.last_name LIKE 'M%';" \
    #         .format(TBL_USR=USERS, TBL_ADDR=ADDRESSES)
    #     self.print_all_data(query=query)

    # def sample_delete(self):
    #     # Delete Data by Id
    #     query = "DELETE FROM {} WHERE id=3".format(USERS)
    #     self.execute_query(query)
    #     self.print_all_data(USERS)
    #     # Delete All Data
    #     '''
    #     query = "DELETE FROM {}".format(USERS)
    #     self.execute_query(query)
    #     self.print_all_data(USERS)
    #     '''

    # def sample_insert(self):
    #     # Insert Data
    #     query = "INSERT INTO {}(id, first_name, last_name) " \
    #             "VALUES (3, 'Terrence','Jordan');".format(USERS)
    #     self.execute_query(query)
    #     self.print_all_data(USERS)

    # def sample_update(self):
    #     # Update Data
    #     query = "UPDATE {} set first_name='XXXX' WHERE id={id}"\
    #         .format(USERS, id=3)
    #     self.execute_query(query)
    #     self.print_all_data(USERS)

# https://www.pythonsheets.com/notes/python-sqlalchemy.html
