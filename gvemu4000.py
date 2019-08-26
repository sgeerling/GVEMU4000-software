# -*- coding: utf-8 -*-
"""
@author: gopimn
"""
import os
from gps import *
from time import *
import time
import threading
from models.device import device as dev
gpsd = None #seting the global variable
# these parameters are globals for now.
# when one of those is None, theres  no excecution of the timer thread,
params = {}
params['period_gtfri'] = 0.4
params['period_gtinf'] = 0.3

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


def main():
  gvemu = dev(params)
  gvemu.start()
  print("threads started\n") 
  gpsp = GpsPoller() # create the thread
  try:
    while True:
      gpsp.start() # start it up
      print ("latitude  " +gpsd.fix.latitude)
      time.sleep(5)
      
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    
  print "Done.\nExiting."
  
if __name__== "__main__":
  main()
