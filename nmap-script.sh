#!/bin/bash

while getopts "n:p:sh" flag;
do
    case $flag in
        n) networkip=$OPTARG;;
        p) portfile=$OPTARG;;
		s) scan='true';;
		h) 
			echo "-p Expects a file with a list of ports and the -n network arg. One port per line without a newline at the end. This will output all port infomation for the network in a file named scanned_ports. A port range can also be specified. i.e. 22-500"
			echo ""
			echo "-n Expects a network in the form of 192.168.0.0\/24"
			echo ""
			echo "-s Scans the given network and lists all the ips in a file called scanned_ips. If this value is not given, the network scan of ips will not be performed."
			exit;;
			
			
    esac
done
echo "Doing Work..."

if [[ -n "${networkip}" ]] && [[ "${scan}" ]];
then
	nmap -sn $networkip | awk '/Nmap scan/{gsub(/[()]/,"",$NF); print $NF > "scanned_ips"}'
	echo "Ips for network: $networkip saved in scanned_ips";
fi

if [[ -n "${portfile}" ]] && [[ -n "${networkip}" ]];
then
	portargs=`tr '\n' ',' < $portfile`
	nmap -sV -p $portargs $networkip > "scanned_ports"
	echo "Ports for network: $networkip saved in scanned_ports";
fi

echo "Done Boss..."
