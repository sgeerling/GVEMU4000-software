# -*- coding: utf-8 -*-

from utils.utils import perpetualTimer as timer
from time import ctime
from gps import *
import time
import threading

gpsd = None #seting the global variable

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

class device(object):
    
    def gtfri_method(self,test_var = None): 
        print("gtfri into queue\n")
        print(gpsd.utc)
        
    def gtinf_method(self,test_var = None): 
        print("gtinf into queue\n")
        print(gpsd.fix.latitude)
        
    def __init__(self,params):
        #global gpsd #bring it in the device class scope
        gpsp = GpsPoller() # create the thread
        gpsp.start() # start it up try here
        self.params = params
        self.born_date = ctime()
        if 'period_gtfri' in params.keys():
            self.timer_gtfri = timer(params['period_gtfri'],self.gtfri_method)
        if 'period_gtinf' in params.keys():
            self.timer_gtinf = timer(params['period_gtinf'],self.gtinf_method)
            
    def start(self):
        if 'period_gtfri' in self.params.keys():
            self.timer_gtfri.start()
        if 'period_gtinf' in self.params.keys():
            self.timer_gtinf.start()


#https://stackoverflow.com/questions/3295065/gpsd-python-client
