#!/bin/bash

echo "======== Cleaning up Mininet ========"
sudo mn -c

echo "======== Running without STP ========"

# Clean and prepare captures folder for no STP
sudo rm -rf captures_no_stp
mkdir captures_no_stp

# Run without STP
sudo python3 without_stp.py

echo "======== Waiting before running with STP ========"
sleep 10

echo "======== Running with STP ========"

# Clean and prepare captures folder for with STP
sudo rm -rf captures_with_stp
mkdir captures_with_stp

# Run with STP
sudo python3 with_stp.py

echo "======== DONE ========"
