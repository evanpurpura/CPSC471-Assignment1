#! /usr/local/bin/python3

from socket import *

# Name and port number of the server to connect
serverName = "ecs.fullerton.edu"
serverPort = 12000

# Create a socket
clientSocket = socket(_AF_INET, SOCK_STREAM)

# Connect to the server
clientSocket.connect((serverName, serverPort))

# A string we want to send to the server
data = "Hello world! This is a very long string."

# Keep sending bytes untill all bytes are sent
while bytesSent != len(data):
    # Sent that string!
    bytesSent += clientSocket.send(data[bytesSent:])

# Close the socket
clientSocket.close()
