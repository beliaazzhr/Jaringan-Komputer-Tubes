#Anyelir Belia Azzahra - 1301200048

#!/usr/bin/python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.node import Node
from mininet.topo import Topo
from mininet.log import setLogLevel, info
from mininet.util import pmonitor
from signal import SIGINT
from time import time
import os



def routerNet():
    net = Mininet( link=TCLink )


#CLO1
#Membangun Topologi  
    # Add Router (Membangun objek untuk R1, R2, R3, R4)
    R1 = net.addHost( 'R1', ip='192.172.0.254/24')
    R2 = net.addHost( 'R2', ip='192.172.5.1/24')
    R3 = net.addHost( 'R3', ip='192.172.2.1/24')
    R4 = net.addHost( 'R4', ip='192.172.3.254/24')
    
    # Add Host (hostA dan hostB)
    hostA = net.addHost( 'hostA', ip='192.172.0.1/24')
    hostB = net.addHost( 'hostB', ip='192.172.2.254/24')
     
    # Add Link (Menghubungkan)
    net.addLink(hostA, R1, max_queue_size=100, intfName1='hostA-eth0',intfName2='R1-eth0', cls=TCLink, bw=1 )
    net.addLink(hostA, R2, max_queue_size=100, intfName1='hostA-eth1',intfName2='R2-eth0', cls=TCLink, bw=1 )
    net.addLink(hostB, R3, max_queue_size=100, intfName1='hostB-eth0',intfName2='R3-eth1', cls=TCLink, bw=1 )
    net.addLink(hostB, R4, max_queue_size=100, intfName1='hostB-eth1',intfName2='R4-eth1', cls=TCLink, bw=1 )
    net.addLink(R1, R3, max_queue_size=100, intfName1='R1-eth1',intfName2='R3-eth0', cls=TCLink, bw=0.5 )
    net.addLink(R1, R4, max_queue_size=100, intfName1='R1-eth2',intfName2='R4-eth2', cls=TCLink, bw=1 )
    net.addLink(R2, R4, max_queue_size=100, intfName1='R2-eth1',intfName2='R4-eth0', cls=TCLink, bw=0.5 )
    net.addLink(R2, R3, max_queue_size=100, intfName1='R2-eth2',intfName2='R3-eth2', cls=TCLink, bw=1 )
    
    # Config IP 
    
    #Memasukkan IP pada hostA
    hostA.cmd("ifconfig hostA-eth0 0")
    hostA.cmd("ifconfig hostA-eth1 0")
    hostA.cmd("ifconfig hostA-eth0 192.172.0.1 netmask 255.255.255.0")
    hostA.cmd("ifconfig hostA-eth1 192.172.5.254 netmask 255.255.255.0")
    
    #Memasukkan IP pada hostB
    hostB.cmd("ifconfig hostB-eth0 0")
    hostB.cmd("ifconfig hostB-eth1 0")
    hostB.cmd("ifconfig hostB-eth0 192.172.2.254 netmask 255.255.255.0")
    hostB.cmd("ifconfig hostB-eth1 192.172.3.1 netmask 255.255.255.0")
    
    # Config router
  
    R1.cmd( 'sysctl net.ipv4.ip_forward=1' )
    R2.cmd( 'sysctl net.ipv4.ip_forward=1' )
    R3.cmd( 'sysctl net.ipv4.ip_forward=1' )
    R4.cmd( 'sysctl net.ipv4.ip_forward=1' )
    
    # Add IP Address for Router

    #Memasukkan IP router pada R1
    R1.cmd( 'ip addr add 192.172.0.254/24 brd + dev R1-eth0' )
    R1.cmd( 'ip addr add 192.172.1.1/24 brd + dev R1-eth1' )
    R1.cmd( 'ip addr add 192.172.6.1/24 brd + dev R1-eth2' )
    
    #Memasukkan IP router pada R2
    R2.cmd( 'ip addr add 192.172.5.1/24 brd + dev R2-eth0' )
    R2.cmd( 'ip addr add 192.172.4.254/24 brd + dev R2-eth1' )
    R2.cmd( 'ip addr add 192.172.7.1/24 brd + dev R2-eth2' )
    
    #Memasukkan IP router pada R3
    R3.cmd( 'ip addr add 192.172.1.254/24 brd + dev R3-eth0' )
    R3.cmd( 'ip addr add 192.172.2.1/24 brd + dev R3-eth1' )
    R3.cmd( 'ip addr add 192.172.7.254/24 brd + dev R3-eth2' )
    
    #Memasukkan IP router pada R4
    R4.cmd( 'ip addr add 192.172.4.1/24 brd + dev R4-eth0' )
    R4.cmd( 'ip addr add 192.172.3.254/24 brd + dev R4-eth1' )
    R4.cmd( 'ip addr add 192.172.6.254/24 brd + dev R4-eth2' ) 
    
    #CLO2

    #Routing Host    
    hostA.cmd('ip rule add from 192.172.0.1 table 1')
    hostA.cmd('ip rule add from 192.172.5.254 table 2')
    hostA.cmd('ip route add 192.172.0.0/24 dev hostA-eth0 scope link table 1')
    hostA.cmd('ip route add default via 192.172.0.254 dev hostA-eth0 table 1')
    hostA.cmd('ip route add 192.172.5.0/24 dev hostA-eth1 scope link table 2')
    hostA.cmd('ip route add default via 192.172.5.1 dev hostA-eth1 table 2')
    hostA.cmd('ip route add default scope global nexthop via 192.172.0.254 dev hostA-eth0')
    hostA.cmd('ip route add default scope global nexthop via 192.172.5.1 dev hostA-eth1')
    
    hostB.cmd('ip rule add from 192.172.2.254 table 3')
    hostB.cmd('ip rule add from 192.172.3.1 table 4')
    hostB.cmd('ip route add 192.172.2.0/24 dev hostB-eth0 scope link table 3')
    hostB.cmd('ip route add default via 192.172.2.1 dev hostB-eth0 table 3')
    hostB.cmd('ip route add 192.172.3.0/24 dev hostB-eth1 scope link table 4')
    hostB.cmd('ip route add default via 192.172.2.254 dev hostB-eth1 table 4')
    hostB.cmd('ip route add default scope global nexthop via 192.172.2.1 dev hostB-eth0')
    hostB.cmd('ip route add default scope global nexthop via 192.172.3.254 dev hostB-eth1')
    
    # Static Routing (router)
    R1.cmd('route add -net 192.172.2.0/24 gw 192.172.1.254')
    R1.cmd('route add -net 192.172.3.0/24 gw 192.172.6.254')
    R1.cmd('route add -net 192.172.4.0/24 gw 192.172.6.2')
    R1.cmd('route add -net 192.172.5.0/24 gw 192.172.6.254')
    R1.cmd('route add -net 192.172.7.0/24 gw 192.172.1.254')
    
    R2.cmd('route add -net 192.172.0.0/24 gw 192.172.7.254')
    R2.cmd('route add -net 192.172.1.0/24 gw 192.172.7.254')
    R2.cmd('route add -net 192.172.2.0/24 gw 192.172.7.254')
    R2.cmd('route add -net 192.172.3.0/24 gw 192.172.4.1')
    R2.cmd('route add -net 192.172.6.0/24 gw 192.172.4.1')
    
    R3.cmd('route add -net 192.172.0.0/24 gw 192.172.1.1')
    R3.cmd('route add -net 192.172.3.0/24 gw 192.172.7.1')
    R3.cmd('route add -net 192.172.4.0/24 gw 192.172.7.1')
    R3.cmd('route add -net 192.172.5.0/24 gw 192.172.1.1')
    R3.cmd('route add -net 192.172.6.0/24 gw 192.172.1.1')
    
    R4.cmd('route add -net 192.172.0.0/24 gw 192.172.6.1')
    R4.cmd('route add -net 192.172.1.0/24 gw 192.172.6.1')
    R4.cmd('route add -net 192.172.2.0/24 gw 192.172.6.1')
    R4.cmd('route add -net 192.172.5.0/24 gw 192.172.4.254')
    R4.cmd('route add -net 192.172.7.0/24 gw 192.172.4.254')
    

        
    #Menjalankan iPerf 
    hostA.cmd('iperf -s &')
    hostB.cmd('iperf -t 40 -c 192.172.2.2 &')

    def testIperf( net, server='hostA', clients=('hostB') ):
        popens = {}
        tperf = 20
        tout = ( tperf + 1 ) * 4
        stopPerf = time() + tout + 5
        inv = 4

        popens[ net[ server ] ] = net[ server ].popen( 'iperf -s -t '+str( tout ) )
        for client in clients:
            client = 'hostB'
            popens[ net[ client ] ] = net[ client ].popen( 'iperf -c '+net[ server ].IP()+' -i '+str(inv)+' -t '+str( tperf ) )
            break

        logserver = logclient1 = logclient2 = logclient3 = ""

        for host, line in pmonitor(popens, timeoutms=(tperf + tout) * 4):
            if host:
                if host.name == server: logserver += (host.name +": "+line)
                elif host.name == clients[0]: logclient1 += (host.name +": "+line)
                # elif host.name == clients[1]: logclient2 += (host.name +": "+line)
                # elif host.name == clients[2]: logclient3 += (host.name +": "+line)

            if time() >= stopPerf:
                for p in popens.values(): p.send_signal(SIGINT)

        print(logserver)
        print(logclient1)
        print(logclient2)
        print(logclient3)
        
    
    net.start()
    net.build()
    info( '\n', net.ping() ,'\n' )
    CLI(net)
    net.stop()
    
if __name__ == "__main__":
    os.system('mn -c')
    os.system('clear')
    setLogLevel('info')
    routerNet()
