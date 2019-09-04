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
import logging

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

logging.basicConfig()

c_handler = logging.StreamHandler() # Log for display
f_handler = logging.FileHandler('gvemu_test.log', mode='a') # Log for file

logger = logging.getLogger()

logger.addHandler(c_handler)
logger.addHandler(f_handler)



logger.debug('invisible magic')  # <-- magic

logger.setLevel(logging.DEBUG)

formatt = logging.Formatter('[%(asctime)s] (%(levelname)s@%(name)s) eBot: %(message)s', datefmt='%d%m%y-%H:%M:%S')

logger.setFormatter(formatt)


logger.info('Welcome eTrancer!')

# logging.basicConfig()
# logging.StreamHandler()
# a = logging.FileHandler('gvemu_test.log', mode='a')
# logger = logging.getLogger(__name__)
# logger.addHandler(a)
# logger.setLevel(logging.DEBUG)

# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')

while True:
    time.sleep(1)
    
def main():
    utils.get_imei()
    gpsp = gps.GpsPoller()
    try:
        gpsp.start()
        gvemu = dev(params)
        gvemu.start()
        logger.info("threads started!")
        while True:
            if share.to_server:
                logger.debug("server queue not empty!")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # UGLY HARDCODE
                s.connect((server_ip_add, server_port))
                s.settimeout(1)
                while share.to_server:
                    str_to_server = share.to_server.popleft()
                    str_to_server +=\
                                  str((datetime.now().strftime("%Y%m%d%H%M%S")))
                    str_to_server += ",FFFF$"
                    logger.info("Transmitting: %s", str_to_server)
                    try:
                        s.sendall(str_to_server.encode())
                        time.sleep(0.1)
                        data = s.recv(1024)
                        if data:
                            logger.info("recieved from server: %s", str(data))
                            gvemu.send_to_kam(data)
                    except socket.timeout as e:
                        logger.error("Exception raised:", exc_info=True)
                    finally:
                        s.close()
                    logger.info("I'm alive")
                    time.sleep(1)

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        logger.error("Killing thread")
        share.gpsp.running = False
        share.gpsp.join() # wait for the thread to finish what it's doing
        logger.error("ciao =)")
        

if __name__== "__main__":
    main()
    #EOF
