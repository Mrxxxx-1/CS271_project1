'''
Author: Mrx
Date: 2023-01-25 13:18:48
LastEditors: Mrx
LastEditTime: 2023-01-25 13:43:30
FilePath: \CS271_project1\client.py
Description: 
Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''


import socket
import threading, time
from sys import exit

print("client")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = input("Please input IP address: ")
PORT = 10888

NickName = input("Please input your nick-name : ")
s.sendto(NickName.encode('utf-8'), (HOST, PORT))

def RECV():
   while True:
      (data, addr) = s.recvfrom(1024)
      print(data.decode('utf-8'))
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
   