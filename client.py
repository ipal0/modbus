#!/usr/bin/python3
import socket
from sys import argv
from array import array
from struct import unpack, pack
from math import ceil
from argparse import ArgumentParser
from random import randint

__all__ = ["client"]


class client:
	def __init__(self, host='localhost', unit=1):
		self.host = host
		self.unit = unit
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect((host, 502))
		self.TID = 0

	def fc(self):
		print("Supported Function Codes:\n\
		1 = Read Coils or Digital Outputs\n\
		2 = Read Digital Inputs\n\
		3 = Read Holding Registers\n\
		4 = Read Input Registers\n\
		5 = Write Single Coil\n\
		6 = Write Single Register\n\
		15 = Write Coils or Digital Outputs\n\
		16 = Write Holding Registers")

	def read(self, FC=3, ADR=0, LEN=10):
		lADR = ADR & 0x00FF
		mADR = ADR >> 8
		lLEN = LEN & 0x00FF
		mLEN = LEN >> 8
		if (FC < 3):
			BYT = ceil(LEN / 8)  # Round off the no. of bytes
		else:
			BYT = LEN * 2
		if self.TID < 255: 
			self.TID = self.TID + 1
		else: self.TID = 1
		cmd = array('B', [0, self.TID, 0, 0, 0, 6,
						  self.unit, FC, mADR, lADR, mLEN, lLEN])
		self.sock.send(cmd)
		buf = array('B', [0] * (BYT + 9))
		self.sock.recv_into(buf)
		#print(('Received', buf))
		if (FC > 2):
			return unpack('>' + 'H' * LEN, buf[9:(9 + BYT)])
		else:
			return unpack('B' * BYT, buf[9:(9 + BYT)])

	def write(self, *DAT, FC=16, ADR=0):
		if FC < 5: return(self.fc())
		lADR = ADR & 0x00FF
		mADR = ADR >> 8
		VAL = b''
		for i in DAT:
			VAL = VAL + pack('>H', i)
		if FC == 5 or FC == 6:
			VAL = VAL[0:2]			 
		if FC == 5 or FC == 15:
			LEN = len(VAL) * 8
		else:
			LEN = int(len(VAL) / 2)
		lLEN = LEN & 0x00FF
		mLEN = LEN >> 8
		if self.TID < 255: 
			self.TID = self.TID + 1
		else: self.TID = 1
		if FC == 6:
			cmd = array('B', [0, self.TID, 0, 0, 0, 6, self.unit, FC, mADR, lADR])
		else:
			cmd = array('B', [0, self.TID, 0, 0, 0, 7 + len(VAL), self.unit, FC, mADR, lADR, mLEN, lLEN, len(VAL)])
		cmd.extend(VAL)
		buffer = array('B', [0] * 20)
		print("Sent", cmd)
		self.sock.send(cmd)
		self.sock.recv_into(buffer)
		#print('Received', buffer[:12])
