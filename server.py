'''
Author: Mrx
Date: 2023-01-25 13:18:48
LastEditors: Mrx
LastEditTime: 2023-01-25 13:43:09
FilePath: \CS271_project1\server.py
Description: 

Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''



import socket
from sys import exit

print("server")

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

HOST = input("Please input IP address: ")
PORT = 10888

s.bind((HOST, PORT))

user = {}

while True:
   (data, addr) = s.recvfrom(1024)
   if user.get(addr, False) == False:
      user[addr] = data.decode('utf-8')
      print("IP(%s) NickName(%s) Join" % (addr, data.decode('utf-8')))
   else:
      print(addr," : ", data.decode('utf-8'))
      data = user[addr] + " : " + data.decode('utf-8')
      for key, value in user.items():
         if key != addr:
            s.sendto(data.encode('utf-8'), key)

