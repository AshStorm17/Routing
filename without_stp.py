#!/usr/bin/env python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
import time
import os

class LoopTopo(Topo):
    def build(self):
        # Default switches (no STP)
        s1 = self.addSwitch('s1')  # OVSKernelSwitch by default
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

        # Switch Links (7ms delay) - loop present!
        self.addLink(s1, s2, cls=TCLink, delay='7ms')
        self.addLink(s2, s3, cls=TCLink, delay='7ms')
        self.addLink(s3, s4, cls=TCLink, delay='7ms')
        self.addLink(s4, s1, cls=TCLink, delay='7ms')
        self.addLink(s1, s3, cls=TCLink, delay='7ms')  # Diagonal link (creates loop)

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
    for idx, (src, dst) in enumerate(tests, 1):
        print(f"\nTesting {src} -> {dst}:")
        logfile = f"ping_test_{idx}.log"
        with open(logfile, 'w') as f:
            for i in range(3):
                print(f"Attempt {i+1}:")
                result = net[src].cmd(f'ping -c 3 {net[dst].IP()}')
                f.write(result + "\n\n")
                print(result)

                if 'rtt min/avg/max/mdev' in result:
                    stats_line = [line for line in result.split('\n') if 'rtt min/avg/max/mdev' in line][0]
                    times = stats_line.split('=')[1].split('/')
                    avg_time = times[1]
                    print(f"Average delay: {avg_time} ms")
                    f.write(f"Average delay: {avg_time} ms\n")
                elif '100% packet loss' in result:
                    print("Ping failed (100% packet loss)")
                    f.write("Ping failed (100% packet loss)\n")
                else:
                    print("Ping results inconclusive")
                    f.write("Ping results inconclusive\n")

                if i < 2:
                    print("Waiting 30 seconds...")
                    time.sleep(30)

def start_capture(net, capture_dir='captures_no_stp'):
    print("\n=== Starting Packet Capture on All Switches ===")
    for sw in net.switches:
        for intf in sw.intfList():
            if intf.name != 'lo':
                filename = f"{capture_dir}/{sw.name}_{intf.name}.pcap"
                sw.cmd(f'tcpdump -i {intf.name} -w {filename} &')

def stop_capture():
    print("\n=== Stopping Packet Capture ===")
    for sw in net.switches:
        sw.cmd('kill %tcpdump')

if __name__ == '__main__':
    setLogLevel('info')

    topo = LoopTopo()
    net = Mininet(topo=topo, link=TCLink, autoSetMacs=True)

    print("Starting network...")
    net.start()

    print("Starting packet capture...")
    start_capture(net)

    print("Waiting 30 seconds before running tests...")
    time.sleep(30)

    run_tests(net)

    print("Stopping packet capture...")
    stop_capture()

    net.stop()
