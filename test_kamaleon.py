#!/usr/bin/env python
import serial
import time

serialport = serial.Serial("/dev/ttyO4",115200, timeout = 0.5)
ans = serialport.readline()
print("Welcome etrans!")
time_stamp = time.time()
time_stamp2 = time.time()
while True:
    if (int(time.time())-int(time_stamp)) > 45:
	print(str("+RESP:GTUDT,,,,,,,0,,1,1,,0,550.1,90,180,6667776665,,,,,,,,,,,,,,,,,,,,,,,,,,0001$\r\n"))
#	time.sleep(0.5)
	serialport.write(str("+RESP:GTUDT,,,,,,,0,,1,1,,0,550.1,90,180,6667776665,,,,,,,,,,,,,,,,,,,,,,,,,,0001$\r\n"))
#	time.sleep(0.1)
        print(str(time_stamp))
        time_stamp = time.time()
    if (int(time.time())-int(time_stamp2)) > 30:
        time_stamp2 = time.time()
#	time.sleep(0.5)
        serialport.write(str("CMD97,0\r\n"))
#	time.sleep(0.1)
	print(str("CMD97"))
    ans = serialport.readline()
    if ans:
        print(str(ans))       
#	time.sleep(0.5) 
	serialport.write(str("CMD605,98,0\r\n"))
#	time.sleep(0.1)
	#if (str(ans[0:8]) == "AT+GTUDT"):
            #time.sleep(0.5)
	    #serialport.write(str("+RESP:GTUDT,,,,,,,0,,1,1,,0,550.1,-70.613968,-33.500660,20190808000025,,,,,,,,,,,,,,,,,,,,,,,,,,0001$\r\n"))
            #time.sleep(0.1)
	    #print(str("+RESP:GTUDT,,,,,,,0,,1,1,,0,550.1,-70.613968,-33.500660,20190808000025,,,,,,,,,,,,,,,,,,,,,,,,,,0001$\r\n"))


# print(str("resp sended"))
# print("issue GTUDT")
# serialport.write(str("AT+GTUDT=gv300w,1,,45,1,,0,,60,,,,,,,FFFF$\r\n"))
# time.sleep(0.01)    
