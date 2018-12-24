#! /usr/local/bin/python3

# Client code
from socket import *
import os, sys

def recvAll(sock, numBytes):
    # The buffer
    recvBuff = ""

    # The temporary buffer
    tmpBuff = ""

    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(numBytes)

        if not tmpBuff:
            break

        tmpBuff = tmpBuff.decode()
        recvBuff += tmpBuff
    return recvBuff

# Name and port number of the server (no user arg given)
serverName = "localhost"
serverPort = 1234
contentPort = 2000
reversePort = 2001

# Change ports to user arg
if len(sys.argv) == 3:
    serverName = sys.argv[1]
    serverPort = int(sys.argv[2])
    contentPort = serverPort + 1
    reversePort = contentPort + 1

# User menu for client
while True:
    # Connect or reconnect to the server
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))
    print('ftp>', end='', flush=True)
    # splits user input so it can read multiple arguments
    word = input()
    words = word.split()
    if words[0] == "quit":
        clientSocket.send(words[0].encode())
        break
    elif words[0] == "get":
        # Send command and filename to search from server
        if len(words) == 1: continue
        filename = words[1]
        clientSocket.send((words[0] + " " + words[1]).encode())
        # Attempt to start a server-like connection to receive file
        recvSocket = socket(AF_INET, SOCK_STREAM)
        recvSocket.bind(('', reversePort))
        recvSocket.listen(1)
        connect2, addr2 = recvSocket.accept()
        fileSizeBuff = ""
        # gets us the size of the data
        fileSizeBuff = recvAll(connect2, 10)
        if fileSizeBuff == 0:
            connect2.close()
        else:
            fileSize = int(fileSizeBuff)
            # pass in the size of the data so that we can recv it all
            content = recvAll(connect2, fileSize)
            print(content)

            # Create a text file from server
            f = open(words[1], "w+")
            f.write(content)
            f.close()

            connect2.close()
    elif words[0] == "ls":
        # list files on server
        clientSocket.send(words[0].encode())
        # Attempt to start a server-like connection to receive file
        recvSocket = socket(AF_INET, SOCK_STREAM)
        recvSocket.bind(('', reversePort))
        recvSocket.listen(1)
        connect2, addr2 = recvSocket.accept()
        fileSizeBuff = ""
        # gets us the size of the data
        fileSizeBuff = recvAll(connect2, 10)
        if fileSizeBuff == 0:
            connect2.close()
        else:
            fileSize = int(fileSizeBuff)
            # pass in the size of the data so that we can recv it all
            content = recvAll(connect2, fileSize)
            print(content)
            connect2.close()

    elif words[0] == "put":
        if len(words) == 1: continue
        filename = words[1]
        exists = os.path.isfile(words[1])
        if (exists):
            clientSocket.send((words[0] + " " + words[1]).encode())
            contentSocket = socket(AF_INET, SOCK_STREAM)
            contentSocket.connect((serverName, contentPort))
            # Opens file and sends data over contentSocket
            with open(filename) as file:
                data = file.read()
            file.closed
            data = data.encode()
            print("Sending file: ", filename)
            bytesSent = 0
            while bytesSent != len(data):
                bytesSent += contentSocket.send(data[bytesSent:])
            contentSocket.close()
        else:
            print("File does not exist")
    else:
        print("Invalid command")
# Close final connection
clientSocket.close()
