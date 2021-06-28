from vnpy import *
from IMU_Functions import *
import time
import csv
import socket
import struct

SERVER = '10.1.93.3'
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
first_packet = 3
last_packet = 22
PACKET_ID = [packet for packet in range(first_packet,last_packet)]
# Instatiates VnSensor Class Object
sensor = VnSensor()
# Connects Class Object to appropriate COM Port
sensor.connect(USB_PORT, 115200)

# Filename for data collection
csvoutput = 'IMU_output.csv'

# Socket Connection
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

functions = IMU_Functions()


with open(csvoutput, 'w') as IMU_data:
    # Establishing headers for the collected data
    fields = ["Yaw", "Pitch", "Roll", "X Accel", "Y Accel", "Z Accel", "X Rate",
              "Y Rate", "Z Rate", "Magnetic X", "Magnetic Y", "Magnetic Z",
              "Gravity X", "Gravity Y", "Gravity Z", "Q1", "Q2", "Q3", "Q4"]
    # Writing the headers to the file
    IMU_writer = csv.writer(IMU_data)
    IMU_writer.writerow(fields)
    while difference < TOF:
        # Update stop time for every iteration
        stop = time.time()
        # Update the difference every iteration
        difference = stop - start
        # Collection of data during the TOF
        # Initializing data registers
        outputs = sensor.read_yaw_pitch_roll_magnetic_acceleration_and_angular_rates()
        inputs = sensor.read_magnetic_and_gravity_reference_vectors()
        quaternion_read = sensor.read_quaternion_magnetic_acceleration_and_angular_rates()
        # List holding the information from data collection
        ypr = outputs.yaw_pitch_roll
        accel = outputs.accel
        gyro = outputs.gyro
        mag = inputs.mag_ref
        grav = inputs.acc_ref
        quaternions = quaternion_read.quat
        rows = []
        functions.data_set(ypr, rows)
        functions.data_set(accel, rows)
        functions.data_set(gyro, rows)
        functions.data_set(mag, rows)
        functions.data_set(grav, rows)
        functions.data_set(quaternions, rows)
        # Writing list to csv file
        IMU_writer.writerow(rows)
        yaw = functions.send_data(rows, 0, PACKET_ID,client)
        pitch = functions.send_data(rows, 1, PACKET_ID, client)
        roll = functions.send_data(rows, 2, PACKET_ID, client)
        x_accel = functions.send_data(rows, 3, PACKET_ID, client)
        y_accel = functions.send_data(rows, 4, PACKET_ID, client)
        z_accel = functions.send_data(rows, 5, PACKET_ID, client)
        x_rate = functions.send_data(rows, 6, PACKET_ID, client)
        y_rate = functions.send_data(rows, 7, PACKET_ID, client)
        z_rate = functions.send_data(rows, 8, PACKET_ID, client)
        x_mag = functions.send_data(rows, 9, PACKET_ID, client)
        y_mag = functions.send_data(rows, 10, PACKET_ID, client)
        z_mag = functions.send_data(rows, 11, PACKET_ID, client)
        x_grav = functions.send_data(rows, 12, PACKET_ID, client)
        y_grav = functions.send_data(rows, 13, PACKET_ID, client)
        z_grav = functions.send_data(rows, 14, PACKET_ID, client)
        Q1 = functions.send_data(rows, 15, PACKET_ID, client)
        Q2 = functions.send_data(rows, 16, PACKET_ID, client)
        Q3 = functions.send_data(rows, 17, PACKET_ID, client)
        Q4 = functions.send_data(rows, 18, PACKET_ID, client)
        #time.sleep(0.1)
sensor.disconnect()
