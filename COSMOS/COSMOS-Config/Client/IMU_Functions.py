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
