#!/usr/bin/env python
 
from scapy.all import *
import csv

interface = "eth0"

 
#everytime when scapy receives a packet, this procedure is started
def get_mac(pkt):
	#stamgmtstypes = (0, 2, 4)
	#print p 
	#if p.haslayer(Dot11):
	#	print p
	#	if p.type == 0 and p.subtype in stamgmtstypes:
	#		if p.addr2 in device_dict:
	#			print device_dict[p.addr2]
	if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
                #return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")
		if pkt.hwsrc in device_dict:
			print device_dict[pkt.hwsrc]
		else:
			print pkt.hwsrc + " unknown"

# Wireless sniffing
#def get_mac(p):
        #stamgmtstypes = (0, 2, 4)
        #print p
        #if p.haslayer(Dot11):
        #       print p
        #       if p.type == 0 and p.subtype in stamgmtstypes:
        #               if p.addr2 in device_dict:
        #                       print device_dict[p.addr2]
        #        	else:
        #                	print p.addr2 + " unknown"



	
 
if __name__=="__main__":
 
	device_dict = {}
	for mac_address, identifier in csv.reader(open("../mac.csv")):
		device_dict[mac_address] = identifier
	sniff(iface=interface, prn=get_mac, store=0)
