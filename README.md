## Modbus Server and Client programs using Python-3
* server.py
* client.py

## Installation:
* sudo pip3 install modbus

## Usage Examples:

### Server:
* sudo python3 -m modbus.server ...to run server in commandline
* For Register Read, the server sends value starting from 1 and incrementing upto 6000. For example, the client wants to read with FuncCode=3, Address=0, and Length=4. Then the server's reply for values will be 1,2,3,4 for the first read and values will increment for every subsequent read.
* For Coil Reads, the server sends back values 85,86... for the required length.

### Client:
* from modbus.client import *
* c = client() ...if host = 'localhost'
* c = client(host='HOSTNAME') ...Change HOSTNAME to Server IP address
* c.read() ...To read 10 Input Registers from Address 0
* c.read(FC=3, ADR=10, LEN=8) ...To read 8 Holding Registers from Address 10
* c.write(11,22,333,4444) ...To write Holding Registers from Address 0
* c.write(11,22,333,4444, ADR=10) ...To write Holding Registers from Address 10
* c.write(11,22, FC=15, ADR=10) ...To write Coils from Address 10
* fc() ...To get the supported Function Codes

### Supported Function Codes:
* 1 = Read Coils or Digital Outputs\n\
* 2 = Read Digital Inputs\n\
* 3 = Read Holding Registers\n\
* 4 = Read Input Registers\n\
* 5 = Write Single Coil\n\
* 6 = Write Single Register\n\
* 15 = Write Coils or Digital Outputs\n\
* 16 = Write Holding Registers")


