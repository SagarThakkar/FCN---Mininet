#!/usr/bin/python

"""
Example network of Quagga routers
(QuaggaTopo + QuaggaService)
"""

import sys
import atexit

# patch isShellBuiltin
import mininet.util
import mininext.util
mininet.util.isShellBuiltin = mininext.util.isShellBuiltin
sys.modules['mininet.util'] = mininet.util

from mininet.util import dumpNodeConnections
from mininet.node import OVSController
from mininet.log import setLogLevel, info

from mininext.cli import CLI
from mininext.net import MiniNExT

from topo import QuaggaTopo

net = None


def startNetwork():
	"instantiates a topo, then starts the network and prints debug information"

	info('** Creating Quagga network topology\n')
	topo = QuaggaTopo()

	info('** Starting the network\n')
	global net
	net = MiniNExT(topo, controller=OVSController)
	net.start()

	info('** Dumping host connections\n')
	dumpNodeConnections(net.hosts)

	

	info('** Dumping host processes\n')
	#    for host in net.hosts:
	#        host.cmdPrint("ps aux")
	#    for host in net.hosts:
	#        host.cmdPrint('ifconfig')

	# Enabling IP forwarding
	net.get("R1").cmd("sysctl -w net.ipv4.ip_forward=1")
	net.get("R2").cmd("sysctl -w net.ipv4.ip_forward=1")
	net.get("R3").cmd("sysctl -w net.ipv4.ip_forward=1")
	net.get("R4").cmd("sysctl -w net.ipv4.ip_forward=1")

	# Setting Interface IPs
	net.get("R1").cmd("ifconfig R1-eth1 172.0.2.1/24")
	net.get("R1").cmd("ifconfig R1-eth2 172.0.6.2/24")
	net.get("R2").cmd("ifconfig R2-eth1 172.0.3.1/24")
	net.get("R4").cmd("ifconfig R4-eth1 172.0.3.2/24")
	net.get("R4").cmd("ifconfig R4-eth2 172.0.5.1/24")
	net.get("R3").cmd("ifconfig R3-eth1 172.0.5.2/24")
	
	# Static Routes from R1 to R2
	net.get("H1").cmd("route add default gw 172.0.1.2")
	net.get("R1").cmd("ip route add 172.0.3.0/24 via 172.0.2.2 dev R1-eth1")
	net.get("R1").cmd("ip route add 172.0.4.0/24 via 172.0.2.2 dev R1-eth1")
	net.get("R2").cmd("ip route add 172.0.4.0/24 via 172.0.3.2 dev R2-eth1")
	
	# Allowing Nating ar each router in the path from H1 to H2	
	net.get("R1").cmd("iptables -t nat -A POSTROUTING -o R1-eth1 -j MASQUERADE")
	net.get("R1").cmd("iptables -A FORWARD -i R1-eth1 -o R1-eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT")
	net.get("R1").cmd("iptables -A FORWARD -i R1-eth0 -o R1-eth1 -j ACCEPT") 
	net.get("R2").cmd("iptables -t nat -A POSTROUTING -o R2-eth1 -j MASQUERADE")
	net.get("R2").cmd("iptables -A FORWARD -i R2-eth1 -o R2-eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT")
	net.get("R2").cmd("iptables -A FORWARD -i R2-eth0 -o R2-eth1 -j ACCEPT") 
	net.get("R4").cmd("iptables -t nat -A POSTROUTING -o R4-eth0 -j MASQUERADE")
	net.get("R4").cmd("iptables -A FORWARD -i R4-eth0 -o R4-eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT")
	net.get("R4").cmd("iptables -A FORWARD -i R4-eth1 -o R4-eth0 -j ACCEPT")


	info('** Testing network connectivity\n')
	net.ping(net.hosts)

	
	info('** Running CLI\n')
	CLI(net)


def stopNetwork():
    "stops a network (only called on a forced cleanup)"

    if net is not None:
        info('** Tearing down Quagga network\n')
        net.stop()

if __name__ == '__main__':
    # Force cleanup on exit by registering a cleanup function
    atexit.register(stopNetwork)

    # Tell mininet to print useful information
    setLogLevel('info')
    startNetwork()
