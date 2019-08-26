# -*- coding: utf-8 -*-

from utils.utils import perpetualTimer as timer
from time import ctime

class device(object):
    
    def gtfri_method(self,test_var = None):
        print("gtfri issued\n")
        print("Message content:\n")
        gtfri_str = ""
        # Header
        gtfri_str.append("+RESP:GTFRI,")
        # Protocol ver
        gtfri_str.append("270601,")
        # IMEI
        gtfri_str.append(str(imei)+",")
        # Dev name
        gtfri_str.append(",")
        # External Vcc
        gtfri_str.append(",")
        # Report ID
        gtfri_str.append("10,")
        # Number
        gtfri_str.append("1,")
        # GNSS accuracy
        gtfri_str.append(",")
        # Speed
        gtfri_str.append(str(gpsd.fix.speed)+ ",")
        # heading
        gtfri_str.append("168,")
        # Altitude
        gtfri_str.append(str(gpsd.fix.altitude)+ ",")
        # Longitude
        gtfri_str.append(str(gpsd.fix.longitude)+ ",")
        # Latitude
        gtfri_str.append(str(gpsd.fix.latitude)+ ",")
        # Latitude
        gtfri_str.append(str(gpsd.fix.latitude)+ ",")
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


