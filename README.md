## Modbus Server and Client programs using Python-3
* server.py
* client.py

## Installation:
* sudo pip3 install modbus

## Usage Examples:

### Server:
* sudo python3 -m modbus.server ...to run server
* For Register Reads, the server sends back values incrementing upto 6000. 
* For example, the client wants to read with FuncCode=3, Address=100, and Length=4 
* Then the server's reply for values will be 100,101,102,103
* For Coil Reads, the server sends back values 85,86... for the required length.

### Client:
* python3 -m modbus.client ...to run client in commandline
#### To run the client within another program or interpreter.
* from modbus import client
* c = client(host='localhost') ...Change the localhost to your IP address
* r = c.read(FC=3, ADD=0, LEN=8)
* print("Received Data =", r)  
* c.write(FC=16, ADD=0, DAT=[11,22,333,4444]) ...DAT should be a list of values

