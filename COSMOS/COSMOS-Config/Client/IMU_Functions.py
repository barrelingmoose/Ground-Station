import struct
from vnpy import *
from IMU_Functions import *
import time
import csv
import socket
import struct


class IMU_Functions:
    def __init__(self):
        pass

    def data_set(self, from_array, to_array):
        for element in from_array:
            to_array.append(str(element))
        return to_array 

    def send_data(self,lst,index,ID,destination):
        size = struct.calcsize(">Llf")
        temp = lst[index]
        data = struct.pack(">Llf",size,ID[index],float(temp))
        destination.send(data)

    def write2csv(self, csvoutput, fields, TOF, sensor,start,stop, PACKET_ID, client):
        with open(csvoutput, 'w') as IMU_data:
            # Establishing headers for the collected data
            # Writing the headers to the file
            IMU_writer = csv.writer(IMU_data)
            IMU_writer.writerow(fields)
            difference = stop-start
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
                self.data_set(ypr, rows)
                self.data_set(accel, rows)
                self.data_set(gyro, rows)
                self.data_set(mag, rows)
                self.data_set(grav, rows)
                self.data_set(quaternions, rows)
                # Writing list to csv file
                IMU_writer.writerow(rows)
                yaw = self.send_data(rows, 0, PACKET_ID,client)
                pitch = self.send_data(rows, 1, PACKET_ID, client)
                roll = self.send_data(rows, 2, PACKET_ID, client)
                x_accel = self.send_data(rows, 3, PACKET_ID, client)
                y_accel = self.send_data(rows, 4, PACKET_ID, client)
                z_accel = self.send_data(rows, 5, PACKET_ID, client)
                x_rate = self.send_data(rows, 6, PACKET_ID, client)
                y_rate = self.send_data(rows, 7, PACKET_ID, client)
                z_rate = self.send_data(rows, 8, PACKET_ID, client)
                x_mag = self.send_data(rows, 9, PACKET_ID, client)
                y_mag = self.send_data(rows, 10, PACKET_ID, client)
                z_mag = self.send_data(rows, 11, PACKET_ID, client)
                x_grav = self.send_data(rows, 12, PACKET_ID, client)
                y_grav = self.send_data(rows, 13, PACKET_ID, client)
                z_grav = self.send_data(rows, 14, PACKET_ID, client)
                Q1 = self.send_data(rows, 15, PACKET_ID, client)
                Q2 = self.send_data(rows, 16, PACKET_ID, client)
                Q3 = self.send_data(rows, 17, PACKET_ID, client)
                Q4 = self.send_data(rows, 18, PACKET_ID, client)