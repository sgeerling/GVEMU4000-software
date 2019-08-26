# -*- coding: utf-8 -*-
"""
@author: gopimn
"""
import time
from models.device import device as dev
import models.gps_get as gps
import utils.share as share
import utils.utils as utils

      
# these parameters are globals for now.
# when one of those is None, theres  no excecution of the timer thread,
params = {}
params['period_gtfri'] = 1
#params['period_gtinf'] = 

def main():
  print("0\n")
  utils.get_imei()
  print("1\n")
  gpsp = gps.GpsPoller()
  print("2\n")
  try:
    print("4\n")
    gvemu = dev(params)
    print("5\n")
    gvemu.start()
    print("6\n")
    gpsp.run()
    print("threads started\n")
    print(share.imei)
    while True:
      print (share.imei)
      print (share.gpsd.fix.latitude)
      time.sleep(5)
      
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    share.gpsp.running = False
    share.gpsp.join() # wait for the thread to finish what it's doing
    
  print ("Done.\nExiting.")
  
if __name__== "__main__":
  main()


