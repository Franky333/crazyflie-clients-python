#from http://forum.bitcraze.se/viewtopic.php?f=9&t=1488


import sys
sys.path.append("lib")

#from crazyradio import Crazyradio
from cflib.drivers.crazyradio import Crazyradio


cr = Crazyradio()

cr.set_channel(27) #change if needed
cr.set_data_rate(cr.DR_2MPS) #change if needed

if cr.send_packet((0xff, 0xfe, 0xff)).ack:   # Init the reboot
	if cr.send_packet((0xff, 0xfe, 0xf0, 0)).ack:   # Reboot to Bootloader
#	if cr.send_packet((0xff, 0xfe, 0xf0, 1)).ack:   # Reboot to Firmware
		print "Reboot to Bootloader sucessfull!"
	else:
		print "Reboot to Bootloader failed!\nPower CF on and check connection settings."
else:
	print "Reboot to Bootloader failed!\nPower CF on and check connection settings."

