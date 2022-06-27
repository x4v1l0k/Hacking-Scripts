import argparse, os, logging, netifaces
from colorama import init
from termcolor import colored
from multiprocessing import Process, Manager
init()
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
try:
	import ipaddress
except ImportError:
	exit(colored("You need ipaddress!\n", "red")+colored("You can instal it with", "cyan")+colored(" pip3 install ipaddress", "yellow", attrs=['bold'])+colored(" or dowload it from ", "cyan")+colored("https://github.com/phihag/ipaddress", "yellow"))
try:
	import scapy.all as scapy
except ImportError:
	exit(colored("You need scapy!\n", "red")+colored("You can instal it with", "cyan")+colored(" pip3 install scapy", "yellow", attrs=['bold'])+colored(" or dowload it from ", "cyan")+colored("https://github.com/secdev/scapy", "yellow"))

def getArguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--ip", dest="ip", help="target ip address or a ip range like x.x.x.x/x")
	parser.add_argument("-d", "--device", dest="device", help="Network interface device")
	parser.add_argument("-t", "--timeout", dest="default_timeout", help="default timeout for the host recognition.", type=int)
	parser.add_argument("-a", "--alive", action="store_true", help="show only alive hosts")
	parser.add_argument("-o", "--output", dest="output", help="save to log file")
	parser.add_argument("-oc", "--output-clean", dest="output_clean", help="save to log file only ip addresses")
	parser.add_argument("-v", "--verbose", action="store_true", help="mainly for debugging")
	args = parser.parse_args()
	if not args.device:
		args.device = netifaces.gateways()['default'][netifaces.AF_INET][1]
	if not args.ip:
		parser.error(colored("[-] Please specify a ip address or a network range with format x.x.x.x/x", "red"))
	if not args.default_timeout:
		args.default_timeout = 1
	return args

def printBanner():
	print(colored("   __             __        ", "cyan")+colored("___   _                              ", "yellow")+"""
"""+colored("  / /  ___   ___ / /_ ___  ", "cyan")+colored("/ _ \ (_)___ ____ ___  _  __ ___  ____", "yellow")+"""
"""+colored(" / _ \/ _ \ (_-</ __/(_-< ", "cyan")+colored("/ // // /(_-</ __// _ \| |/ // -_)/ __/", "yellow")+"""
"""+colored("/_//_/\___//___/\__//___/", "cyan")+colored("/____//_//___/\__/ \___/|___/ \__//_/   ", "yellow")+"""
"""+colored("                      Made by: x4v1l0k", "green")+"""
_________________________________________________________________\n""")

def tcpSynPing(options, ip, ipStatus, verbose):
	ans, unans = scapy.sr(scapy.IP(dst=ip) / scapy.TCP(dport=80, flags="S"), iface=options.device, timeout=options.default_timeout, verbose=verbose)
	for a in ans: ipStatus.append(a[1].src)

def tcpAckPing(options, ip, ipStatus, verbose):
	ans, unans = scapy.sr(scapy.IP(dst=ip) / scapy.TCP(dport=80, flags="A"), iface=options.device, timeout=options.default_timeout, verbose=verbose)
	for a in ans: ipStatus.append(a[1].src)

def arpPing(options, ip, ipStatus, verbose):
	ans, unans = scapy.srp(scapy.Ether(dst="ff:ff:ff:ff:ff:ff") / scapy.ARP(pdst=ip), iface=options.device, timeout=options.default_timeout, verbose=verbose)
	for a in ans: ipStatus.append(a[1].src)

def icmpPing(options, ip, ipStatus, verbose):
	ans, unans = scapy.sr(scapy.IP(dst=ip) / scapy.ICMP(), iface=options.device, timeout=options.default_timeout, verbose=verbose)
	for a in ans: ipStatus.append(a[1].src)

def checkHost(options, ip):
	with Manager() as manager:
		ipStatus = manager.list()
		ip = str(ip)
		verbose = 1 if options.verbose else 0
		pTcpSynPing = Process(target=tcpSynPing, args=(options, ip, ipStatus, verbose, ))
		pTcpAckPing = Process(target=tcpAckPing, args=(options, ip, ipStatus, verbose, ))
		pArpPing = Process(target=arpPing, args=(options, ip, ipStatus, verbose, ))
		pIcmpPing = Process(target=icmpPing, args=(options, ip, ipStatus, verbose, ))
		pTcpSynPing.start()
		pTcpAckPing.start()
		pArpPing.start()
		pIcmpPing.start()
		pTcpSynPing.join()
		pTcpAckPing.join()
		pArpPing.join()
		pIcmpPing.join()
		return True if len(ipStatus) > 0 else False

def printResult(options, ip, status):
	if options.alive and status != "alive":
		return
	color = "green" if status == "alive" else "red"
	print("Host "+colored(ip, "yellow", attrs=['bold'])+" is: "+colored(status, color, attrs=['bold']))

def appendToLog(options, outfile, ip, status):
	if (options.alive and status != "alive") or not outfile:
		return
	if options.output:
		outfile.write("Host {ip} is {status}\n".format(ip=ip, status=status))
	elif options.output_clean:
		outfile.write("{}\n".format(ip))
	outfile.flush()

if __name__ == '__main__':
	if os.name != 'nt' and os.geteuid() != 0:
		print(colored("This script needs to be run as root as it uses sockets.", "red", attrs=['bold']))
		exit()
	printBanner()
	options = getArguments()
	if options.output:
		outfile = open(options.output, 'a')
	elif options.output_clean:
		outfile = open(options.output_clean, 'a')
	else:
		outfile = False

	for ip in ipaddress.IPv4Network(options.ip):
		ipStatus = []
		status = "alive" if checkHost(options, ip) else "dead"
		printResult(options, ip, status)
		appendToLog(options, outfile, ip, status)

	if outfile:
		outfile.close()
