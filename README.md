# Routing Project

This repository contains the implementation of various networking tasks and experiments. Below is the file structure and the purpose of each file:

## How to run Q1:

1. Grant execute permissions to the shell script:
   ```bash
   chmod +x q1.sh
   ```
2. Run the script:
   ```bash
   ./q1.sh
   ```

### Files:
- **with_stp.py**: Implements a custom Mininet topology using Linux bridges with STP (Spanning Tree Protocol) enabled. It performs packet capture and delay analysis for multiple host pairs.
- **without_stp.py**: Sets up a Mininet topology using Open vSwitch (OVS) switches without STP support. It performs packet capture and ping-based delay measurement.
- **delay_analysis_1.txt, delay_analysis_2.txt, delay_analysis_3.txt**: Log files containing delay analysis results for different host pairs in the STP-enabled network.
- **ping_test_1.txt, ping_test_2.txt, ping_test_3.txt**: Log files containing ping and delay results for the corresponding host pairs in the non-STP network.

You can download the captured pcap files from this link:
[Captured pcap files (Google Drive)](https://drive.google.com/file/d/1ySjvAK3SLHPq0q745BNKnq5yI43pVY08/view?usp=sharing)

Inside that zip file:
- **captures_with_stp/**: Contains .pcap files generated during packet capture from the STP-enabled network.
- **captures_no_stp/**: Contains .pcap files generated during packet capture from the network without STP.

---

## How to run Q2:

1. Run the following command to start the custom Mininet topology with STP enabled:
   ```bash
   sudo python3 q2.py
   ```

### Files:
- **q2.py**: Sets up a custom Mininet topology with Linux bridge switches and STP enabled. Implements NAT using a dedicated host (h9) for communication between private and public networks. Includes ping tests and iperf3 traffic analysis to verify connectivity and performance.
- **bridge.py**: Implements a bidirectional bridge approach.
- **iperf_results.log**: Contains results of the iperf3 traffic analysis.
- **ping_results.log**: Contains results of the ping-based tests for connectivity.

---

## How to run Q3:

1. Compile the C files using the following command:
   ```bash
   cc distance_vector.c node0.c node1.c node2.c node3.c
   ```
2. Run the compiled program:
   ```bash
   ./q3.out
   ```

### Files:
- **distance_vector.c, node0.c, node1.c, node2.c, node3.c**: Implements the Distance Vector Routing algorithm for a network of 4 nodes.
- **o1.log, o2.log, o3.log**: Log files containing logs generated during the execution of the Distance Vector Routing algorithm.
