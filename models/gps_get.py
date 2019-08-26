from gps import *
import threading
import utils.share as share

share.gpsd = None

class GpsPoller(threading.Thread):
  def __init__(self):
    print("00\n")
    threading.Thread.__init__(self)
    global share.gpsd #bring it in scope
    share.gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    #global gpsd
    while self.running:
      share.gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

