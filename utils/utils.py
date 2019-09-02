# -*- coding: utf-8 -*-

from threading import Timer,Thread,Event
import os
import utils.share as share

def hrs_to_sec(value):
    return round((value * 60 * 60), 1)

def get_imei():
    raw =os.popen("cat /var/log/messages | grep 'AT+GSN' -A 1 | tail -1").read()
    raw = str(raw)
    aux1=raw.split(": ")
    aux2=aux1[1].split("^")
    imei=aux2[0]
    share.imei = imei

def is_gtdat(data):
    aux = str(data).split(",")
    if (len(aux) >10):
        print(aux[0])
        if (str(aux[0]) == "AT+GTDAT=gv300w"):
            return True
    return False
            
class SqlInsertingError(Exception):
    def __init__(self, arg):
        self.args = arg


class MissingConfigurationError(Exception):
    def __init__(self, arg):
        self.args = arg


class DuplicateKeyError(Exception):
    def __init__(self, arg):
        self.args = arg

class perpetualTimer():
   def __init__(self,t,hFunction):
      # Sets the period of the timer
      self.t=t
      # Sets the function to execute in this instance of the class
      self.hFunction = hFunction
      # Creates the first timer that's going to be excecuted
      self.timer0 = Timer(self.t,self.handle_function)

   def handle_function(self):
      # executes the target function
      self.hFunction()
      # at this point, the timer0 has already been excecuted.
      # We are assigning it again and restarting it.
      self.timer0 = Timer(self.t,self.handle_function)
      self.timer0.start()

   def start(self):
      # Gives the first start to the timer.
      self.timer0.start()

   def cancel(self):
      # Stops the timer0 
      self.timer0.cancel()
