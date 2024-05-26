


import socket
import threading

HOST='127.0.0.1'

PORT=8082

threads=[]




s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)


s.bind((HOST,PORT))

s.listen()


activelist=[]

activeClient=[]

defaultdict={}

print(f"Starting the server at host : {HOST} and port : {PORT}")


def addingActive():

    startingMessage=f" Please specify who you want to talk.Here are the list of active people:\n Use this method to send message: \n Type #<active-id><space><Your Message> \n Type ##<active-id><space><message> to set default active id for message. \n"
    for i in range(len(activelist)):
        startingMessage+=f"{i}."
        startingMessage+=activelist[i]
        if i<len(activelist)-1:
            startingMessage+="\n"
    return startingMessage

def sendmesage(data,client,id):
    trimmed_data=data.strip()
    sender=id
    receiver=defaultdict[id]

    split=trimmed_data.split(' ')
    message=' '
    if len(split)>1:
        message=split[1]


    if(len(trimmed_data)>1):
        if(trimmed_data[0]=="#"):
            receiver=int(trimmed_data[1])
            if(len(trimmed_data)==3 and trimmed_data[1]=="#"):
                receiver=int(trimmed_data[2])
                defaultdict[id]=int(trimmed_data[2])
    else:
        client.sendall(b'please make a valid message')
    if activeClient[receiver]:
        activeClient[receiver].sendall(message.encode("utf-8"))



def handleClient(client):
    data=client.recv(1024)
    while not data:
        pass 
    name=data.decode()
    activelist.append(name)
    id=len(activelist)-1
    defaultdict[id]=0
    activeClient.append(client)
    msg=addingActive()
    client.sendall(msg.encode('utf-8'))
    while True:
        data=client.recv(1024)

        if not data :
            break
        sendmesage(data.decode("utf-8"),client,id)        

        print(data.decode("utf-8"))
    

while True:
    conn,addr=s.accept()
    conn.sendall(b'Please set your name:')

    thread=threading.Thread(target=handleClient,args=(conn,))
    thread.start()
    threads.append(thread)

    print(addr)

    
