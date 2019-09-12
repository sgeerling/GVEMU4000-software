# -*- coding: utf-8 -*-
"""
@author: gopimn
"""
import serial
import time
from models.device import GVDevice as dev
import models.gps_get as gps
import utils.share as share
import utils.utils as utils
from models.queue import Queue
from datetime import datetime
import socket
import os
import logging
from models import dblite
# 79 chars according to PEP 8
###############################################################################
# these parameters are globals for now.
# when one of those is None, theres  no excecution of the timer thread,
# this variable should be on utils/share.py
params = {}
params['period_gtfri'] = 2
params['period_gtudt'] = 2
#params['period_gtinf'] =
server_ip_add = "190.216.145.154"
server_port = 61000

# TO define:
#
# imei path
# log path
# sqlite path

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
logger.info('Welcome main eTrancer!')
###############################################################################
#                  End of Logging block
###############################################################################

def main():
    utils.get_imei()
    gpsp = gps.GpsPoller()
    # if db doesnt exists, create tables and stuff # log PLZ!
    if not os.path.isfile('mydb.sqlite'):
        share.dbms = dblite.MyDatabase(dblite.SQLITE, dbname='mydb.sqlite')
        share.dbms.create_db_tables()
    else:
        share.dbms = dblite.MyDatabase(dblite.SQLITE, dbname='mydb.sqlite')
    try:
        gpsp.start()
        gvemu = dev(params)
        gvemu.start()
        logger.info("threads started!")
        # get element
        # try to send them
        # if recieved back ack change bd state of the element
        while True:
            logger.debug("New inet agent loop iteration!")
            if utils.ping_inet():
                unsended = share.dbms.select_io_unsended()
                if unsended:
                    logger.debug("Unsended msgs found in local DB")
                    # SOCKET UGLY HARDCODED
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((server_ip_add, server_port))
                    s.settimeout(5) # Important timeout if your connection is slow =)
                    for row in unsended:
                        curr_id = row[0]
                        str_to_server = str(row[2])
                        str_to_server +=\
                            str((datetime.now().strftime("%Y%m%d%H%M%S")))
                        str_to_server += ",FFFF$"
                        logger.info("Trying to send: %s", str_to_server)
                        try:
                            s.sendall(str_to_server.encode())
                            time.sleep(0.1)
                            data = s.recv(1024)
                            if data:
                                logger.info("Recieved from server: %s", str(data))
                                logger.info("Updating flag for message local id: %s", str(curr_id))
                                share.dbms.updae_io_sended(curr_id)
                                gvemu.send_to_kam(data)
                                logger.info("Data sended to Kamaleon (tty5)")
                            else:
                                logger.info("No ACK recieved in time. Msg not updated in DB ")
                        except socket.timeout as e:
                            logger.error("Exception raised:", exc_info=True)
                    s.close()
            time.sleep(1)
    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        logger.error("Killing thread")
        share.gpsp.running = False
        share.gpsp.join() # wait for the thread to finish what it's doing
        logger.error("ciao =)")

if __name__== "__main__":
    main()
#EOF!
