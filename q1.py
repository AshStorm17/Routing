#!/usr/bin/env python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink
from mininet.node import RemoteController, OVSSwitch
import time

class LoopTopo(Topo):
    def build(self):
        # Create switches (Open vSwitch)
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')

        # Create hosts with specified IPs
        h1 = self.addHost('h1', ip='10.0.0.2/24')
        h2 = self.addHost('h2', ip='10.0.0.3/24')
        h3 = self.addHost('h3', ip='10.0.0.4/24')
        h4 = self.addHost('h4', ip='10.0.0.5/24')
        h5 = self.addHost('h5', ip='10.0.0.6/24')
        h6 = self.addHost('h6', ip='10.0.0.7/24')
        h7 = self.addHost('h7', ip='10.0.0.8/24')
        h8 = self.addHost('h8', ip='10.0.0.9/24')

        # Inter-switch links with 7ms delay
        self.addLink(s1, s2, cls=TCLink, delay='7ms')
        self.addLink(s2, s3, cls=TCLink, delay='7ms')
        self.addLink(s3, s4, cls=TCLink, delay='7ms')
        self.addLink(s4, s1, cls=TCLink, delay='7ms')
        self.addLink(s1, s3, cls=TCLink, delay='7ms')  # Looping link

        # Add host links with 5ms delay
        self.addLink('h1', 's1', cls=TCLink, delay='5ms')
        self.addLink('h2', 's1', cls=TCLink, delay='5ms')
        self.addLink('h3', 's2', cls=TCLink, delay='5ms')
        self.addLink('h4', 's2', cls=TCLink, delay='5ms')
        self.addLink('h5', 's3', cls=TCLink, delay='5ms')
        self.addLink('h6', 's3', cls=TCLink, delay='5ms')
        self.addLink('h7', 's4', cls=TCLink, delay='5ms')
        self.addLink('h8', 's4', cls=TCLink, delay='5ms')

def run_tests(net):
    print("\n=== Running Tests ===")
    tests = [('h3', 'h1'), ('h5', 'h7'), ('h8', 'h2')]
    for src, dst in tests:
        print(f"\nTesting {src} -> {dst}:")
        for i in range(3):
            print(f"Attempt {i+1}:")
            result = net[src].cmd(f'ping -c 3 {net[dst].IP()}')
            print(result)
            if '0% packet loss' in result:
                time_pos = result.find('min/avg/max')
                if time_pos != -1:
                    times = result[time_pos:].split()[3].split('/')
                    print(f"Average delay: {times[1]} ms")
            if i < 2:
                print("Waiting 60 seconds...")
                time.sleep(60)

def main():
    setLogLevel('info')

    info("*** Creating network\n")
    c0 = RemoteController('c0', ip='127.0.0.1', port=6633)

    net = Mininet(topo=LoopTopo(),
                  link=TCLink,
                  controller=c0,
                  switch=OVSSwitch,
                  autoSetMacs=True)

    info("*** Starting network\n")
    net.start()

    # Wait a bit for controller to learn topology
    info("*** Waiting 30 seconds for controller/STP\n")
    time.sleep(30)

    run_tests(net)

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    main()
