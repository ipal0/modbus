#!/usr/bin/python3
import socket
from sys import argv
from array import array
from struct import unpack, pack
from math import ceil
from argparse import ArgumentParser
from random import randint

__all__ = ["client"]

def Help():
    print("Supported Function Codes:\n\
          1 = Read Coils or Digital Outputs\n\
          2 = Read Digital Inputs\n\
          3 = Read Holding Registers\n\
          4 = Read Input Registers\n\
          5 = Write Single Coil\n\
          6 = Write Single Register\n\
          15 = Write Coils or Digital Outputs\n\
          16 = Write Holding Registers")

class client:
    def __init__(self, host='localhost', unit=1):
        self.host = host
        self.unit = unit
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, 502))

    def read(self, FC, ADD, LEN):
        lADD = ADD & 0x00FF
        mADD = ADD >> 8
        lLEN = LEN & 0x00FF
        mLEN = LEN >> 8
        if (FC < 3):
            BYT = ceil(LEN / 8)  # Round off the no. of bytes
        else:
            BYT = LEN * 2
        cmd = array('B', [0, randint(0, 255), 0, 0, 0, 6,
                          self.unit, FC, mADD, lADD, mLEN, lLEN])
        self.sock.send(cmd)
        buf = array('B', [0] * (BYT + 9))
        self.sock.recv_into(buf)
        #print(('Received', buf))
        if (FC > 2):
            return unpack('>' + 'H' * LEN, buf[9:(9 + BYT)])
        else:
            return unpack('B' * BYT, buf[9:(9 + BYT)])

    def write(self, FC, ADD, DAT):
        lADD = ADD & 0x00FF
        mADD = ADD >> 8
        VAL = b''
        for i in DAT:
            VAL = VAL + pack('>H', int(i))
        if FC == 5 or FC == 6:
            VAL = VAL[0:2]           
        if FC == 5 or FC == 15:
            LEN = len(VAL) * 8
        else:
            LEN = int(len(VAL) / 2)
        lLEN = LEN & 0x00FF
        mLEN = LEN >> 8
        if FC == 6:
            cmd = array('B', [0, 0, 0, 0, 0, 6, self.unit, FC, mADD, lADD])
        else:
            cmd = array('B', [0, 0, 0, 0, 0, 7 + len(VAL), self.unit, FC, mADD, lADD, mLEN, lLEN, len(VAL)])
        cmd.extend(VAL)
        buffer = array('B', [0] * 20)
        print("Sent", cmd)
        self.sock.send(cmd)
        self.sock.recv_into(buffer)
        #print('Received', buffer[:12])

if __name__ == "__main__":
    parser = ArgumentParser(description="Modbus Client Program")
    parser.add_argument('-i', dest='host', type=str,
                        help="Host Name or IP Address [Default=localhost]", default="localhost")
    parser.add_argument('-u', dest='unit', type=int,
                        help="Unit Number [Default=1]", default=1)
    args = parser.parse_args()
    c = client(args.host, args.unit)
    while True:
        S = input("Enter: FunctionCode, Address, Length of Registers to Read or Value of Registers to Write\n")
        L = S.strip().split(',')
        try:
            FC = int(L[0])
            if FC in [1,2,3,4]:
                print("Received =", c.read(int(L[0]), int(L[1]), int(L[2])))
            elif FC in [5,6,15,16]:
                c.write(int(L[0]), int(L[1]), L[2:])
        except Exception:
            Help()
