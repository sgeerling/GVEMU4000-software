# GVEMU4000!!!

(GE-VE-MU 4 triple o')

This project aims to generate a replica of the queclink GV300w. The idea is to use a [BeagleBone Black](https://beagleboard.org/black) to get info from the 
telemetry devices, connect a GNSS and a cellular antenna like the picture:

![image](https://user-images.githubusercontent.com/5314353/62744785-27208400-ba16-11e9-9ed0-4a4f340d5279.png)

The current progress was done on [archlinux](https://www.archlinux.org/): 
```
uname -a

Linux HagalePues 5.1.2-arch1-1-ARCH #1 SMP PREEMPT Wed May 15 00:09:47 UTC 2019 x86_64 GNU/Linux

```
## Image burning and eMMC flashing

We need to burn and install into the eMMC the image from the [manufacturer's page](https://beagleboard.org/latest-images), the [IoT flasher](https://debian.beagleboard.org/images/BBB-blank-debian-9.5-iot-armhf-2018-10-07-4gb.img.xz) is the one used on this iteration (aug 2019).

Once downloaded, decompress it with _unxz_:

```
unxz BBB-blank-debian-9.5-iot-armhf-2018-10-07-4gb.img.xz
```

And then burn it a micro SD card with _dd_:
```
dd bs=4M if=BBB-blank-debian-9.5-iot-armhf-2018-10-07-4gb.img  of=/dev/mmcblk0 status=progress
```
The uSD card must be empty (no partitions or nothing, I use _gparted_ to ensure that, creating a new partition table).

Ater _dd_ is done, insert the uSD and power on the board. The leds will start to blink.

After aprox 5 minutes, the device will power off. remove the sd card, the image has being burned correctly.

Now connect it to a router that has an internet connection via the RJ-45 jack, the board will automatically get an IP trough DHCP.

In our specific case its 192.168.0.101, and ssh is activated by default

```
ssh debian@192.168.0.101
```

The default password is "_temppwd_". For getting super user credential use _sudo_ for each command or _sudo su_:

```
apt-get update && apt-get upgrade
```

It's going to take a time... Think about getting a coffe or two (or three).
## UART

If not installed, install the packet _bb-cape-overlays_:

```
apt-get install bb-cape-overlays
```

Now edit the file:

```
emacs /boot/uenv.txt
```

Change the following lines:

```
#uboot_overlay_addr0=/lib/firmware/<file0>.dtbo
#uboot_overlay_addr1=/lib/firmware/<file1>.dtbo
#uboot_overlay_addr2=/lib/firmware/<file2>.dtbo
#uboot_overlay_addr3=/lib/firmware/<file3>.dtbo
```

for:

```
uboot_overlay_addr0=/lib/firmware/BB-UART1-00A0.dtbo
uboot_overlay_addr1=/lib/firmware/BB-UART2-00A0.dtbo
uboot_overlay_addr2=/lib/firmware/BB-UART4-00A0.dtbo
uboot_overlay_addr3=/lib/firmware/BB-UART5-00A0.dtbo
```

And add the following line

```
cape_enable=capemgr.enable_partno=BB-UART1,BB-UART2,BB-UART4,BB-UART5
```

Reboot and uarts 1,2,4 and 5 will be woking.

## GSM

The current wiring:

![image](https://user-images.githubusercontent.com/5314353/63189758-b8a17e80-c032-11e9-956e-75c4e714a885.png)

_pppd_ comes installed by default, so first add the following file:

```
/etc/ppp/peers/etrans
```

with contents:
```
connect "/usr/sbin/chat -v -f /etc/chatscripts/gprs -T m2m.entel.cl"
/dev/ttyO2
9600
noipdefault
usepeerdns
defaultroute
persist
noauth
nocrtscts
local
replacedefaultroute
```

One of the functions on the program uses _/var/log/messages_ to get the IMEI value of the internet module. In order to get this information, we must add to _/etc/chatscripts/gprs_ before the connection is issued:
```
OK            AT+GSN
```

You can see that we are using an m2m entel SIM card, change the credentials if needed.
Now we need to add the APN credentials to the following files:

```
echo "entelpcs * entelpcs" >> /etc/ppp/peers/etrans
```
and

```
echo "entelpcs * entelpcs" >> /etc/ppp/peerspap-secrets
```

If you haven't activate the serial: 

```
config-pin P9.22 uart
config-pin P9.21 uart
```
In order to test the GSM module we can use _screen_:

```
screen /dev/ttyO2 9600
```

and issue a simple AT command:

```
at
OK
```

If the module answer OK then we are ready to activate pppd. Detach the screen instance with _CTRL+A CTRL+D_ then get the instance identifier number  with:

```
screen -ls
```

A number is shown. Kill the screen instance:

```
screen -X -S <ID> kill
```

That way the serial port resource is free. Activate the pppd interface with

```
pon etrans
```

You should be able to see the new _ppp0_ interface

```
ip a

...

7: ppp0: <POINTOPOINT,MULTICAST,NOARP,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UNKNOWN group default qlen 3
    link/ppp 
    inet 10.4.130.45 peer 10.64.64.64/32 scope global ppp0
       valid_lft forever preferred_lft forever
```

__YAY!!__ we have an internet connection now. Maybe you are going to need to add google dns to esolv.config


```
echo "nameserver 8.8.8.8" >>/etc/resolv.conf
```

and remember to add the following to _ /etc/network/interfaces_:

```
    auto etrans
    iface etrans inet ppp
    	provider etrans
```

This way it will connect on boot if posible.

In case you run in some trouble you can see the logs:

```
cat /var/log/syslog |grep ppp
```

If you want to use the serial port in other thin, remember to turn of the interface

```
poff etrans
```

## GPS

The current wiring is:

![image](https://user-images.githubusercontent.com/5314353/63393631-e9aee580-c389-11e9-9858-b3b39ba9b21c.png)

First, install gpsd and his clients:

```
apt-get install gpsd gpsd-clients
```

Configure pins 11 and 13 to be used as _uart4_, if you haven't activate the serial 4: 

```
config-pin P9.11 uart
config-pin P9.13 uart
```

Disable the debian default service (it's configured on a different serial port)

```
systemctl stop gpsd.socket
systemctl disable gpsd.socket
```

Enable daemon manually:

```
gpsd /dev/ttyO4 -F /var/run/gpsd.sock
```

And monitor the results with:

```
cgps -s
```

or

```
gpsmon
```

Now well, in order to start automatically _gpsd_ at boot, check that the file _/lib/systemd/system/gpsd.service_:

```
[Unit]
Description=GPS (Global Positioning System) Daemon
Requires=gpsd.socket
# Needed with chrony SOCK refclock
After=chronyd.service

[Service]
EnvironmentFile=-/etc/default/gpsd
ExecStart=/usr/sbin/gpsd -N $GPSD_OPTIONS $DEVICES

[Install]
Also=gpsd.socket

```

and the onfiguration file _/etc/default/gpsd_:

```
START_DAEMON="true"
GPSD_OPTIONS="-n"
DEVICES="/dev/ttyO4"
USBAUTO="false"
GPSD_SOCKET="/var/run/gpsd.sock"

```

Now you can enable the service:

```
systemctl enable gpsd
```

and start it if you want:

```
systemctl start gpsd
```

## for the python3 venv

The default python version that the unit is currently using is python 2.7, so we have to use the _python3_ ad _pip3_  commands. First install the _virtualenv_ pip package (on the project folder):

```
pip3 install virtualenv
```

Now create the virtual environment folder:

```
virtualenv virtual_python
```

This may take a while...

Gt inside the venv using:

```
source virtual_python/bin/activate
```

Now on the venv, install the gps libraries:
```
pip3 install gps
```

Pika is also needed
```
pip3 install pika
```

DOnt forget pyserial 

~~~~
pip3 install pyserial
~~~~

And for the local DB

~~~~
pip3 install sqlalchemy
~~~~

Install slite3

~~~~
apt-get install sqlite3
~~~~

## Service for the gvemu application

To add a daemon at startup that runs the application, create the file _/lib/systemd/system/gv.service_, with the following content:
```
[Unit]
Description = eTrans gvemu daemon
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
#Restart=always
#RestartSec=1
ExecStart = /home/debian/git/GVEMU4000-software/gv_daemon.sh

[Install]
Wanted
By=multi-user.target
```

Then you can do:
```
systemctl enable gv.service
systemctl start gv.service
```


