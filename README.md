## Modbus Server and Client

Implementations in Python 3 can be found in
`server.py`
and `client.py`.

## Dependencies

* numpy

## Installation

Using a virtual environment (recommended), install with:

```
python -m venv venv && source venv/bin/activate
(venv) pip3 install modbus
```

If you wish to run with the default modbus/tcp port 502/tcp,
consider creating and activating the virtualenv using sudo.

## Usage Examples

### Server

The IANA defined default TCP port for modbus/tcp is `502/tcp`.
To run on this low-numbered port requires root privileges.

```
sudo python3 -m modbus.server ...to run server in commandline
```

* For Register Read,
  the server sends value starting from 1 and incrementing upto 6000.
  For example,
  the client wants to read with
  `FuncCode=3`,
  `Address=0`,
  `and Length=4`.
  Then the server's reply for values will be
  `1,2,3,4`
  for the first read
  and values will increment
  for every subsequent read.

* For Coil Reads, the server sends back values 85,86... for the required length.

### Client:

```
from modbus.client import *
c = client(host='HOSTNAME')     # Change HOSTNAME to Server IP address, defaults to localhost
c.read()                        # To read 10 Input Registers from Address 0
c.read(FC=3, ADR=10, LEN=8)     # To read 8 Holding Registers from Address 10
c.write(11,22,333,4444)         # To write Holding Registers from Address 0
c.write(11,22,333,4444, ADR=10) # To write Holding Registers from Address 10
c.write(11,22, FC=15, ADR=10)   # To write Coils from Address 10
fc()                            # To get the supported Function Codes
```

### Supported Function Codes:

| Code | Description                    |
|----- | ------------------------------ |
| 1    | Read Coils or Digital Outputs  |
| 2    | Read Digital Inputs            |
| 3    | Read Holding Registers         |
| 4    | Read Input Registers           |
| 5    | Write Single Coil              |
| 6    | Write Single Register          |
| 15   | Write Coils or Digital Outputs |
| 16   | Write Holding Registers        |
