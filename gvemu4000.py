# -*- coding: utf-8 -*-
"""
@author: gopimn
"""
import time
from models.device import device as dev
from models.gps_get import gpsd, GpsPoller
import utils.share as share
import utils.utils as utils

      
# these parameters are globals for now.
# when one of those is None, theres  no excecution of the timer thread,
params = {}
params['period_gtfri'] = 1
#params['period_gtinf'] = 

def main():
  utils.get_imei()
  try:
    gvemu = dev(params)
    gvemu.start()
    print("threads started\n")
    print(share.imei)
    while True:
      print (share.imei)
      time.sleep(5)
      
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    #gpsp.running = False
    #gpsp.join() # wait for the thread to finish what it's doing
    
  print ("Done.\nExiting.")
  
if __name__== "__main__":
  main()


