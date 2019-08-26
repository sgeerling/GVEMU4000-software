# -*- coding: utf-8 -*-

from utils.utils import perpetualTimer as timer
from time import ctime
import utils.share as share

class device(object):
    
    def gtfri_method(self,test_var = None):
        print("gtfri issued\n")
        
        print("Message content:\n")
        gtfri_str = ""
        # Header
        gtfri_str += "+RESP:GTFRI,"
        # Protocol ver
        gtfri_str += "270601,"
        # IMEI
        gtfri_str += str(str(share.imei)+",")
        # Dev name
        gtfri_str += ","
        # External Vcc
        gtfri_str += ","
        # Report ID
        gtfri_str += "10,"
        # Number
        gtfri_str += "1,"
        # GNSS accuracy
        gtfri_str += ","
        # Speed
        gtfri_str += str(str(share.gpsd.fix.speed)+ ",")
        # heading
        gtfri_str += "168,"
        # Altitude
        gtfri_str += str(str(share.gpsd.fix.altitude)+ ",")
        # Longitude
        gtfri_str += str(str(share.gpsd.fix.longitude)+ ",")
        # Latitude
        gtfri_str += str(str(share.gpsd.fix.latitude)+ ",")
        # Latitude
        gtfri_str += str(str(share.gpsd.fix.latitude)+ ",")
        print(gtfri_str)
        
    def gtinf_method(self,test_var = None): 
        print("gtinf into queue\n")
        
    def __init__(self,params):
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


