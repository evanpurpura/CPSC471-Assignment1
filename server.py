#! /usr/local/bin/python3

# Server Code
from socket import *

# The port on which to listen
serverPort = 12000

# Create a TCP socket
serverSocket = socket(_AF_INET,SOCK_STREAM)

# Bind the socket to the serverPort
serverSocket.bind(('',serverPort))

# Start listening for incoming connections
serverSocket.listen(1)

while 1:
    # Accept a connection; get client's socket
    connectionSocket,addr = serverSocket.accept()

    # The temporary buffer
    tmpBuff = ""

    while len(data) != 40:
        # Recieve whatever the newly connected client has to send
        tmpBuff = connectionSocket.recv(40)

        # The other side unexpectly closed it's socket
        if not tmpBuff:
            break

        # Save the data
        data += tmpBuff

    print data

    # Close the socket
    connectionSocket.close()
