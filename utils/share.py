# -*- coding: utf-8 -*-
from collections import deque
import logging
imei = None
gpsd = None
to_server = deque()

#logging.basicConfig()

logger = logging.getLogger(__name__)

c_handler = logging.StreamHandler() # Log for display
f_handler = logging.FileHandler('test.log', mode='a') # Log for file


formattc = logging.Formatter('[%(asctime)s](%(levelname)s) eBot: %(message)s', datefmt='%d%m%y-%H:%M:%S')
formattf = logging.Formatter('[%(asctime)s](%(levelname)s) eBot: %(message)s', datefmt='%d%m%y-%H:%M:%S')

c_handler.setFormatter(formattc)
f_handler.setFormatter(formattf)

c_handler.setLevel(logging.DEBUG)
f_handler.setLevel(logging.DEBUG)

logger.addHandler(c_handler)
logger.addHandler(f_handler)

logger.info("logger started")
