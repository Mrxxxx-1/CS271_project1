'''
Author: Mrx
Date: 2023-01-25 13:18:48
LastEditors: Mrx
LastEditTime: 2023-01-26 16:19:26
FilePath: \CS271_project1\client.py
Description: 
Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''


import socket
import threading, time
from sys import exit

print("client")
def UI():
    while True :
        print("1. Transfer money to other clients")
        print("2. Query balance transaction")
        print("3. Print out blockchain")
        print("0. Exit application")
        a = input("please insert command\n")
        if a == "0" :
            break
        elif a == "1" :
            pass
        elif a == "2" :
            pass
        elif a == "3" :
            pass
        else :
            print("ERROR! Please insert correct command")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = input("Please input IP address: ")
PORT = 10888

NickName = input("Please input your nick-name : ")
s.sendto(NickName.encode('utf-8'), (HOST, PORT))

def RECV():
    user = {}
    username = {}
    while True:
        (data, addr) = s.recvfrom(1024)
        if user.get(addr, False) == False:  # if the client is new, add it to the local dictionary
            user[addr] = data.decode('utf-8')
            username[data.decode('utf-8')] = addr # another dic with username -- key, addr -- value, easy to query
            print("IP(%s) NickName(%s) has joined the blockchain" % (addr, data.decode('utf-8')))
        else:
            print(addr," : ", data.decode('utf-8'))
            data = user[addr] + " : " + data.decode('utf-8')
            # print(data.decode('utf-8'))
            time.sleep(1)
      
def SEND():
   while True:
      data = input("")
      s.sendto(data.encode('utf-8'), (HOST, PORT))
      time.sleep(1)

t1 = threading.Thread(target=RECV)
t2 = threading.Thread(target=SEND)

t1.start()
t2.start()
t1.join()
t2.join()

def initial() :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    HOST = input("Please input IP address: ")
    PORT = 10888
    NickName = input("Please input your nick-name : ")
    
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    PORT = 1060
 
    network = '<broadcast>'
 
    s.sendto('Client broadcast message!'.encode('utf-8'), (network, PORT))

    s.sendto(NickName.encode('utf-8'), (HOST, PORT))