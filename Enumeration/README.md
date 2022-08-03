# hostsDiscover

```
   __             __        ___   _                              
  / /  ___   ___ / /_ ___  / _ \ (_)___ ____ ___  _  __ ___  ____
 / _ \/ _ \ (_-</ __/(_-< / // // /(_-</ __// _ \| |/ // -_)/ __/
/_//_/\___//___/\__//___//____//_//___/\__/ \___/|___/ \__//_/   
                      Made by: x4v1l0k
_________________________________________________________________

usage: hostsDiscover.py [-h] [-i IP] [-d DEVICE] [-t DEFAULT_TIMEOUT] [-a] [-o OUTPUT] [-oc OUTPUT_CLEAN] [-v]

options:
  -h, --help                                    Show this help message and exit
  -i IP, --ip IP                                Target ip address or a ip range like x.x.x.x/x
  -l LIST, --list LIST                          File with list of target ip address (one per line)
  -d DEVICE, --device DEVICE                    Network interface device
  -t TIMEOUT, --timeout TIMEOUT                 Default timeout for the host recognition
  -p PORTS, --ports PORTS                       List of ports for testing comma separated ("all" for all ports). Ex: 21,22,80
  -tp TOPPORTS, --top-ports TOPPORTS            List of top ports for testing (Choose from: 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000)
  -s SCAN, --scan SCAN                          List of scan types comma separated (all, icmp, syn, ack, synack, arp, steal, xmas, fin, null). Ex: syn,ack
  -o OUTPUT, --output OUTPUT                    Save alive ips to log file
  -v, --verbose                                 Mainly for debugging
  ```
