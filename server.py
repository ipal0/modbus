#!/usr/bin/python3
import socket
import _thread
from array import array
from math import ceil
from struct import unpack
import numpy as np


def TCP(conn, addr):
	buffer = array('B', [0] * 300)
	cnt = 0
	hexOf = lambda BUFFER: ','.join([hex(i) for i in BUFFER])
	while True:
		try:
			conn.recv_into(buffer)
			TID0 = buffer[0]   #Transaction ID	to sync
			TID1 = buffer[1]   #Transaction ID 
			ID = buffer[6]	   #Unit ID
			FC = buffer[7]	   #Function Code
			mADR = buffer[8]   #Address MSB
			lADR = buffer[9]   #Address LSB
			ADR = mADR * 256 + lADR 
			LEN = 1
			if FC not in [5,6]: 
				LEN = buffer[10] * 256 + buffer[11]
			BYT = LEN * 2
			print("Received: ", hexOf(buffer[:6+buffer[5]]))
			if (FC in [1, 2, 3, 4]):  # Read Inputs or Registers
				DAT = array('B')
				if FC < 3:
					BYT = ceil(LEN / 8)  # Round off the no. of bytes
					v = 85	# send 85,86.. for bytes.
					for i in range(BYT):
						DAT.append(v)
						v = (lambda x: x + 1 if (x < 255) else 85)(v)
					DATA = DAT
				else:
					DAT = array('B', np.arange(cnt, LEN+cnt, dtype=np.dtype('>i2')).tobytes())
					DATA = [i for i in range(cnt, LEN+cnt)] 
				conn.send(array('B', [TID0, TID1, 0, 0, 0, BYT + 3, ID, FC, BYT]) + DAT)
				print(f"TID = {(TID0 * 256 + TID1)}, ID= {ID}, Fun.Code= {FC}, Address= {ADR}, Length= {LEN}, Data= {DATA}\n--------")
				if cnt < 60000: cnt = cnt + 1
				else: cnt = 1
			elif (FC in [5, 6, 15, 16]):  # Write Registers
				conn.send(array('B', [TID0, TID1, 0, 0, 0, 6, ID, FC, mADR, lADR, buffer[10], buffer[11]]))
				if FC in [5,6]:
					BYT = 2
					buf = buffer[10:12]
				else:
					BYT = buffer[12]
					buf = buffer[13:13+BYT]
				print(f"TID = {(TID0 * 256 + TID1)}, ID= {ID}, Fun.Code= {FC}, Address= {ADR}, Length= {LEN}, Bytes= {BYT}")
				if FC == 5 or FC == 15:
					message = 'bytes: '+ str(unpack('B' * BYT, buf))
				elif FC == 6 or FC == 16:
					message = str(unpack('>' + 'H' * int(BYT / 2), buf))
				print(f"Received Write Values = {message}\n--------")
			else:
				print(f"Funtion Code {FC} Not Supported")
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
