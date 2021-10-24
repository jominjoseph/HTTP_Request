
import sys
import socket
import struct
import datetime, time
import os.path, time

serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
print("The server is ready to receive on port:  " + str(serverPort) + "\n")


serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))
serverSocket.listen()
connection, addr = serverSocket.accept()
with connection:
    #print("connected by", addr)
    while True:
        #recieve and decode data
        data = connection.recv(1024)
        decodeddata= data.decode('utf-8')
        #print(decodeddata)
        #take filename from data
        
        
        holder1= decodeddata.split("/",1)
        holder2 = (holder1[1]).split(" HTTP",1)
        filename= holder2[0]
       
        # get current time
        current_time = datetime.datetime.now(datetime.timezone.utc)
        current_time= "Date: " + current_time.strftime("%a, %d %b %Y %H:%M:%S %Z")+"\r\n"
        
        try:
            #open file and save contents
            fopen = open(filename, "r")
            if fopen.mode == 'r':
                contents = fopen.read()
                fopen.close()
            
            
            
            #get last modified time change these variables
            modificationT = os.path.getmtime(filename)
            modificationTime = datetime.datetime.utcfromtimestamp(modificationT).strftime("%a, %d %b %Y %H:%M:%S %Z")
            
            #check if file is already updated in cache
            if("If-Modified since" in decodeddata):
                if(modificationTime in decodeddata):
                    responsemessage=""
                    responsemessage += "HTTP/1.1 304 Not Modified\r\n"
                    responsemessage += current_time
                    responsemessage += "\r\n"
                    sendingmessage=responsemessage.encode('utf-8')
                    connection.sendall(sendingmessage)
                    connection.close()
                    print(responsemessage)
                    break;
                #updates information if modification time differs
                else:
                    responsemessage=""
                    responsemessage += "HTTP/1.1 200 OK\r\n"
                    responsemessage += current_time
                    responsemessage += "Last-Modified:" + modificationTime +"UTC\r\n"
                    responsemessage += "Content-Length: " + str(len(contents)) + "\r\n"
                    responsemessage += "Content-Type: text/html; charset=UTF-8\r\n"
                    responsemessage += "\r\n"
                    responsemessage += contents
                    sendingmessage=responsemessage.encode('utf-8')
                    connection.sendall(sendingmessage)
                    connection.close()
                    print(responsemessage)
                    break;

            responsemessage=""
            responsemessage += "HTTP/1.1 200 OK\r\n"
            responsemessage += current_time
            responsemessage += "Last-Modified:" + modificationTime +"UTC\r\n"
            responsemessage += "Content-Length: " + str(len(contents)) + "\r\n"
            responsemessage += "Content-Type: text/html; charset=UTF-8\r\n"
            responsemessage += "\r\n"
            responsemessage += contents
        except FileNotFoundError:
            responsemessage=""
            responsemessage += "HTTP/1.1 404 Not Found\r\n"
            responsemessage += current_time
            responsemessage += "Content-Length: " + str(0) + "\r\n"
            responsemessage += "\r\n"

        #if data is an empty string it will end the program
        if not data:
            break
        #sends response message and closes socket
        print(responsemessage)
        sendingmessage=responsemessage.encode('utf-8')
        connection.sendall(sendingmessage)
        connection.close()
        break;
