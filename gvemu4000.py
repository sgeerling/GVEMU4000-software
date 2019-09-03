# -*- coding: utf-8 -*-
"""
@author: gopimn
"""
import serial
import time
from models.device import device as dev
import models.gps_get as gps
import utils.share as share
import utils.utils as utils
from models.queue import Queue
from datetime import datetime
import socket

# these parameters are globals for now.
# when one of those is None, theres  no excecution of the timer thread,
# this variable should be on utils/share.py
params = {}
params['period_gtfri'] = 2
params['period_gtudt'] = 2
#params['period_gtinf'] =
server_ip_add = "190.216.145.154"
server_port = 61000
def main():
  utils.get_imei()
  gpsp = gps.GpsPoller()
  try:
    gpsp.start()
    gvemu = dev(params)
    gvemu.start()
    print("threads started!!!!!!!!!!!!\n")
    while True:
      if share.to_server:
        print("\nEBOT:server queue not empty!\n")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # UGLY HARDCODE
        s.connect((server_ip_add, server_port))
        s.settimeout(0.5)
        while share.to_server:
          str_to_server = share.to_server.popleft()
          str_to_server += str((datetime.now().strftime("%Y%m%d%H%M%S")))
          str_to_server += ",FFFF$"
          print(str_to_server)
          try:
            s.sendall(str_to_server.encode())
            time.sleep(0.1)
            data = s.recv(1024)
            if data:
              print("\nEBOT: SENDED FROM SERVER\n")
              print(data)
              gvemu.send_to_kam(data)
          except socket.timeout:
            print("TIMEOUT")
          
        s.close()
      print ("\n\nIm alive\n")
      time.sleep(1)

  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    share.gpsp.running = False
    share.gpsp.join() # wait for the thread to finish what it's doing

  print ("Done.\nExiting.")

if __name__== "__main__":
  main()
#EOF
