#!/bin/bash

# Define usage instructions
usage() {
  echo "Usage: $0 [-h|--help] <time interval in seconds>, run the script using nohup background: nohup ./perfmonitor.sh 60 &"
  echo ""
  echo "Capture performance metrics using ps, top, iostat, and iotop commands and write the output to a file."
  echo ""
  echo "Options:"
  echo "  -h, --help  Display this help message and exit."
  echo ""
  echo "Arguments:"
  echo "  <time interval in seconds>  The time interval in seconds between capturing performance metrics."
  echo ""
  echo "The default output file is /var/log/performance_metrics.txt, change it in the line contains output_file="
}

# Check if the help parameter is passed
if [ "$1" == "-h" ] || [ "$1" == "--help" ]
then
  usage
  exit 0
fi

# Check if an number argument is passed
if [ "$1" -gt 0 ] 2>/dev/null;then
  echo "Time interval:" "$1"
else
  echo "Error: No time interval specified."
  echo ""
  usage
  exit 1
fi

# Set the time interval
interval="$1"

# Define the output file name
output_file=/var/log/performance_metrics-"$(date "+%m%d%H%s")".txt

# Check if iotop is installed
if ! command -v iotop &> /dev/null
then
  echo "iotop is not installed. Installing it now..."
  if [ -f /etc/redhat-release ]; then
          echo "Detected Red Hat based distribution"
          sudo yum install iotop -y
  elif [ -f /etc/lsb-release ]; then
          apt-get install iotop -y
  elif [ -f /etc/os-release ]; then
          . /etc/os-release
          if [[ "$ID" == "opensuse" || "$ID" == "sles" ]]; then
            echo "Detected SUSE-based distribution."
            zypper --non-interactive install iotop
          fi
  else
      echo "Unsupported distribution,install iotop manually"
  fi
fi

# Capture performance metrics every $interval seconds and write to the output file
while true
do
  # Print the system time
  echo "System time: $(date)" >> $output_file

  echo "Running tasks:" >> $output_file
  ps -eo stat,pid,user,%cpu,%mem,time,cmd | grep -e '^[R|D]' >> $output_file
  echo "" >> $output_file

  # Capture CPU and memory usage using 'ps' command
  echo "Top CPU usage:" >> $output_file
  top -b -n 1 -o +%CPU | grep -A 20 average >> $output_file
  echo "" >> $output_file

  echo "Top MEM usage:" >> $output_file
  top -b -n 1 -o +%MEM | grep -A 20 average >> $output_file
  echo "" >> $output_file

  # Capture I/O statistics using 'iostat' command
  echo "I/O statistics:" >> $output_file
  iostat -dxctm >> $output_file

  # Capture I/O usage by process using 'iotop' command
  echo "I/O usage by process:" >> $output_file
  iotop -t -o -b -n 1 >> $output_file

  # Wait for $interval seconds before capturing the next set of performance metrics
  sleep $interval
done
