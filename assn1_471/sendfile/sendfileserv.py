# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints its contents.
# *****************************************************

import socket
import sys

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

    # ************************************************
    # Receives the specified number of bytes
    # from the specified socket
    # @param sock - the socket from which to receive
    # @param numBytes - the number of bytes to receive
    # @return - the bytes received
    # *************************************************
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
    
    def send_file(sock, file_name):
     try:
        # Open the file in binary mode
        with open(file_name, 'rb') as file_obj:
            # Read the file data
            file_data = file_obj.read()
            
            # Get the size of the data and convert it to string
            data_size_str = str(len(file_data))
            
            # Prepend 0's to the size string until the size is 10 bytes
            data_size_str = data_size_str.zfill(10)
            
            # Send the size of the data to the client
            sock.sendall(data_size_str.encode('utf-8'))
            
            # Send the file data to the client
            sock.sendall(file_data)
            
            print("Sent {file_name} to the client.")
     except IOError:
        print("Error: File {file_name} not found.")



    # Accept connections forever
    while True:
        
        print"Waiting for connections..."
            
        # Accept connections
        clientSock, addr = welcomeSock.accept()
        
        print"Accepted connection from client:", addr
        print"\n"
        
        # The buffer to all data received from the
        # client.
        fileData = ""
        
        # The temporary buffer to store the received
        # data.
        recvBuff = ""
        
        # The size of the incoming file
        fileSize = 0    
        
        # The buffer containing the file size
        fileSizeBuff = ""
        
        # Receive the first 10 bytes indicating the
        # size of the file
        fileSizeBuff = recvAll(clientSock, 10)
        
        # Get the file size
        fileSize = int(fileSizeBuff)
        
        print"The file size is", fileSize
        
        # Get the file data
        fileData = recvAll(clientSock, fileSize)
        
        print"The file data is:"
        print fileData
            
        # Close our side
        clientSock.close()
	