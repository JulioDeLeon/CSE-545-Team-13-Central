# CSE-545-Team-13-Central
Repo for CTF related things

## Scripts:

### install-packages.sh
This script installs packages from packages.list Add required packages to packages.list to install them.

### arp-scan.sh
This script runs arp-scan and saves information into a file called ip.txt. This should retrieve all the ips on the local network.

  ip.txt example file:
  
    Interface: v-test, type: EN10MB, MAC: f2:88:46:94:9b:75, IPv4: 10.0.0.1
    Starting arp-scan 1.9.7 with 256 hosts (https://github.com/royhills/arp-scan)
    10.0.0.2        fa:3c:22:93:d7:6f       (Unknown: locally administered)
    10.0.0.3        ff:b2:bb:ee:aa:8f       (Unknown: locally administered)
    10.0.0.4        aa:11:86:99:88:8f       (Unknown: locally administered)

    3 packets received by filter, 0 packets dropped by kernel
    Ending arp-scan 1.9.7: 256 hosts scanned in 2.164 seconds (118.30 hosts/sec). 3 responded
