# -*- coding: utf-8 -*-

from utils.utils import perpetualTimer as timer
from datetime import datetime
import utils.share as share
import serial

class device(object):

    def gtfri_method(self,test_var = None):
        print("\n\ngtfri issued\n")
        gtfri_str = ""
        gtfri_str += "+RESP:GTFRI,"# Header
        gtfri_str += "270601," # Protocol ver
        gtfri_str += str(str(share.imei)+",")# IMEI
        gtfri_str += "," # Dev name
        gtfri_str += "," # External Vcc
        gtfri_str += "10,"# Report ID
        gtfri_str += "1," # Number
        gtfri_str += "," # GNSS accuracy
        gtfri_str += str(str(share.gpsd.fix.speed)+ ",")# Speed
        gtfri_str += "168," # heading
        gtfri_str += str(str(share.gpsd.fix.altitude)+ ",")# Altitude
        gtfri_str += str(str(share.gpsd.fix.longitude)+ ",")# Longitude
        gtfri_str += str(str(share.gpsd.fix.latitude)+ ",")# Latitude
        gtfri_str += str((datetime.now().strftime("%Y%m%d%H%M%S")))# GNSS UTC time
        gtfri_str += ",0730,"# MCC
        gtfri_str += "0001," # MNC
        gtfri_str += "3536," # LAC
        gtfri_str += "52FB390," # CELL ID
        gtfri_str += "0,"# res
        gtfri_str += "104746.0," # mileage
        gtfri_str += "," # Hour meter count
        gtfri_str += ","# AI 1
        gtfri_str += "," # AI 2
        gtfri_str += "89,"# Batt %
        gtfri_str += "220110,"# Dev status
        gtfri_str += ","# Res
        gtfri_str += ","# Res
        gtfri_str += ","# Res
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
        gtudt_str = "" 
        print("eBOT: SENDING GTDUT.\n")                             # * means fixed, ! means variable
        gtudt_str += "+RESP:GTUDT,"                                 #* header
        gtudt_str += ","                                            #* Protocol Ver.
        gtudt_str += ","                                            #* FW Version
        gtudt_str += ","                                            #* HW Version
        gtudt_str += ","                                            #* Reserved
        gtudt_str += str(str(share.imei)+",")                       #! IMEI
        gtudt_str += ","                                            #* Device name
        gtudt_str += "1,"                                           #* Report type
        gtudt_str += ","                                            #* Number
        gtudt_str += ","                                            #* GPS accuracy
        gtudt_str += str(str(share.gpsd.fix.altitude)+ ",")         #! Speed
        gtudt_str += str(str(share.gpsd.fix.track)+ ",")            #! Heading, check if the angle is right
        gtudt_str += ","                                            #! Azimuth. MISSING
        gtudt_str += str(str(share.gpsd.fix.altitude)+ ",")         #! Altitude
        gtudt_str += str(str(share.gpsd.fix.longitude)+ ",")        #! Longitude
        gtudt_str += str(str(share.gpsd.fix.latitude)+ ",")         #! Latitude
        gtudt_str += str((datetime.now().strftime("%Y%m%d%H%M%S"))) # GNSS UTC time
        gtudt_str += ","                                            #* MCC
        gtudt_str += ","                                            #* MNC
        gtudt_str += ","                                            #* LAC
        gtudt_str += ","                                            #* CELL ID. is this the SIM number?
        gtudt_str += ","                                            #* Reserved
        gtudt_str += ","                                            #* Mileage, used?
        gtudt_str += ","                                            #* Reserved
        gtudt_str += ","                                            #* HMC
        gtudt_str += ","                                            #* Reserved
        gtudt_str += ","                                            #* External GPS antenna, 
        gtudt_str += ","                                            #* GSV number
        gtudt_str += ","                                            #* Geo fence state
        gtudt_str += ","                                            #* AI1
        gtudt_str += ","                                            #* AI2
        gtudt_str += ","                                            #* DI
        gtudt_str += ","                                            #* DO
        gtudt_str += ","                                            #* Motion status
        gtudt_str += ","                                            #* External power vcc
        gtudt_str += ","                                            #* Batt lvl
        gtudt_str += ","                                            #* charging
        gtudt_str += ","                                            #* geo status mask
        gtudt_str += ","                                            #* reserved
        gtudt_str += ","                                            #* reserved
        gtudt_str += ","                                            #* reserved
        gtudt_str += str((datetime.now().strftime("%Y%m%d%H%M%S"))) #! SEND TIME
        gtudt_str += ",FFFF$"                                       #* Footer
        print(str(gtudt_str))
        self.serialport.write(bytes(gtudt_str,'utf-8'))

    def send_to_kam(self,test_var = None):

        #print("EBOT: SENDING GTDUT.\n")
        # print(str("+RESP:GTUDT,,,,,,,0,,1,1,,0,550.1,90,180,6667776665,,,,,,,,,,,,,,,,,,,,,,,,,,0001$\r\n"))
        # check the encpodign      issue
        #ASSUMING IS A STRING
        aux = str(test_var)
        aux=aux.split(',')

        to_kam=aux[3]+","+aux[4]+","+aux[5]+"\r\n"
        self.serialport.write(bytes(to_kam,'utf-8'))
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

        if 'period_gtfri' in params.keys():
            self.timer_gtfri = timer(params['period_gtfri'],self.gtfri_method)
        if 'period_gtinf' in params.keys():
            self.timer_gtinf = timer(params['period_gtinf'],self.gtinf_method)
        if 'period_gtudt' in params.keys():
            self.timer_gtudt = timer(params['period_gtudt'],self.print_gtudt)
        # NEGLI'S WAY:
        kam_listener_thread = threading.Thread(target=self.kamaleon_listener, args=(1,))
        
        
    def start(self):

        if 'period_gtfri' in self.params.keys():
            self.timer_gtfri.start()
        if 'period_gtinf' in self.params.keys():
            self.timer_gtinf.start()
        if 'period_gtinf' in self.params.keys():
            self.timer_gtudt.start()
        # NEGLI'S WAY:
        self.kam_listener_thread.start()

