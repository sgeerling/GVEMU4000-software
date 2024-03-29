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



share.logger.info('Welcome eTrancer!')
    
def main():
    utils.get_imei()
    gpsp = gps.GpsPoller()
    try:
        gpsp.start()
        gvemu = dev(params)
        gvemu.start()
        share.logger.info("threads started!")
        while True:
            if share.to_server:
                share.logger.debug("server queue not empty!")
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # UGLY HARDCODE
                s.connect((server_ip_add, server_port))
                s.settimeout(1)
                while share.to_server:
                    str_to_server = share.to_server.popleft()
                    str_to_server +=\
                                  str((datetime.now().strftime("%Y%m%d%H%M%S")))
                    str_to_server += ",FFFF$"
                    share.logger.info("Transmitting: %s", str_to_server)
                    try:
                        s.sendall(str_to_server.encode())
                        time.sleep(0.1)
                        data = s.recv(1024)
                        if data:
                            share.logger.info("recieved from server: %s", str(data))
                            gvemu.send_to_kam(data)
                    except socket.timeout as e:
                        share.logger.error("Exception raised:", exc_info=True)
                s.close()
                share.logger.info("I'm alive")
                time.sleep(0.8)

    except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
        share.logger.error("Killing thread")
        share.gpsp.running = False
        share.gpsp.join() # wait for the thread to finish what it's doing
        share.logger.error("ciao =)")
        

if __name__== "__main__":
    main()
    #EOF
