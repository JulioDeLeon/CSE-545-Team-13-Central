# Possible Vulnerability Scanners

## Lynis 
### setup
- `sudo apt install lynis`
- `sudo lynis audit system` 

### Pros
- easy to use
- report is easy to read, even provides suggestions for possible fixes for found vulnerabilities. Some of which we were concerned with in our envisioning.
- can be used on remote systems

### Cons 
- does not check for web based attacks

## BurbSuite
### setup
- download tool from https://portswigger.net/burp/community-download-thank-you
- run install script for your respective system
- use built in browser to examine web based services 

### Pros
- looks like it can automate detection and attack of vulnerabilites

### Cons
- looks like it has a steep learning curve. 
- not sure if its allowed
