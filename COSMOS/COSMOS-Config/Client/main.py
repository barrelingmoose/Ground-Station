################################################################################
# Filename:    main.py
# Description: Operates Raspberry Pi Flight Computer
# Authors:     Chandler Kramer
#              Thomas Bennett
################################################################################

################################################################################
# Imports
################################################################################
from vnpy import *
from IMU_Functions import *
import time
import csv
import socket
import struct

################################################################################
# Establishing Global Variables
################################################################################

# Serial Port and Server related variables
SERVER = '10.1.93.72'
PORT = 6787
HEADER = 64
FORMAT = 'utf-8'
ADDR = (SERVER, PORT)
USB_PORT = '/dev/ttyUSB0'

# Time of Flight in Seconds
TOF = 30

# Initializes the start/reference time
start = time.time()

# Initializes the stop time
stop = time.time()

# Initializes the counter to be compared to TOF
difference = stop - start

# Setting Packet IDs
first_packet = 3
last_packet = 22
PACKET_ID = [packet for packet in range(first_packet,last_packet)]

################################################################################
# Establishing Sensor Connections
################################################################################

# Instatiates VnSensor Class Object
sensor = VnSensor()

# Connects Class Object to appropriate COM Port
sensor.connect(USB_PORT, 115200)

# Filename for data collection
csvoutput = 'IMU_output.csv'

# Socket Connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Instatiates IMU_Functions Class Object
functions = IMU_Functions()

# Create Desired Fields for CSV file
fields = ["Yaw", "Pitch", "Roll", "X Accel", "Y Accel", "Z Accel", "X Rate",
              "Y Rate", "Z Rate", "Magnetic X", "Magnetic Y", "Magnetic Z",
              "Gravity X", "Gravity Y", "Gravity Z", "Q1", "Q2", "Q3", "Q4"]

#################################################################################
# Main Loop
#################################################################################
functions.write2csv(csvoutput, fields, TOF, sensor, start,stop, PACKET_ID, client)

sensor.disconnect()
########################################################################################
# End of File
########################################################################################
