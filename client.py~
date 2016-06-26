#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import pandas as pd

#routing_table_df = pd.read_csv('').to_string()

s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 12345               # Reserve a port for your service.

s.connect((host, port))
print s.recv(1024)
s.close              
