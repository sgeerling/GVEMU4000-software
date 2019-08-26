# -*- coding: utf-8 -*-
"""
@author: gopimn
"""
import time
from models.device import device as dev
import models.gps_get as gps
import utils.share as share
import utils.utils as utils
from models.queue import Queue
from datetime import datetime
      
# these parameters are globals for now.
# when one of those is None, theres  no excecution of the timer thread,
params = {}
params['period_gtfri'] = 2
params['alert_amqp_url'] = "amqp://tester:copilotoTester01000@10.1.1.55:5672/copiloto"
params['alert_queue_name'] = "test"
#params['period_gtinf'] = 

def main():
  utils.get_imei()
  gpsp = gps.GpsPoller()
  try:
    gpsp.start()
    gvemu = dev(params)
    gvemu.start()
    print("threads started!!!!!!!!!!!!\n")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("190.216.145.154", 61000))
    while True:
      while share.to_server:
        print("server queue not empty!")
        str_to_server = share.to_server.popleft()
        print(str_to_server)

      print ("\n\nIm alive\n")
      time.sleep(1)
      
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    share.gpsp.running = False
    share.gpsp.join() # wait for the thread to finish what it's doing
    
  print ("Done.\nExiting.")
  
if __name__== "__main__":
  main()


