from mininet.topo import Topo
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.node import CPULimitedHost
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class NATTopo(Topo):
    def build(self):
        # Add switch
        s1 = self.addSwitch('s1')

        # Add hosts h1, h2, h3, h5, h6, h8, h9
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3', ip='10.0.0.4/24')
        h5 = self.addHost('h5', ip='10.0.0.6/24')
        h6 = self.addHost('h6', ip='10.0.0.7/24')
        h8 = self.addHost('h8', ip='10.0.0.9/24')
        h9 = self.addHost('h9')  # NAT host

        # Internal links to h9
        self.addLink(h1, h9, cls=TCLink, delay='5ms')
        self.addLink(h2, h9, cls=TCLink, delay='5ms')

        # h9 to s1 (public)
        self.addLink(h9, s1, cls=TCLink, delay='5ms')

        # External hosts to s1
        self.addLink(h3, s1)
        self.addLink(h5, s1)
        self.addLink(h6, s1)
        self.addLink(h8, s1)

def run():
    topo = NATTopo()
    net = Mininet(topo=topo, link=TCLink, host=CPULimitedHost)
    net.start()

    h1, h2, h3, h5, h6, h8, h9 = net.get('h1', 'h2', 'h3', 'h5', 'h6', 'h8', 'h9')

    info('*** Assigning IP addresses\n')

    # Assign IPs to h1 and h2 (internal)
    h1.setIP('10.1.1.2/24', intf='h1-eth0')
    h2.setIP('10.1.1.3/24', intf='h2-eth0')

    # Assign IPs to h9 interfaces
    h9.cmd('ifconfig h9-eth0 172.16.10.10/24')  # public
    h9.cmd('ifconfig h9-eth1 10.1.1.1/24')      # internal

    # Set default gateway for h1 and h2
    h1.cmd('ip route add default via 10.1.1.1')
    h2.cmd('ip route add default via 10.1.1.1')

    info('*** Enabling NAT on h9\n')

    h9.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Set up NAT (MASQUERADE)
    h9.cmd('iptables -t nat -A POSTROUTING -o h9-eth0 -j MASQUERADE')
    h9.cmd('iptables -A FORWARD -i h9-eth0 -o h9-eth1 -m state --state RELATED,ESTABLISHED -j ACCEPT')
    h9.cmd('iptables -A FORWARD -i h9-eth1 -o h9-eth0 -j ACCEPT')

    info('*** Optional: port forwarding for incoming access (e.g., iperf)\n')
    h9.cmd('iptables -t nat -A PREROUTING -i h9-eth0 -p tcp --dport 5001 -j DNAT --to-destination 10.1.1.2:5001')
    h9.cmd('iptables -t nat -A PREROUTING -i h9-eth0 -p tcp --dport 5002 -j DNAT --to-destination 10.1.1.3:5002')

    info('*** Network setup complete. Launching CLI...\n')
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()
