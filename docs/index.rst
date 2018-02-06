.. modbus documentation master file, created by
   sphinx-quickstart on Tue Feb  6 12:19:14 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Modbus Server and Client programs using Python-3
------------------------------------------------

-  server.py
-  client.py

Installation
-------------

-  sudo pip3 install modbus

Usage Examples
---------------

Server
~~~~~~~

-  sudo python3 -m modbus.server …to run server in commandline
-  For Register Read, the server sends value starting from 1 and
   incrementing upto 6000. For example, the client wants to read with
   FuncCode=3, Address=0, and Length=4. Then the server’s reply for
   values will be 1,2,3,4 for the first read and values will increment
   for every subsequent read.
-  For Coil Reads, the server sends back values 85,86… for the required
   length.

Client - run in commandline
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  python3 -m modbus.client 

Client - run within another program or interpreter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  from modbus.client import client
-  c = client(host=‘localhost’)    #Change localhost to IP address
-  r = c.read(FC=3, ADD=0, LEN=8)
-  print(“Received Data =”, r)
-  c.write(FC=16, ADD=0, DAT=[11,22,333,4444]) …DAT should be a list of values
