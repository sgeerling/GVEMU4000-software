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
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true

  def run(self):
    global gpsd
    while self.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer


      
gpsd = None #seting the global variable
# these parameters are globals for now.
# when one of those is None, theres  no excecution of the timer thread,
params = {}
params['period_gtfri'] = 10
params['period_gtinf'] = 5
imei = get_imei()


def main():
  gvemu = dev(params)
  gvemu.start()
  print("threads started\n") 
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      print ("latitude  " +str(gpsd.fix.latitude))
      print (imei)
      time.sleep(5)
      
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    print ("\nKilling Thread...")
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
    
  print ("Done.\nExiting.")
  
if __name__== "__main__":
  main()


  # 1) revisar los gps_event_measurent Ningun paquete raro se ha encontrado
  # 2) LOGS        Los logs no muestran entradas con la imei del camión de prueba.
  # 3) Drivetech


# aaguilaru
# kaufmann01

# https://vpn.kaufmann.cl 443

# BD 10.1.1.23
# copiloto-dev 1433

# user dev-r
# pass think_pad.#82
	
