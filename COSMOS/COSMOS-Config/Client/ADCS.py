from ADCSFunctions import *


ADCS = MAI_400()

print("\nRecieving Data")
bytes_cat = ADCS.receive_packet(ADCS.ser)

unpack_length = struct.calcsize("<6sBLBHHHBB");

data = struct.unpack("<6sBLBHHHBB",bytes_cat[:unpack_length])
header = data[0]
time = data[2]
subtime = data[3]
valid_commands = data[4]
invalid_commands = data[5]
invalid_crc = data[6]
last_valid = data[7]
mode = data[8]

ADCS.set_mode(0)
ADCS.set_wheel_speed(500,x=1)

sleep(10)

ADCS.turn_off_rws_speed()

print("Header: "+header.hex())
print("Valid Commands: "+str(valid_commands))
print("Invalid Commands: "+str(invalid_commands))
print("Invalid CRC: "+str(invalid_crc))
print("Last Valid Command: "+last_valid.to_bytes(1,'little').hex())
print("ACS Mode:"+str(mode))