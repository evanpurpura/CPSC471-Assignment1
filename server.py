# Server code
from socket import *
import os, sys

# The port on which to listen (no user arg given)
serverName = "localhost"
serverPort = 1234
contentPort = 2000
reversePort = 2001

#Change ports to user arg
if len(sys.argv) == 2:
    serverPort = int(sys.argv[1])
    contentPort = serverPort + 1
    reversePort = contentPort + 1

# Create a TCP socket
serverSocket = socket(AF_INET, SOCK_STREAM)
contentSocket = socket(AF_INET, SOCK_STREAM)
# Bind the socket to the port
serverSocket.bind(('', serverPort))
contentSocket.bind(('', contentPort))

# Start listening for incoming connections
#serverSocket.listen(1)
print ("The server is ready to receive")

# Forever accept incoming connections
while 1 :
    serverSocket.listen(1)
    # Accept a connection ; get client’s socket
    connectionSocket , addr = serverSocket.accept()
    # Receive whatever the newly connected client has to send
    menu = connectionSocket.recv(1024)
    menu = menu.decode()
    menu = menu.split()
    print("Commands entered: ", menu)
    if len(menu) == 0: continue
    if menu[0] == "put":
        contentSocket.listen(1)
        connect2, addr2 = contentSocket.accept()
        content = connect2.recv(1024)
        print(content.decode())
        connect2.close()
    elif menu[0] == "ls":
        print("Files in server directory:")
        for file in os.listdir():
            print(file)
    elif menu[0] == "get":
        reverseSocket = socket(AF_INET, SOCK_STREAM)
        reverseSocket.connect((serverName, reversePort))
        #check if file exists
        if(os.path.isfile(menu[1])):
            #opens file and stores data
            with open(menu[1]) as file:
                data = file.read()
            file.closed
            dataSize = str(len(data))
            while len(dataSize) < 10:
                dataSize = "0" + dataSize
            data = dataSize + data
            data = data.encode()
            print("Sending file: ", menu[1])
            bytesSent = 0
            while bytesSent != len(data):
                bytesSent += reverseSocket.send(data[bytesSent:])
            reverseSocket.close()
        else:
           print("File does not exist")
           dataSize = "0000000000"
           data = dataSize
           data = data.encode()
           bytesSent = 0
           while bytesSent != len(data):
                bytesSent += reverseSocket.send(data[bytesSent:])
           reverseSocket.close()
        # Close the socket
        connectionSocket.close()