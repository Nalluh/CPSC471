import socket
import sys
import os

#once server is running open another terminal
#and run this command to communicate with server
# py .\sendfilecli.py localhost 1234

#so far we can use the put command to send file.txt to server
#need to work on get, ls, and quit





#if no argument provided on command line give error
if len(sys.argv) < 3:
    print("Error: Please provide server address and port number.\nIE py cli.py <server machine> <server port>")
    #else continue with port number and server address given 

else:
    
    # Server address
    serverAddr = sys.argv[1]
    
    # Server port
    serverPort = int(sys.argv[2])

    # The name of the file
   # fileName = "file.txt"

    # Open the file
    #fileObj = open(fileName, "r")

    # Create a TCP socket
    connSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    connSock.connect((serverAddr, serverPort))

    # The number of bytes sent
    numSent = 0

    # The file data
    fileData = None
    
    invalidInput =""
   
    #get user input for selection
    userInput = raw_input("ftp> ")
    #split the command and file name 
    # first index will have the command second the file name 
    userInput = userInput.split()
    
    #if len is less than 2 that means the file name was not provided 
    if len(userInput) < 2:
        invalidInput = True
        print "Include the file name"


    #if user input is not the listed commands throw error and ask them to insert again
    if userInput[0] not in ["get", "put", "ls", "quit"]:
        invalidInput = True
        print "invalid command"

    #until they input a correct command give error
    while invalidInput:
        userInput = raw_input("ftp> ")
        userInput = userInput.split()
        if userInput[0] not in ["get", "put", "ls", "quit"]:
           print "invalid command"
        elif len(userInput) < 2:
           invalidInput = True
           print "Include the file name"
        else:
           invalidInput = False
    

    fileName = userInput[1] # second half of input contains filename

     #if file name provided in not present in directory
     #ask for file name again
    if os.path.isfile(fileName) == False:
     invalidInput = True
     while  invalidInput:
        print "file not found, please enter correct file name to use with ", userInput[0], " command"
        fileName = raw_input()
        #if new input is still not correct, try again
        if os.path.isfile(fileName) == False:
           continue
        #if filename is now valid open it and end while loop
        else:
            fileObj = open(fileName, "r")
            invalidInput = False
            print "File found! Continuning"
    else:
     fileObj = open(fileName, "r")


    
    if userInput[0] == "put":
     
     while True:
        # Read 65536 bytes of data
        fileData = fileObj.read(65536)
        
        # Make sure we did not hit EOF
        if fileData:
            # Get the size of the data read
            # and convert it to string
            dataSizeStr = str(len(fileData))
            
            # Prepend 0's to the size string
            # until the size is 10 bytes
            while len(dataSizeStr) < 10:
                dataSizeStr = "0" + dataSizeStr
        
            # Prepend the size of the data to the
            # file data.
            fileData = dataSizeStr + fileData    
            
            # The number of bytes sent
            numSent = 0
            
            # Send the data!
            while len(fileData) > numSent:
                numSent += connSock.send(fileData[numSent:])

            connSock.send(userInput[0])
        # The file has been read. We are done
        else:
            break
   


    print("Sent", numSent, "bytes.")
    
    # Close the socket and the file
    connSock.close()
    fileObj.close()

