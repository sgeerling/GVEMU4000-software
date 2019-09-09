# -*- coding: utf-8 -*-

from threading import Timer,Thread,Event
import os
import utils.share as share
import logging

###############################################################################
#                  Begin of Logging block
###############################################################################
logger = logging.getLogger(__name__)
c_handler = logging.StreamHandler() # Log for display
f_handler = logging.FileHandler('test.log', mode='a') # Log for file
formattc = logging.Formatter('[%(asctime)s](%(levelname)s %(name)s) eBot: %(message)s',
                             datefmt='%d%m%y-%H:%M:%S')
formattf = logging.Formatter('[%(asctime)s](%(levelname)s %(name)s) eBot: %(message)s',
                             datefmt='%d%m%y-%H:%M:%S')
c_handler.setFormatter(formattc)
f_handler.setFormatter(formattf)
logger.setLevel(logging.DEBUG)
logger.addHandler(c_handler)
logger.addHandler(f_handler)
logger.info('utils module loaded!')
###############################################################################
#                  End of Logging block
###############################################################################

def ping_inet():
    response = os.system("ping -c 1 190.153.248.100  > /dev/null 2>&1") # ugly hardcoded IP
    if response == 0:
        logger.info("cellular network up!")
        return True
    else:
        logger.info("cellular network down!")
        return False

def hrs_to_sec(value):
    return round((value * 60 * 60), 1)

def get_imei():
    with open("imei",'r') as file:
        imei=file.readline()
        logger.debug("Retrieving imei from file:")
        logger.debug(str(imei).strip())
        share.imei = str(imei).strip()

def is_gtdat(data):
    share.logger.debug("DECODE!!!!")
    data = data.decode()
    aux_0 = str(data).split(",")
    if (len(aux_0) >10):
        header = str(aux_0[0])
        logger.debug(header)
        aux_1 = "AT+GTDAT=gv300w"
        logger.debug(aux_1)
        if (header == aux_1):
            return str(aux_0[3])
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
