from time import sleep
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.log import setLogLevel, info
from mininet.node import Host, Switch
from mininet.util import dumpNodeConnections

class LinuxBridge(Switch):
    """Custom switch using Linux bridge with STP enabled"""
    def start(self, controllers):
        self.cmd('brctl addbr', self)
        self.cmd('brctl stp', self, 'on')
        self.cmd('brctl setbridgeprio', self, '32768')
        for intf in self.intfList():
            if intf.name != 'lo':
                self.cmd('brctl addif', self, intf)
        self.cmd('ifconfig', self, 'up')

    def stop(self):
        self.cmd('ifconfig', self, 'down')
        self.cmd('brctl delbr', self)

class NATTopo(Topo):
    def build(self):
        # Add switch
        s1 = self.addSwitch('s1', cls=LinuxBridge)
        s2 = self.addSwitch('s2', cls=LinuxBridge)
        s3 = self.addSwitch('s3', cls=LinuxBridge)
        s4 = self.addSwitch('s4', cls=LinuxBridge)

        # Hosts h1 and h2 behind NAT
        h1 = self.addHost('h1', ip='10.1.1.2/24', defaultRoute='via 10.1.1.1')
        h2 = self.addHost('h2', ip='10.1.1.3/24', defaultRoute='via 10.1.1.1')

        # Other hosts
        h3 = self.addHost('h3', ip='10.0.0.4/24')
        h4 = self.addHost('h4', ip='10.0.0.5/24')
        h5 = self.addHost('h5', ip='10.0.0.6/24')
        h6 = self.addHost('h6', ip='10.0.0.7/24')
        h7 = self.addHost('h7', ip='10.0.0.8/24')
        h8 = self.addHost('h8', ip='10.0.0.9/24')

        # NAT host with public IP
        h9 = self.addHost('h9')

        # Switch interconnections
        self.addLink(s1, s2, cls=TCLink, delay='7ms')
        self.addLink(s2, s3, cls=TCLink, delay='7ms')
        self.addLink(s3, s4, cls=TCLink, delay='7ms')
        self.addLink(s4, s1, cls=TCLink, delay='7ms')
        self.addLink(s1, s3, cls=TCLink, delay='7ms')

        # h9 connected to s1 (public side)
        self.addLink(h9, s1, cls=TCLink, delay='5ms')

        # Private links: h1 and h2 to h9 (internal side)
        self.addLink(h1, h9, cls=TCLink, delay='5ms')
        self.addLink(h2, h9, cls=TCLink, delay='5ms')

        # Other hosts
        self.addLink(h3, s2, cls=TCLink, delay='5ms')
        self.addLink(h4, s2, cls=TCLink, delay='5ms')
        self.addLink(h5, s3, cls=TCLink, delay='5ms')
        self.addLink(h6, s3, cls=TCLink, delay='5ms')
        self.addLink(h7, s4, cls=TCLink, delay='5ms')
        self.addLink(h8, s4, cls=TCLink, delay='5ms')

def ping_server():
    h1 = net.get('h1')
    h2 = net.get('h2')
    h8 = net.get('h8')
    h6 = net.get('h6')
    info('*** Pinging tests\n')
    info(h1.cmd('ping -c 3 10.0.0.6'))  # h5
    info(h2.cmd('ping -c 3 10.0.0.4'))  # h3
    info(h8.cmd('ping -c 3 10.1.1.2'))  # h1
    info(h6.cmd('ping -c 3 10.1.1.3'))  # h2

def iperf_test():
    h1 = net.get('h1')
    h2 = net.get('h2')
    h3 = net.get('h3')
    h8 = net.get('h8')
    h6 = net.get('h6')

    info('*** Starting iperf3 servers and clients\n')

    h1.cmd('iperf3 -s -p 5001 > /tmp/h1_iperf.txt &')
    sleep(2)
    result1 = h6.cmd('iperf3 -c 10.1.1.2 -p 5001 -t 5')
    info("*** h6 -> h1 iperf result:\n", result1)

    h8.cmd('iperf3 -s -p 5003 > /tmp/h8_iperf.txt &')
    sleep(2)
    result2 = h2.cmd('iperf3 -c 10.0.0.9 -p 5003 -t 5')
    info("*** h2 -> h8 iperf result:\n", result2)

    h2.cmd('iperf3 -s -p 5004 > /tmp/h2_iperf.txt &')
    sleep(2)
    result3 = h3.cmd('iperf3 -c 10.1.1.3 -p 5004 -t 5')
    info("*** h3 -> h2 iperf result:\n", result3)

def verify_stp(net):
    print("\n=== STP Status ===")
    for switch in net.switches:
        print(f"\nSTP info for {switch.name}:")
        print(switch.cmd('brctl showstp', switch))

if __name__ == '__main__':
    setLogLevel('info')
    topo = NATTopo()
    net = Mininet(topo=topo, host=CPULimitedHost, link=TCLink)
    net.start()

    h9 = net.get('h9')

    info('*** Configuring NAT bridge on h9\n')
    h9.cmd('brctl addbr br0')
    h9.cmd('brctl addif br0 h9-eth1')
    h9.cmd('brctl addif br0 h9-eth2')
    h9.cmd('ip addr add 10.1.1.1/24 dev br0')
    h9.cmd('ip link set dev br0 up')

    info('*** Assigning public IP to h9-eth0\n')
    h9.cmd('ip addr add 172.16.10.10/24 dev h9-eth0')
    h9.cmd('ip link set dev h9-eth0 up')

    info('*** Enabling NAT\n')
    h9.cmd('sysctl -w net.ipv4.ip_forward=1')
    h9.cmd('iptables -t nat -A POSTROUTING -o h9-eth0 -j MASQUERADE')
    h9.cmd('iptables -A FORWARD -i h9-eth0 -o br0 -m state --state RELATED,ESTABLISHED -j ACCEPT')
    h9.cmd('iptables -A FORWARD -i br0 -o h9-eth0 -j ACCEPT')

    sleep(5)
    print("Waiting 60 seconds for STP convergence...")
    sleep(60)

    verify_stp(net)

    ping_server()
    iperf_test()

    net.stop()
