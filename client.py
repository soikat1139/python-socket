

import socket 
import threading
import sys

s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
   s.connect(('127.0.0.1',8082))
except:
    print("Failed to connect")
    s.close()
    sys.exit(1)



#s.sendall(b'hello')


def sendresponse():

    while True:
        msg=str(input(">>"))
        try:
           s.sendall(msg.encode("utf-8"))
        except:
            print("An error occured")
            break


def recvresponse():

    while True:
        data=s.recv(1024)
        if not data:
            break 
        print(data.decode('utf-8'))


t1=threading.Thread(target=sendresponse)
t2=threading.Thread(target=recvresponse)

t1.start()
t2.start()



