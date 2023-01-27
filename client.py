'''
Author: Mrx
Date: 2023-01-25 13:18:48
LastEditors: Mrx
LastEditTime: 2023-01-26 22:23:15
FilePath: \CS271_project1\client.py
Description: 
Copyright (c) 2023 by Mrx, All Rights Reserved. 
'''


import socket
import threading, time
from sys import exit

print("client")

usertable = {'Alice' : 10882, 'Bob' : 10884, 'Carl' : 10886} 
user = { ('192.168.0.167', 10882) : 'Alice', ('192.168.0.167', 10884) : 'Bob', ('192.168.0.167', 10886) : 'Carl'}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True :
    username = input("Please input your username : ")
    if usertable.get(username) == None :
        print("wrong username!")
        continue
    break

PORT = usertable[username]
HOST = '192.168.0.167'
s.bind((HOST, PORT))

s.sendto(username.encode('utf-8'), (HOST, 10888))
time.sleep(1)
# for key, value in usertable.items():
#     if key != username:
#         s.sendto(username.encode('utf-8'), (HOST, usertable[key]))
#         time.sleep(1)

count = 0

PORT = 10888
flag = True
def RECV():
    while flag:
      (data, addr) = s.recvfrom(1024)
      if usertable.get(data.decode('utf-8')) :
            print("connected to client(%s)" % (data.decode('utf-8')))
      elif data.decode('utf-8') == 'Transfer' :
        print('User(%s) is requesting a transfer' % (user[addr]))
        data = "OK"
        s.sendto(data.encode('utf-8'), addr)
        time.sleep(1)
      elif data.decode('utf-8') == "OK" :
        print('User(%s) agreed to the request' % (user[addr]))
        count = count + 1
        time.sleep(1)
      print(data.decode('utf-8'))
      time.sleep(1)
      
# def SEND():
#    while True:
#       data = input("")
#       s.sendto(data.encode('utf-8'), (HOST, PORT))
#       time.sleep(1)

def UI():
    while True :
        print("1. Transfer money to other clients")
        print("2. Query balance transaction")
        print("3. Print out blockchain")
        print("0. Exit application")
        a = input("please insert command\n")
        if a == "0" :
            flag = False
            # to server
            break
        elif a == "1" :
            info = 'Transfer'
            for key, value in usertable.items():
                if key != username:
                    s.sendto(info.encode('utf-8'), (HOST, usertable[key]))
                    time.sleep(1)
            if count == 3 :
                data = 'Query balance'
                s.sendto(data.encode('utf-8'), (HOST, 10888))
                time.sleep(1)

        elif a == "2" :
            data = 'Query balance'
            s.sendto(data.encode('utf-8'), (HOST, 10888))
            time.sleep(1)

        elif a == "3" :
            pass
        else :
            print("ERROR! Please insert correct command")


t1 = threading.Thread(target=RECV)
t2 = threading.Thread(target=UI)

t1.start()
t2.start()
t1.join()
t2.join()
