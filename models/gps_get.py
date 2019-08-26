from gps import *
import threading
import utils.share as share

share.gpsd = None

class GpsPoller(threading.Thread):
  def __init__(self):
    print("00\n")
    threading.Thread.__init__(self)
    print("01\n")
    #global share.gpsd #bring it in scope
    share.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    print("02\n")
    self.current_value = None
    print("03\n")
    self.running = True #setting the thread running to true
    print("04\n")
    
  def run(self):
    #global gpsd
    print("06\n")
    while self.running:
        print("07\n")
        share.gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

