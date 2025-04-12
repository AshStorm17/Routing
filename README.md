# Routing Project

This repository contains the implementation of various networking tasks and experiments. Below is the file structure and the purpose of each file:

## File Structure
[`delay_analysis_1.txt`](delay_analysis_1.txt )
[`delay_analysis_2.txt`](delay_analysis_2.txt ) 
[`delay_analysis_3.txt`](delay_analysis_3.txt ) <br>
[`distance_vector.c`](distance_vector.c )
[`node0.c`](node0.c )
[`node1.c`](node1.c )
[`node2.c`](node2.c )
[`node3.c`](node3.c ) <br>
[`o1.log`](o1.log )
[`o2.log`](o2.log )
[`o3.log`](o3.log ) <br>
[`q1.py`](q1.py )
[`q2.py`](q2.py )
[`q3.out`](q3.out ) <br>
[`README.md`](README.md ) <hr>
captures/ <br>
    [`captures/s1_s1-eth1.pcap`](captures/s1_s1-eth1.pcap )
    [`captures/s1_s1-eth2.pcap`](captures/s1_s1-eth2.pcap )
    [`captures/s1_s1-eth3.pcap`](captures/s1_s1-eth3.pcap )
    [`captures/s1_s1-eth4.pcap`](captures/s1_s1-eth4.pcap )
    [`captures/s1_s1-eth5.pcap`](captures/s1_s1-eth5.pcap )
    [`captures/s2_s2-eth1.pcap`](captures/s2_s2-eth1.pcap )
    [`captures/s2_s2-eth2.pcap`](captures/s2_s2-eth2.pcap )
    [`captures/s2_s2-eth3.pcap`](captures/s2_s2-eth3.pcap )
    [`captures/s2_s2-eth4.pcap`](captures/s2_s2-eth4.pcap )
    [`captures/s3_s3-eth1.pcap`](captures/s3_s3-eth1.pcap )
    [`captures/s3_s3-eth2.pcap`](captures/s3_s3-eth2.pcap )
    [`captures/s3_s3-eth3.pcap`](captures/s3_s3-eth3.pcap )
    [`captures/s3_s3-eth4.pcap`](captures/s3_s3-eth4.pcap )
    [`captures/s3_s3-eth5.pcap`](captures/s3_s3-eth5.pcap )
    [`captures/s4_s4-eth1.pcap`](captures/s4_s4-eth1.pcap )
    [`captures/s4_s4-eth2.pcap`](captures/s4_s4-eth2.pcap )
    [`captures/s4_s4-eth3.pcap`](captures/s4_s4-eth3.pcap )
    [`captures/s4_s4-eth4.pcap`](captures/s4_s4-eth4.pcap )


## Purpose of Files

### Q1
- **`q1.py`**: Implements a custom Mininet topology with STP (Spanning Tree Protocol) enabled. It also performs delay analysis and packet capture.
- **Packet Captures (`captures/`)**: Contains `.pcap` files generated during the packet capture process.
- **Delay Analysis (`delay_analysis_1.txt`, `delay_analysis_2.txt`, `delay_analysis_3.txt`)**: Logs the results of delay analysis for different host pairs.

### Q2
- **`q2.py`**: Implements a NAT (Network Address Translation) topology using Mininet. It sets up internal and external hosts and configures NAT rules.

### Q3
- **C Files (`distance_vector.c`, `node0.c`, `node1.c`, `node2.c`, `node3.c`)**: Implements the Distance Vector Routing algorithm for a network of 4 nodes.
- **Log Files (`o1.log`, `o2.log`, `o3.log`)**: Contains logs generated during the execution.