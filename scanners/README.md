# Possible Vulnerability Scanners

## Lynis 
### setup
- `sudo apt install lynis`
- `sudo lynis audit system` 

### Pros
- easy to use
- report is easy to read, even provides suggestions for possible fixes for found vulnerabilities. Tool was able to find vulnerabilities on my vanilla Ubuntu Machine. (but nothing on my superior Debian machine). Warnings as passwords not being set, vulnerable packages installed, bad nameserver configuration, and empty iptable configurations being loaded. Some of which we were concerned with in our envisioning.
- can be used on remote systems

### Cons 