
import sys
import socket
import struct

#take in url as commandline argument
url = sys.argv[1]

#find port,hostname, and filename
hostname, filename = url.split("/",1)
hostname, stringport =hostname.split(":",1)
port = (int)(stringport)

#print(stringport +" " + filename)

#connect to server using TCP
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientsocket.settimeout(1)

#print("\nSending Request to "+ str(hostname)+", " + str(port))
#open cache
cache = open("cache.txt", "r+")
cachecontents = cache.read()

counter= 0

#check if filename exists within the cache, if it does send a conditional get
if filename in cachecontents:
    getmessage='GET /' + filename + ' HTTP/1.1\r\n'
    getmessage+= 'Host: ' + hostname + ':' +stringport +'\r\n'
        
    holder1 = cachecontents.split("Last-Modified:",1)
    lastmodifieddate= (holder1[1]).split("\n",1)
    lmd=lastmodifieddate[0]
    #print(lmd)
    
    getmessage+= 'If-Modified since: ' +lmd+'\r\n'
           

    getmessage += '\r\n'
        
    clientsocket.connect((hostname,port))

    message = getmessage.encode('utf-8')

    clientsocket.sendall(message)
    counter=1

if(counter==0):
            #cache.write(filename + "\n"+ responsemessage)
    getmessage='GET /' + filename + ' HTTP/1.1\r\n'
    getmessage+= 'Host: ' + hostname + ':' +stringport +'\r\n'
    getmessage += '\r\n'



    clientsocket.connect((hostname,port))

    message = getmessage.encode('utf-8')

    clientsocket.sendall(message)
        
    
    
    
print(getmessage)




while True:
    
    responsemessage = clientsocket.recv(1024)
    if not responsemessage:
        break
    responsemessage= responsemessage.decode('utf-8')
    
    print(responsemessage)
    if ("200 OK" in responsemessage):
        cache.write(filename + "\n"+ responsemessage)
    break


cache.close()


clientsocket.close()
