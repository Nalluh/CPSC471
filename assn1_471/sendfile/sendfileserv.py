# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints its contents.
# *****************************************************

import socket
import sys
import os 

def list_text_files_in_directory(directory):
    try:
        # List all files in the given directory
        files = os.listdir(directory)

        # Filter for text files (files ending with '.txt')
        text_files = [file for file in files if file.endswith('.txt')]

        # Print the names of text files
        if text_files:
            print("Text files in {}:".format(directory))
            for text_file in text_files:
                print(text_file)
        else:
            print("No text files found in {}.".format(directory))
    except FileNotFoundError:
        print("Directory not found: {}".format(directory))

def send_file(client_socket, file_path):
    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Read the file content
            file_data = file.read()

            # Send the size of the file data
            client_socket.send(str(len(file_data)).ljust(10).encode())

            # Send the file data
            client_socket.sendall(file_data)
    except FileNotFoundError:
        print("File not found: {}".format(file_path))
        # Handle the case where the file is not found
        
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

def send_file(client_socket, file_path):
    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as file:
            # Read the file content
            file_data = file.read()

            # Send the size of the file data
            client_socket.send(str(len(file_data)).ljust(10).encode())

            # Send the file data
            client_socket.sendall(file_data)
    except FileNotFoundError:
        print("File not found: {}".format(file_path))
        # Inform the client that the file was not found
        client_socket.send(str(0).ljust(10).encode())

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

    #destination_directory = "Downloads"

    isCon = False
    
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
      filename = clientSock.recv(1024).decode()

            # Send the requested file to the client
      send_file(clientSock, filename)

     elif command == "get":
       requested_file = clientSock.recv(1024).decode()
       
       #file_to_send = requested_file[1]
       print requested_file
       send_file(clientSock, file_to_send)


     elif command == "ls":
         directory_path =  os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'assn1_471/sendfile/server'))
         list_text_files_in_directory(directory_path)
    
     elif command == "quit":
           print("Connection has been closed...")
           print("Goodbye...")
           clientSock.close()
           break
        
      