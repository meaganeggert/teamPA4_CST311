#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from mininet.term import makeTerm   # import makeTerm to allow xterm to run the chat server file using h4 on networks startup
from subprocess import call
import subprocess
import time

# subprocess.run(["sudo", "-E", "python3", "certificate_generation.py"]) ---------------> moved to line 74 to make use of ip_addresses.txt

def save_ip_addresses(net):
    with open("ip_addresses.txt", "w") as file:
        for host in net.hosts:
            ip = host.IP()
            file.write(f"{host.name}: {ip}\n")
        file.close()

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    # moved switches before routers
    # mininet needs to create switches before the legacy routers
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    r5 = net.addHost('r5', cls=Node, ip='10.0.2.0/24')  # changed IP to have a subnet of 10.0.2.0/24 r5-eth0
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    r4 = net.addHost('r4', cls=Node, ip='192.168.1.1')  # changed IP to have an IP of 192.168.1.1 r4-eth0
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    r3 = net.addHost('r3', cls=Node, ip='10.0.1.0/24')  # changed IP to have a subnet of 10.0.1.0/24 r3-eth0
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    # h1 and h2 has submnet 10.0.1.0/24 to match r3. (h1 = 10.0.1.1)(h2 = 10.0.1.2)
    h1 = net.addHost('h1', cls=Host, ip='10.0.1.1', defaultRoute='via 10.0.1.0')  # added default route for h1 and h2 to forward to r3
    h2 = net.addHost('h2', cls=Host, ip='10.0.1.2', defaultRoute='via 10.0.1.0')
    # h3 and h3 has submnet 10.0.2.0/24 to match r5. (h1 = 10.0.2.1)(h2 = 10.0.2.2)
    h3 = net.addHost('h3', cls=Host, ip='10.0.2.1', defaultRoute='via 10.0.2.0')  # added default route for h3 and h4 to forward to r5
    h4 = net.addHost('h4', cls=Host, ip='10.0.2.2', defaultRoute='via 10.0.2.0')

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)
    net.addLink(h3, s2)
    net.addLink(h4, s2)
    net.addLink(s2, r5)
    net.addLink(s1, r3)
    # added interfaces for r3-r4 using 192.168.1.0/30
    net.addLink(r3, r4,intfName1='r3-eth1',params1={'ip':'192.168.1.2/30'}, intfName2='r4-eth0', params2={'ip':'192.168.1.1/30'})
    # added interfaces for r4-r5 using 192.168.2.0/30
    net.addLink(r4, r5,intfName1='r4-eth1',params1={'ip':'192.168.2.1/30'}, intfName2='r5-eth1', params2={'ip':'192.168.2.2/30'})

    info( '*** Starting network\n')
    net.build()
    # save ip addresses and host names to ip_address.txt file
    save_ip_addresses(net)
    # run certificate_generation.py after saving ip address to use ip_address.py in appending to etc/hosts.
    subprocess.run(["sudo", "-E", "python3", "certificate_generation.py"])
    # ___________________________________________________
    # allow hosts to send packets to its outside networks
    net['h1'].cmd('ip route add 10.0.2.0/24 via 10.0.1.0')
    net['h2'].cmd('ip route add 10.0.2.0/24 via 10.0.1.0')
    net['h3'].cmd('ip route add 10.0.1.0/24 via 10.0.2.0')
    net['h4'].cmd('ip route add 10.0.1.0/24 via 10.0.2.0')

    # Forward anything related to outside networks via r4-eth1 from r5
    net['r5'].cmd('ip route add 10.0.1.0/24 via 192.168.2.1 dev r5-eth1')
    net['r5'].cmd('ip route add 192.168.1.0/30 via 192.168.2.1 dev r5-eth1')

    # Forward anything related to r3 network via r3-eth1 from r4
    # Forward anything related to r5 network via r5-eth1 from r4
    net['r4'].cmd('ip route add 10.0.1.0/24 via 192.168.1.2 dev r4-eth0')
    net['r4'].cmd('ip route add 10.0.2.0/24 via 192.168.2.2 dev r4-eth1')

    # Forward anything related to outside networks via r4-eth0 from r3
    net['r3'].cmd('ip route add 10.0.2.0/24 via 192.168.1.1 dev r3-eth1') 
    net['r3'].cmd('ip route add 192.168.2.0/30 via 192.168.1.1 dev r3-eth1')
    # ___________________________________________________
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')
    # *** chat_server.py file needs to be renamed ***
    # start xterm and run chat_server.py file
    
    makeTerm(h4, title='Node: ', term='xterm', display=None, cmd='python3 tpa4_chat_server.py; bash')
    time.sleep(5)
    makeTerm(h1, title='Node: ', term='xterm', display=None, cmd='python3 tpa4_chat_client.py; bash')
    makeTerm(h2, title='Node: ', term='xterm', display=None, cmd='python3 tpa4_chat_client.py; bash')
    makeTerm(h3, title='Node: ', term='xterm', display=None, cmd='python3 tpa4_chat_client.py; bash')

    CLI(net)
    net.stop()
    net.stopXterms()    # close xterm on exit

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()