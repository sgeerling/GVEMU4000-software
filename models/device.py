# -*- coding: utf-8 -*-

from utils.utils import perpetualTimer as timer
from datetime import datetime
import utils.share as share
import serial

class device(object):

    def gtfri_method(self,test_var = None):
        print("\n\ngtfri issued\n")
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
        # GNSS UTC time
        gtfri_str += str((datetime.now().strftime("%Y%m%d%H%M%S")))
        # MCC
        gtfri_str += ",0730,"
        # MNC
        gtfri_str += "0001,"
        # LAC
        gtfri_str += "3536,"
        # CELL ID
        gtfri_str += "52FB390,"
        # res
        gtfri_str += "00,"
        # mileage
        gtfri_str += "104746.0,"
        # Hour meter count
        gtfri_str += ","
        # AI 1
        gtfri_str += ","
        # AI 2
        gtfri_str += ","
        # Batt %
        gtfri_str += "89,"
        # Dev status
        gtfri_str += "220110,"
        # Res
        gtfri_str += ","
        # Res
        gtfri_str += ","
        # Res
        gtfri_str += ","
        # The following params are going to be added when sending the frame
        # Send time
        # Footer
        share.to_server.append(gtfri_str) # try here

    def gtinf_method(self,test_var = None):
        print("gtinf into queue\n")

    def kamaleon_listener(self,test_var = None):

        print("Starting listener\n")

        # - [ ] Check if the port is open
        # - [ ] Check if the port has available data before calling readline
        while True:
            ans = self.serialport.readline()
            if ans:
                # What if str() fails?
                print(str(ans))
            # sleep plz????

    def print_gtudt(self,test_var = None):

        #print("EBOT: SENDING GTDUT.\n")
        print(str("+RESP:GTUDT,,,,,,,0,,1,1,,0,550.1,90,180,6667776665,,,,,,,,,,,,,,,,,,,,,,,,,,0001$\r\n"))
        # check the encpodign      issue
        self.serialport.write(b'+RESP:GTUDT,,,,,,,0,,1,1,,0,550.1,90,<LATITUDE?>,<LONGITUDE?>,,,,,,,,,,,,,,,,,,,,,,,,,,0001$\r\n')
        # - [ ] Check if the port is open
        # - [ ] Check if the port has available data before calling readline

        #while True:
        #ans = self.serialport.readline()
        #if ans:
                # What if str() fails?
        #        print(str(ans))
            # sleep plz????

    def send_to_kam(self,test_var = None):

        #print("EBOT: SENDING GTDUT.\n")
        # print(str("+RESP:GTUDT,,,,,,,0,,1,1,,0,550.1,90,180,6667776665,,,,,,,,,,,,,,,,,,,,,,,,,,0001$\r\n"))
        # check the encpodign      issue
        #ASSUMING IS A STRING
        aux = str(test_var)
        aux=aux.split(',')

        to_kam=aux[3]+aux[4]+aux[5]
        self.serialport.write(bytes(to_kam))
        # - [ ] Check if the port is open
        # - [ ] Check if the port has available data before calling readline

        #while True:
        #ans = self.serialport.readline()
        #if ans:
                # What if str() fails?
        #        print(str(ans))
            # sleep plz????

    def __init__(self,params):

        self.params = params

        # Exception for not having
        self.serialport = serial.Serial("/dev/ttyO5",115200, timeout = 0.5)

        # necesary?
        #self.born_date = str((datetime.now().strftime("%Y%m%d%H%M%S")))

        if 'period_gtfri' in params.keys():
            self.timer_gtfri = timer(params['period_gtfri'],self.gtfri_method)
        if 'period_gtinf' in params.keys():
            self.timer_gtinf = timer(params['period_gtinf'],self.gtinf_method)
        # Added in a negli way
        self.timer_gtudt = timer(2,self.print_gtudt)

    def start(self):

        if 'period_gtfri' in self.params.keys():
            self.timer_gtfri.start()
        if 'period_gtinf' in self.params.keys():
            self.timer_gtinf.start()
        # Added in a negli way
        self.timer_gtudt.start()

