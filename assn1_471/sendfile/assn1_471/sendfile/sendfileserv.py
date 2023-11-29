# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints its contents.
# *****************************************************

import socket
import sys
def recvAll(sock, numBytes):
        # The buffer
        recvBuff = ""
        
        # The temporary buffer
        tmpBuff = ""
        
        # Keep receiving until all is received
        while len(recvBuff) < numBytes:
            
            # Attempt to receive bytes
            tmpBuff = sock.recv(numBytes)
            
            # The other side has closed the socket
            if not tmpBuff:
                break
            
            # Add the received bytes to the buffer
            recvBuff += tmpBuff
        
        return recvBuff
# run command below on a terminal to start up server
# py .\sendfileserv.py 1234


# port # given by user on command line

#if no argument provided on command line give error
if len(sys.argv) < 2:
    print("Error: Please provide port number.\nIE: py serv.py <PORTNUMBER>")
#else continue with port number given 
else:
    listenPort = int(sys.argv[1])

    # Create a welcome socket.
    welcomeSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the port
    welcomeSock.bind(('', listenPort))

    # Start listening on the socket
    welcomeSock.listen(1)

    

    isCon = False
    files = []
    print "Waiting for connections..."
    # Accept connections forever
while True:
        

        # Accept connections
     clientSock, addr = welcomeSock.accept()
     if not isCon:
      print"Accepted connection from client:", addr
      print"\n"
      isCon = True

     command = clientSock.recv(1024).decode()

     if command == "put":
      print("Receiving file...")
        
        # Receive the size of the file data
      fileSize = int(recvAll(clientSock, 10))
        
        # Receive the file data
      fileData = recvAll(clientSock, fileSize)
        
        # The rest of the data received is the command ("put")
      fileName = clientSock.recv(1024).decode()

      files.append(fileName)

      print "Received file: ", fileName,  "content:"
      print(fileData)

     elif command == "get":
       requested_file = clientSock.recv(1024).decode()

        # Check if the requested file exists
       if requested_file in files:
            print("Sending file: %s" % requested_file)

            # Read the file content
            with open(requested_file, "rb") as fileObj:
                fileData = fileObj.read(65536)

            # Send the file content size as a string followed by a newline character
            file_info = requested_file + '\n' + str(len(fileData)) + '\n'
            clientSock.sendall(file_info.encode())

            # Send the file content
            numSent = 0
            while numSent < len(fileData):
                numSent += clientSock.send(fileData[numSent:])
            
            print("Sent %d bytes." % numSent)
       else:
            print("File %s not found on the server." % requested_file)


     elif command == "ls":
         if len(files) == 0:
             print("No files available.")
         for file in files:
             print(file)
             
     elif command == "quit":
           print("Connection has been closed...")
           print("Goodbye...")
           clientSock.close()
           break
        
      