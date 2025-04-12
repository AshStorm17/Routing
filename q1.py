#!/usr/bin/env python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import Host, Switch
import time

class LinuxBridge(Switch):
    """Custom switch using Linux bridge with STP enabled"""
    def start(self, controllers):
        self.cmd('brctl addbr', self)
        # Enable STP with priority set (lower priority means more likely to be root)
        self.cmd('brctl stp', self, 'on')
        self.cmd('brctl setbridgeprio', self, '32768')  # Default priority
        for intf in self.intfList():
            if intf.name != 'lo':
                self.cmd('brctl addif', self, intf)
        self.cmd('ifconfig', self, 'up')

    def stop(self):
        self.cmd('ifconfig', self, 'down')
        self.cmd('brctl delbr', self)

class LoopTopo(Topo):
    def build(self):
        # Create switches using our LinuxBridge
        s1 = self.addSwitch('s1', cls=LinuxBridge)
        s2 = self.addSwitch('s2', cls=LinuxBridge)
        s3 = self.addSwitch('s3', cls=LinuxBridge)
        s4 = self.addSwitch('s4', cls=LinuxBridge)

        # Create hosts with correct IPs
        hosts = []
        for i in range(1,9):
            hosts.append(self.addHost(f'h{i}', ip=f'10.0.0.{i+1}/24'))

        # Add switch links with 7ms delay
        self.addLink('s1', 's2', cls=TCLink, delay='7ms')
        self.addLink('s2', 's3', cls=TCLink, delay='7ms')
        self.addLink('s3', 's4', cls=TCLink, delay='7ms')
        self.addLink('s4', 's1', cls=TCLink, delay='7ms')
        self.addLink('s1', 's3', cls=TCLink, delay='7ms')
        
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
            # Capture ping output to analyze results
            result = net[src].cmd(f'ping -c 3 {net[dst].IP()}')
            print(result)
            
            # Improved ping result parsing
            if 'rtt min/avg/max/mdev' in result:
                # Extract the statistics line
                stats_line = [line for line in result.split('\n') 
                            if 'rtt min/avg/max/mdev' in line][0]
                # Extract the times
                times = stats_line.split('=')[1].split('/')
                avg_time = times[1]
                print(f"Average delay: {avg_time} ms")
            elif '100% packet loss' in result:
                print("Ping failed (100% packet loss)")
            else:
                print("Ping results inconclusive")
                
            if i < 2:
                print("Waiting 60 seconds...")
                time.sleep(60)

def verify_stp(net):
    print("\n=== STP Status ===")
    for switch in net.switches:
        print(f"\nSTP info for {switch.name}:")
        print(switch.cmd('brctl showstp', switch))

if __name__ == '__main__':
    setLogLevel('info')
    
    # Create network with our custom switch
    net = Mininet(topo=LoopTopo(), link=TCLink, autoSetMacs=True)
    
    print("Starting network...")
    net.start()
    
    print("Waiting 60 seconds for STP convergence...")
    time.sleep(60)
    
    # Verify STP status before running tests
    verify_stp(net)
    
    run_tests(net)
    
    CLI(net)

    net.stop()