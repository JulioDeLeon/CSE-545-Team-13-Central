#!/usr/bin/env python3
import getopt
import sys

from scapy.all import *
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether

try:
    opts, args = getopt.getopt(sys.argv[1:], "",
                               ['interface=', 'machine-ip=', 'ip-ethernet-file=', 'port-file='])
except getopt.GetoptError as e:
    print(e)
for o, a in opts:
    if o in ("--interface"):
        interface = a
    if o in ("--machine-ip"):
        machine_ip = a
    if o in ("--ip-ethernet-file"):
        ip_ethernet_file = a
    if o in ("--port-file"):
        port_file = a

# ports to look at
ports = open(port_file, "r")
# expecting a list of known ips and ethernets separated by a space
ips_ethernets = open(ip_ethernet_file, "r")

def handle_packet(packet):

    if IP in packet:

        # This is intended to be a reflector/forwarder. Intention is to listen for packets coming in UDP and TCP
        # on specific ports then swap the packet destinations and send them back to the known targets.

        if packet[IP].dst == machine_ip:
            packet.show()

            # flag to send the packet if we care about it
            send_flag = False

            del packet.chksum
            if packet.haslayer(TCP):
                # check if the port is a port we care about
                if packet[TCP].dport in port_file:
                    send_flag = True
                    del packet[TCP].chksum
            elif packet.haslayer(UDP):
                # check if the port is a port we care about
                if packet[TCP].dport in ports:
                    send_flag = True
                    del packet[UDP].chksum

            # if we didn't want the packet drop it
            if send_flag :
                # send the modified packets to everything we know about
                for target in ips_ethernets:
                    t = target.split()
                    packet[Ether].dst = packet[Ether].src
                    packet[Ether].src = t[0]
                    packet[IP].dst = packet[IP].src
                    packet[IP].src = t[1]

                    # packet.show()

                    sendp(packet, iface=interface, verbose=False)

sniff(prn=handle_packet, iface=interface)
