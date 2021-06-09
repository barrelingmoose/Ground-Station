#!/bin/bash
###############################################################################################
# Filename:    startGroundStation.sh
# Description: Executable shell script used to run the desired configuration of COSMOS while
#              simultaneously executing the Flight Computers command script and handling the
#              associated collected data.
# Author:      Chandler Kramer
###############################################################################################
# INSTANTIATE VARIABLES

echo "Running startGroundStation.sh"
# username to flight computer
username=pi
# ip address to flight computer
ip_address=10.1.92.89
# command to run the flight computers main script
run_fc_script='python3 COSMOS/main.py'
# password to flight computer for sshpass
fc_pass=Mas2.0
# directory where data is stored on flight computer
get_data='/home/pi/COSMOS/IMU_output.csv'
sleep 1
echo "Variables have been established"

time_stamp=$(date +"%m-%d-%Y-%H.%M")
###############################################################################################
# START COSMOS

echo "Preparing COSMOS"
sleep 1
# Navigate to the COSMOS Launcher executable file
cd ~/Ground-Station/COSMOS/COSMOS-Config/RaspberryPi/tools
# Execute CmdTlmServer tool
./CmdTlmServer &
# Simultaneously execute and start TlmGrapher tool with the specified configuration file
ruby TlmGrapher -c "tlm_grapher_config.txt" -s &
echo "COSMOS Prepared and Running" &
# Short delay to allow the server to initialize
sleep 5

###############################################################################################
# FLIGHT COMPUTER COMMANDS AND DATA HANDLING

echo "Preparing Flight Computer"
# Log into FC and execute the FC script
sshpass -p "$fc_pass" ssh -o StrictHostKeyChecking=no $username@$ip_address $run_fc_script &
pid=$!

spin[0]="-"
spin[1]="\\"
spin[2]="|"
spin[3]="/"
echo -n "[Running]... ${spin[0]}"
while [ -d /proc/$pid ]
do
  for i in "${spin[@]}"
  do
    echo -ne "\b$i"
    sleep 0.5
  done
done
# Navigate to desired data collection folder
cd ~/Ground-Station/COSMOS/COSMOS-Data
# SCP collected data into current directory
echo " "
echo "Collecting Data from Flight Computer"
sshpass -p "$fc_pass" scp $username@$ip_address:$get_data .
echo "Data Collected."
pwd
mv "IMU_output.csv" "log/IMU_output_${time_stamp}.csv"
###############################################################################################
