#!/usr/bin/python3
import socket
import _thread
from array import array
from math import ceil
from struct import unpack

def TCP(conn, addr):
    """
## This Modbus server accepts connections from multiple clients. 
## Supported Function Codes are:
    * 1 = Read Coils or Digital Outputs
    * 2 = Read Digital Inputs
    * 3 = Read Holding Registers or Analog Outputs
    * 4 = Read Input Registers or Analog Inputs
    * 5 = Write Single Coil
    * 6 = Write Single Register or Analog Output
    * 15 = Write Coils or Digital Outputs
    * 16 = Write Holding Registers or Analog Outputs
## Installation:
    * sudo pip3 install modbus
## Usage
    * sudo python3 -m modbus.server
"""
    buffer = array('B', [0] * 300)
    while True:
        try:
            conn.recv_into(buffer)
            TID0 = buffer[0]   #Transaction ID  to sync
            TID1 = buffer[1]   #Transaction ID 
            ID = buffer[6]     #Unit ID
            FC = buffer[7]
            mADR = buffer[8]
            lADR = buffer[9]
            ADR = mADR * 256 + lADR
            LEN = buffer[10] * 256 + buffer[11]
            BYT = LEN * 2
            print("Received = ", buffer[0:13 + buffer[12]])
            if (FC in [1, 2, 3, 4]):  # Read Inputs or Registers
                DAT = array('B')
                if FC < 3:
                    BYT = ceil(LEN / 8)  # Round off the no. of bytes
                    v = 85  # send 85,86.. for bytes.
                    for i in range(BYT):
                        DAT.append(v)
                        v = (lambda x: x + 1 if (x < 255) else 85)(v)
                else:
                    for i in range(LEN):  # Sends back the address as data
                        DAT.append(mADR)
                        DAT.append(lADR)
                        if (lADR == 255):
                            lADR = 0
                            mADR = mADR + 1
                        else:
                            lADR = lADR + 1
                print("TID = %d, ID= %d, Fun.Code= %d, Address= %d, Length= %d" \
                      %((TID0 * 256 + TID1), ID, FC, ADR, LEN))
                conn.send(
                    array('B', [TID0, TID1, 0, 0, 0, BYT + 3, ID, FC, BYT]) + DAT)
            elif (FC in [5, 6, 15, 16]):  # Write Registers
                BYT = buffer[12]
                conn.send(
                    array('B', [TID0, TID1, 0, 0, 0, 6, ID, FC, mADR, lADR, buffer[10], buffer[11]]))
                buf = buffer[13:(13 + BYT)]
                print("TID = %d, ID= %d, Fun.Code= %d, Address= %d, Length= %d, Bytes= %d" \
                          %((TID0 * 256 + TID1), ID, FC, ADR, LEN, BYT))
                if FC == 5 or FC == 15:
                    message = 'bytes: '+ str(unpack('B' * BYT, buf))
                elif FC == 6 or FC == 16:
                    message = str(unpack('>' + 'H' * int(BYT / 2), buf))
                print("Received Write Values =", message)
            else:
                print("Funtion Code %d Not Supported" % FC)
                exit()
        except Exception as e:
            print(e, "\nConnection with Client terminated")
            exit()

if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 502))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        print("Connected by", addr[0])
        _thread.start_new_thread(TCP, (conn, addr))
