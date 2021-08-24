from os import error
from serial import Serial
import struct
import crcmod
import gpiozero
from time import sleep
from serial.serialutil import EIGHTBITS, PARITY_NONE, STOPBITS_ONE

class MAI_400:
    # Initialization dunder method 
    def __init__(self):
        self.ser = Serial("/dev/serial0", 115200, bytesize=EIGHTBITS, parity=PARITY_NONE, stopbits=STOPBITS_ONE) 

    def create_packet(self,id,definition=0,data=b'',data_length=0):

        if len(id)>1:
            error("ID must be a single byte")

        header = bytes.fromhex("90EB")
        crc16_func = crcmod.predefined.mkCrcFun('modbus')
        if len(data) > 0 and data_length == 0:
            data_length = len(data)

        packet = bytearray(bytes.fromhex("000000000000"))
        packet[0:2] = header
        packet[2:4] = data_length.to_bytes(2,'little')
        packet[4:5] = id
        packet[5:6] = definition.to_bytes(1,'little')
        if data_length>0:
            packet.extend(data)

        packet.extend(crc16_func(packet[2:]).to_bytes(2,'little'))

        return packet

    def receive_packet(self,ser):
        #print("Waiting for sync")
        sync_received = False
        while not sync_received:
            while ser.inWaiting == 0:
                sleep(0.001)
            if ser.read() == b'\x90':
                if ser.read() == b'\xeb':
                    sync_received = True
        #print("Sync recieved!")

        size_bytes = ser.read(2)
        packet_size = int.from_bytes(size_bytes, byteorder='little', signed=False)

        #print("Reading packet, legnth = "+str(packet_size))

        recvd_packet = ser.read(packet_size+4) #+4 to include rest of header and CRC
        bytes_cat = b'\x90\xeb' + size_bytes + recvd_packet # Put full packet back together

        ##TODO: Verify CRC of received packet

        #print(bytes_cat.hex())
        return bytes_cat

    switch_pin = gpiozero.OutputDevice(23)
    switch_pin.on()

    sleep(0.1)

    def set_mode(self,mode=0, commanded_1=0, commanded_2=0, commanded_3=0,commanded_4=0):
        # Set mode to test mode
        # Need to add cases maybe based on the modes? 
        data_bytes = struct.pack("<Bllll",mode,commanded_1,commanded_2,commanded_3,commanded_4)
        packet = self.create_packet(bytes.fromhex("00"),data=data_bytes)
        print("Writing data: "+packet.hex())
        self.ser.write(packet)
        self.ser.flush()

    # Set X, Y, Z wheel speed
    def set_wheel_speed(self,wheel_speed=0, x=0,y=0,z=0):
        # wheel_speed = 0 # -10,000 to 10,000
        # Create more elegant error check to ensure speeds do note exceed limits
        if -10000 <= wheel_speed <= 10000:
            data_bytes = struct.pack("<hhhBBB",wheel_speed,wheel_speed,wheel_speed,x,y,z)
            packet = self.create_packet(bytes.fromhex("02"),data=data_bytes)
            print("Writing data: "+packet.hex())
            self.ser.write(packet)
            self.ser.flush()
            print("RPM: {}\nX: {}\nY: {}\nZ: {}".format(wheel_speed,x,y,z))
        else: 
            print("Exceeds Limits")

    # Set wheel torque
    def set_wheel_trq(self,wheel_trq=0, x=0,y=0,z=0):
        # wheel_trq = 0 # -1250 to 1250 
        if -1250 <= wheel_trq <= 1250:
            data_bytes = struct.pack("<hhhBBB",wheel_trq,wheel_trq,wheel_trq,x,y,z)
            packet = self.create_packet(bytes.fromhex("5D"),data=data_bytes)
            print("Writing data: "+packet.hex())
            self.ser.write(packet)
            self.ser.flush()
            print("Torque: {}\nX: {}\nY: {}\nZ: {}".format(wheel_trq,x,y,z))
        else: 
            print("Exceeds Limits")

    # Turn off RWS Wheel Speed 
    def turn_off_rws_speed(self):
        data_bytes = struct.pack("<hhhBBB",0,0,0,1,1,1)
        packet = self.create_packet(bytes.fromhex("02"),data=data_bytes)
        print("Writing data: "+packet.hex())
        self.ser.write(packet)
        self.ser.flush()
        print("RPM: {}\nX: {}\nY: {}\nZ: {}".format(0,0,0,0))
        
    # Turn off RWS Wheel Torque 
    def turn_off_rws_trq(self):
        data_bytes = struct.pack("<hhhBBB",0,0,0,1,1,1)
        packet = self.create_packet(bytes.fromhex("5D"),data=data_bytes)
        print("Writing data: "+packet.hex())
        self.ser.write(packet)
        self.ser.flush()
        print("Torque: {}\nX: {}\nY: {}\nZ: {}".format(0,0,0,0))
        