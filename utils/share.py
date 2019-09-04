# -*- coding: utf-8 -*-
from collections import deque
import logging
imei = None
gpsd = None
to_server = deque()
logging.basicConfig()

c_handler = logging.StreamHandler() # Log for display

f_handler = logging.FileHandler('gvemu_test.log', mode='a') # Log for file

logger = logging.getLogger()



logger.setLevel(logging.DEBUG)

formatt = logging.Formatter('[%(asctime)s] (%(levelname)s@%(name)s) eBot: %(message)s', datefmt='%d%m%y-%H:%M:%S')

c_handler.setFormatter(formatt)

f_handler.setFormatter(formatt)

logger.addHandler(c_handler)

logger.addHandler(f_handler)
