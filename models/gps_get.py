from gps import *
import threading
import os

def get_imei():
  raw =os.popen("cat /var/log/messages | grep 'AT+GSN' -A 1 | tail -1").read()
  raw = str(raw)
  aux1=raw.split(": ")
  aux2=aux1[1].split("^")
  imei=aux2[0]
  return(imei)

class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    global imei
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    imei = get_imei()
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while self.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer

