import socket
import sys
import os

def recvAll(sock, numBytes):
    recvBuff = ""
    while len(recvBuff) < numBytes:
        tmpBuff = sock.recv(4096)  # Adjust the buffer size as needed
        if not tmpBuff:
            break
        recvBuff += tmpBuff
    return recvBuff

# Get server address and port from command line arguments
if len(sys.argv) < 3:
    print("Error: Please provide server address and port number.\nIE py cli.py <server machine> <server port>")
    sys.exit(1)

# Server address and port
serverAddr = sys.argv[1]
serverPort = int(sys.argv[2])

while True:
    # Create a TCP socket
    connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    connSock.connect((serverAddr, serverPort))

    # Get user input for selection
    userInput = raw_input("ftp> ")

    # Split the command and file name
    # The first index will have the command, and the second will have the file name
    userInput = userInput.split()
  # If the user input is not one of the listed commands, throw an error and ask them to insert again
    if userInput[0] not in ["get", "put", "ls", "quit"]:
        print("Invalid command")
        connSock.close()
        continue 


    if userInput[0] in ["get", "put"]:
         # If len is less than 2, that means the file name was not provided
     if len(userInput) < 2:
        print("Include the file name")
        connSock.close()
        continue
     else:
      # If the file name provided is not present in the directory, ask for the file name again
      if not os.path.isfile(userInput[1]) and userInput[1] is "put":
        print("File not found, please enter the correct file name to use with", userInput[0], "command")
        connSock.close()
        continue
      else:
       fileName = userInput[1]  # Second half of input contains filename


    

    # Send the command to the server

    if userInput[0] == "quit":
        connSock.send(str(userInput[0]).encode())
        print("Closing connection.")
        connSock.close()
        break

    if userInput[0] == "ls":
        connSock.send(str(userInput[0]).encode())


    
    if userInput[0] == "get":
     connSock.send(str(userInput[0]).encode())
     connSock.send(fileName.encode())
    # Receive file information from the server
     print "test"
     file_info = recvAll(connSock, 1024).decode()
     print "test2"
     file_name, file_size = file_info.split('\n')[:2]
     file_size = int(file_size)

    # Receive the file data from the server
     file_data = recvAll(connSock, file_size)

    # Save the received file
     with open(file_name, "wb") as file_obj:
        file_obj.write(file_data)

     print("Received file:", file_name)

        




    if userInput[0] == "put":
     connSock.send(str(userInput[0]).encode())
     with open(fileName, "r") as fileObj:
        # Read 65536 bytes of data
        fileData = fileObj.read(65536)

        # Make sure we did not hit EOF
        if fileData:
            # Get the size of the data read and convert it to a string
            dataSizeStr = str(len(fileData))

            # Prepend 0's to the size string until the size is 10 bytes
            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr

            # Prepend the size of the data to the file data
            fileData = dataSizeStr + fileData

            # The number of bytes sent
            numSent = 0

            # Send the data
            while len(fileData) > numSent:
                numSent += connSock.send(fileData[numSent:])

            print "Sent File:", fileName, "Containing ",  numSent, "bytes."
            connSock.send(fileName.encode())

        else:
            print("File is empty.")
    

    connSock.close()
