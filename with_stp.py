#!/usr/bin/env python
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink
from mininet.node import Host, Switch
import time
import os

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

class LoopTopo(Topo):
    def build(self):
        s1 = self.addSwitch('s1', cls=LinuxBridge)
        s2 = self.addSwitch('s2', cls=LinuxBridge)
        s3 = self.addSwitch('s3', cls=LinuxBridge)
        s4 = self.addSwitch('s4', cls=LinuxBridge)

        # Create hosts with specified IPs
        h1 = self.addHost('h1', ip='10.0.0.2/24')
        h2 = self.addHost('h2', ip='10.0.0.3/24')
        h3 = self.addHost('h3', ip='10.0.0.4/24')
        h4 = self.addHost('h4', ip='10.0.0.5/24')
        h5 = self.addHost('h5', ip='10.0.0.6/24')
        h6 = self.addHost('h6', ip='10.0.0.7/24')
        h7 = self.addHost('h7', ip='10.0.0.8/24')
        h8 = self.addHost('h8', ip='10.0.0.9/24')

        self.addLink('s1', 's2', cls=TCLink, delay='7ms')
        self.addLink('s2', 's3', cls=TCLink, delay='7ms')
        self.addLink('s3', 's4', cls=TCLink, delay='7ms')
        self.addLink('s4', 's1', cls=TCLink, delay='7ms')
        self.addLink('s1', 's3', cls=TCLink, delay='7ms')

        self.addLink('h1', 's1', cls=TCLink, delay='5ms')
        self.addLink('h2', 's1', cls=TCLink, delay='5ms')
        self.addLink('h3', 's2', cls=TCLink, delay='5ms')
        self.addLink('h4', 's2', cls=TCLink, delay='5ms')
        self.addLink('h5', 's3', cls=TCLink, delay='5ms')
        self.addLink('h6', 's3', cls=TCLink, delay='5ms')
        self.addLink('h7', 's4', cls=TCLink, delay='5ms')
        self.addLink('h8', 's4', cls=TCLink, delay='5ms')

def start_packet_capture(net, capture_dir='captures_with_stp'):
    print("\n=== Starting Packet Capture on All Switches ===")
    for sw in net.switches:
        for intf in sw.intfList():
            if intf.name != 'lo':
                filename = f"{capture_dir}/{sw.name}_{intf.name}.pcap"
                sw.cmd(f'tcpdump -i {intf.name} -w {filename} &')

def stop_packet_capture(net):
    print("\n=== Stopping Packet Capture ===")
    for sw in net.switches:
        sw.cmd('kill %tcpdump')

def run_tests(net):
    print("\n=== Running Tests ===")
    tests = [('h3', 'h1'), ('h5', 'h7'), ('h8', 'h2')]
    for idx, (src, dst) in enumerate(tests, 1):
        logfile = f"delay_analysis_{idx}.log"
        with open(logfile, 'w') as log:
            log.write(f"Testing {src} -> {dst}\n")
            for i in range(3):
                print(f"\n{src} -> {dst}, Attempt {i+1}:")
                result = net[src].cmd(f'ping -c 3 {net[dst].IP()}')
                print(result)
                log.write(f"\nAttempt {i+1} Output:\n{result}\n")

                if 'rtt min/avg/max/mdev' in result:
                    stats_line = [line for line in result.split('\n') if 'rtt min/avg/max/mdev' in line][0]
                    times = stats_line.split('=')[1].split('/')
                    avg_time = times[1]
                    print(f"Average delay: {avg_time} ms")
                    log.write(f"Average delay: {avg_time} ms\n")
                elif '100% packet loss' in result:
                    print("Ping failed (100% packet loss)")
                    log.write("Ping failed (100% packet loss)\n")
                else:
                    print("Ping results inconclusive")
                    log.write("Ping results inconclusive\n")

                if i < 2:
                    print("Waiting 30 seconds...")
                    time.sleep(30)

def verify_stp(net):
    print("\n=== STP Status ===")
    for switch in net.switches:
        print(f"\nSTP info for {switch.name}:")
        print(switch.cmd('brctl showstp', switch))

if __name__ == '__main__':
    setLogLevel('info')
    net = Mininet(topo=LoopTopo(), link=TCLink, autoSetMacs=True)

    print("Starting network...")
    net.start()

    print("Waiting 60 seconds for STP convergence...")
    time.sleep(60)

    verify_stp(net)
    start_packet_capture(net)

    run_tests(net)

    stop_packet_capture(net)
    net.stop()

    print("\nAnalysis complete. Delay logs saved to delay_analysis_1/2/3.txt and packet captures to ./captures/")
